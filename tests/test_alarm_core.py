"""Focused contract tests against the complete, canonical scenario data."""

import unittest
from pathlib import Path

from src.alarm_core import analyze


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "docs" / "project" / "senaryo"
REQUIRED_FIELDS = {
    "incident_id", "status", "priority", "start_at", "end_at", "alarm_count", "noise_count",
    "root_cause_hypothesis", "confidence", "alternative_hypothesis", "affected_services",
    "affected_hosts", "evidence", "recommended_first_action", "action_owner", "action_status",
}


class DeterministicAlarmCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = analyze(DATA_DIR)
        cls.cards = {card["incident_id"]: card for card in cls.report["incident_cards"]}

    def test_processes_and_accounts_for_all_3000_records(self) -> None:
        dispositions = self.report["alarm_dispositions"]
        self.assertEqual(3000, self.report["input_alarm_count"])
        self.assertEqual(3000, len(dispositions))
        self.assertEqual(3000, len({row["alarm_id"] for row in dispositions}))
        self.assertTrue(all(row["disposition"] == "event" or row.get("noise_reason") for row in dispositions))

    def test_cards_are_capped_and_have_the_required_contract(self) -> None:
        self.assertGreaterEqual(len(self.cards), 1)
        self.assertLessEqual(len(self.cards), 15)
        for card in self.cards.values():
            self.assertTrue(REQUIRED_FIELDS <= card.keys())
            self.assertGreater(card["alarm_count"], 0)
            self.assertTrue(card["evidence"])

    def test_detects_the_three_evidence_backed_event_families(self) -> None:
        expected = {
            "INC-DC1-RACK-A-NETWORK": "DC1/rack-A",
            "INC-BILLING-DB-DISK": "billing-db",
            "INC-EXTERNAL-PAYMENT-GATEWAY": "ödeme sağlayıcısı",
        }
        self.assertEqual(set(expected), set(self.cards))
        for incident_id, expected_text in expected.items():
            self.assertIn(expected_text, self.cards[incident_id]["root_cause_hypothesis"])
            self.assertGreater(self.cards[incident_id]["alarm_count"], 10)


if __name__ == "__main__":
    unittest.main()