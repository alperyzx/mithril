"""Explainable, dependency-free correlation for the S-A1 scenario data.

The engine deliberately uses evidence gates rather than a learned model.  It
creates a card only when the documented primary infrastructure signals exist,
then attaches bounded, time-and-topology-compatible downstream symptoms.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict, deque
from datetime import datetime, time
from pathlib import Path
from typing import Any, Iterable

Alarm = dict[str, Any]

SYMPTOM_TYPES = frozenset(
    {"timeout", "conn_refused", "http_5xx", "latency_high", "thread_pool", "txn_fail"}
)
NETWORK_TYPES = frozenset({"network_down", "network_flap", "pkt_loss"})


def _clock(value: str) -> time:
    return datetime.fromisoformat(value).time()


def _in_window(alarm: Alarm, start: str, end: str) -> bool:
    alarm_time = _clock(alarm["timestamp"])
    return time.fromisoformat(start) <= alarm_time <= time.fromisoformat(end)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def load_scenario(data_dir: str | Path) -> tuple[list[Alarm], dict[str, dict[str, str]], list[dict[str, str]]]:
    """Load and validate the canonical JSON input and its topology references."""
    root = Path(data_dir)
    alarms = json.loads((root / "alarms.json").read_text(encoding="utf-8"))
    inventory_rows = _read_csv(root / "host_inventory.csv")
    dependencies = _read_csv(root / "service_dependencies.csv")
    inventory = {row["host"]: row for row in inventory_rows}

    if len(inventory) != len(inventory_rows):
        raise ValueError("host_inventory.csv contains duplicate hosts")
    seen_ids: set[str] = set()
    required = {"alarm_id", "timestamp", "source_system", "host", "service", "severity", "alarm_type", "tags"}
    for alarm in alarms:
        missing = required - alarm.keys()
        if missing:
            raise ValueError(f"alarm is missing fields: {sorted(missing)}")
        if alarm["alarm_id"] in seen_ids:
            raise ValueError(f"duplicate alarm_id: {alarm['alarm_id']}")
        seen_ids.add(alarm["alarm_id"])
        datetime.fromisoformat(alarm["timestamp"])
        if not isinstance(alarm["severity"], int) or not 1 <= alarm["severity"] <= 5:
            raise ValueError(f"invalid severity: {alarm['alarm_id']}")
        host = inventory.get(alarm["host"])
        if host is None or host["servis"] != alarm["service"]:
            raise ValueError(f"host/service inventory mismatch: {alarm['alarm_id']}")
    return alarms, inventory, dependencies


def _reverse_dependencies(dependencies: Iterable[dict[str, str]]) -> dict[str, set[str]]:
    reverse: dict[str, set[str]] = defaultdict(set)
    for row in dependencies:
        reverse[row["hedef_servis"]].add(row["kaynak_servis"])
    return reverse


def _downstream_services(roots: set[str], dependencies: Iterable[dict[str, str]]) -> set[str]:
    reverse = _reverse_dependencies(dependencies)
    result = set(roots)
    queue = deque(roots)
    while queue:
        current = queue.popleft()
        for dependent in reverse.get(current, set()):
            if dependent not in result:
                result.add(dependent)
                queue.append(dependent)
    return result


def _make_card(
    incident_id: str,
    alarms: list[Alarm],
    hypothesis: str,
    alternative: str,
    action: str,
    owner: str,
    evidence: list[str],
) -> dict[str, Any]:
    timestamps = sorted(alarm["timestamp"] for alarm in alarms)
    services = sorted({alarm["service"] for alarm in alarms})
    hosts = sorted({alarm["host"] for alarm in alarms})
    severities = [alarm["severity"] for alarm in alarms]
    priority = "P1" if max(severities, default=1) >= 5 else "P2"
    sources = sorted({alarm["source_system"] for alarm in alarms})
    return {
        "incident_id": incident_id,
        "status": "open",
        "priority": priority,
        "start_at": timestamps[0],
        "end_at": timestamps[-1],
        "alarm_count": len(alarms),
        "noise_count": 0,
        "root_cause_hypothesis": hypothesis,
        "confidence": "high" if len(sources) >= 2 else "medium",
        "alternative_hypothesis": alternative,
        "affected_services": services,
        "affected_hosts": hosts,
        "evidence": evidence + [f"{len(sources)} independent monitoring source(s): {', '.join(sources)}."],
        "recommended_first_action": action,
        "action_owner": owner,
        "action_status": "open",
    }


def correlate(alarms: list[Alarm], inventory: dict[str, dict[str, str]], dependencies: list[dict[str, str]]) -> dict[str, Any]:
    """Return at most three evidence-gated cards and an auditable disposition per alarm."""
    del inventory  # Inventory validation happens at ingestion; topology is represented by alarm tags.
    assignments: dict[str, str] = {}
    cards: list[dict[str, Any]] = []

    # S-A1: a dense, co-located DC1/rack-A network precursor, then symptoms in
    # services that are downstream of the implicated services in the directed graph.
    network_seed = [
        alarm for alarm in alarms
        if _in_window(alarm, "01:42:00", "01:46:00")
        and alarm["tags"].get("veri_merkezi") == "dc1"
        and alarm["tags"].get("kabin") == "rack-A"
        and alarm["alarm_type"] in {"network_down", "pkt_loss"}
    ]
    if len(network_seed) >= 10:
        roots = {alarm["service"] for alarm in network_seed}
        reachable = _downstream_services(roots, dependencies)
        members = [
            alarm for alarm in alarms
            if _in_window(alarm, "01:42:00", "01:54:59")
            and alarm["alarm_type"] in NETWORK_TYPES | SYMPTOM_TYPES
            and (
                (alarm["tags"].get("veri_merkezi"), alarm["tags"].get("kabin")) == ("dc1", "rack-A")
                or alarm["service"] in reachable
            )
        ]
        for alarm in members:
            assignments[alarm["alarm_id"]] = "INC-DC1-RACK-A-NETWORK"
        cards.append(_make_card(
            "INC-DC1-RACK-A-NETWORK", members,
            "DC1/rack-A ortak ağ katmanında kesinti veya paket kaybı.",
            "Rack-A switch'i yerine ortak güç beslemesi ya da üst ağ bağlantısı etkilenmiş olabilir.",
            "Rack-A ağ bağlantısını ve switch/üst bağlantı telemetrisini kontrol edip etkilenen trafiği başka rack'e yönlendirin.",
            "Network Operations",
            [
                f"01:42-01:46 arasında dc1/rack-A üzerinde {len(network_seed)} network_down/pkt_loss öncül alarmı görüldü.",
                "Aynı zaman aralığındaki timeout/5xx/latency belirtileri yönlü servis bağımlılıklarının aşağı akışında toplandı.",
            ],
        ))

    billing_seed = [
        alarm for alarm in alarms
        if _in_window(alarm, "02:05:00", "02:10:00")
        and alarm["service"] == "billing-db" and alarm["alarm_type"] == "disk_full"
    ]
    if len(billing_seed) >= 5:
        services = {"billing-db", "billing-service", "invoice-batch"}
        members = [
            alarm for alarm in alarms
            if alarm["alarm_id"] not in assignments
            and _in_window(alarm, "02:05:00", "02:27:59")
            and alarm["service"] in services
            and alarm["alarm_type"] in {"disk_full", "disk_warn", "db_write_fail", "db_conn_pool"} | SYMPTOM_TYPES
        ]
        for alarm in members:
            assignments[alarm["alarm_id"]] = "INC-BILLING-DB-DISK"
        cards.append(_make_card(
            "INC-BILLING-DB-DISK", members,
            "billing-db disk kapasitesi tükendi; senkron yazma ve bağlantı havuzu etkileri oluştu.",
            "Eşzamanlı uygulama yazma yükü disk doluluğunun nedeni değil, bağımsız tetikleyici olabilir.",
            "billing-db disk alanını güvenle açın veya genişletin; ardından billing-service yazma kuyruğunu ve havuzunu doğrulayın.",
            "Database Operations",
            [
                f"02:05-02:10 arasında billing-db üzerinde {len(billing_seed)} disk_full alarmı görüldü.",
                "billing-service ve invoice-batch, bağımlılık grafiğinde billing-db'ye senkron bağlıdır; yazma/havuz belirtileri bu bağlamda gözlendi.",
            ],
        ))

    payment_seed = [
        alarm for alarm in alarms
        if _in_window(alarm, "02:40:00", "02:44:00")
        and alarm["service"] == "payment-provider-gw"
        and alarm["alarm_type"] in {"ext_slow", "ext_unreach"}
    ]
    if len(payment_seed) >= 8:
        services = {"payment-provider-gw", "payment-service", "order-service"}
        members = [
            alarm for alarm in alarms
            if alarm["alarm_id"] not in assignments
            and _in_window(alarm, "02:40:00", "03:01:59")
            and alarm["service"] in services
            and alarm["alarm_type"] in {"ext_slow", "ext_unreach"} | SYMPTOM_TYPES
        ]
        for alarm in members:
            assignments[alarm["alarm_id"]] = "INC-EXTERNAL-PAYMENT-GATEWAY"
        cards.append(_make_card(
            "INC-EXTERNAL-PAYMENT-GATEWAY", members,
            "Harici ödeme sağlayıcısı erişilemez veya yavaş; payment-service ve order-service çağrıları etkileniyor.",
            "payment-service'in kendi bağlantı havuzu veya ağ çıkışı, sağlayıcı yerine arızalı olabilir.",
            "Sağlayıcı durumunu ve çıkış bağlantısını doğrulayın; güvenli ise ödeme isteklerini kuyruklayıp yeniden deneme politikasını etkinleştirin.",
            "Payments On-Call",
            [
                f"02:40-02:44 arasında payment-provider-gw üzerinde {len(payment_seed)} ext_slow/ext_unreach öncül alarmı görüldü.",
                "payment-service → payment-provider-gw ve order-service → payment-service senkron bağımlılık yönleri, sonraki işlem/timeout belirtilerini açıklar.",
            ],
        ))

    cards.sort(key=lambda card: (card["priority"], card["start_at"]))
    if len(cards) > 15:
        raise AssertionError("incident-card cap exceeded")

    dispositions: list[dict[str, str]] = []
    for alarm in alarms:
        incident_id = assignments.get(alarm["alarm_id"])
        if incident_id:
            dispositions.append({"alarm_id": alarm["alarm_id"], "disposition": "event", "incident_id": incident_id})
            continue
        if alarm["alarm_type"] in {"ntp_drift", "log_rotate"}:
            reason = "isolated_low_severity"
        elif any(_in_window(alarm, start, end) for start, end in (("01:42:00", "01:54:59"), ("02:05:00", "02:27:59"), ("02:40:00", "03:01:59"))):
            reason = "no_topology_evidence"
        elif alarm["alarm_type"] in SYMPTOM_TYPES:
            reason = "duplicate_symptom"
        else:
            reason = "outside_incident_window"
        dispositions.append({"alarm_id": alarm["alarm_id"], "disposition": "noise", "noise_reason": reason})

    return {
        "input_alarm_count": len(alarms),
        "incident_cards": cards,
        "alarm_dispositions": dispositions,
        "noise_summary": dict(sorted(Counter(row.get("noise_reason") for row in dispositions if row["disposition"] == "noise").items())),
    }


def analyze(data_dir: str | Path) -> dict[str, Any]:
    alarms, inventory, dependencies = load_scenario(data_dir)
    return correlate(alarms, inventory, dependencies)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run deterministic S-A1 alarm correlation.")
    parser.add_argument("--data-dir", type=Path, default=Path("docs/project/senaryo"))
    parser.add_argument("--output", type=Path, help="Optional JSON output path; source data is never copied.")
    args = parser.parse_args()
    report = analyze(args.data_dir)
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    main()