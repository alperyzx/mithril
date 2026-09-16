const reasonLabels = {
  isolated_low_severity: "İzole düşük şiddet",
  no_topology_evidence: "Topoloji kanıtı yok",
  duplicate_symptom: "Tekrarlayan türev belirti",
  outside_incident_window: "Olay penceresi dışında",
};
let dashboard;

const formatTime = (value) => new Intl.DateTimeFormat("tr-TR", { hour: "2-digit", minute: "2-digit", second: "2-digit" }).format(new Date(value));
const setText = (selector, text) => document.querySelector(selector).textContent = text;
const statusClass = (status) => `status status-${status}`;

const countList = (title, values) => `<div><b>${title}</b><ul>${Object.entries(values).map(([name, count]) => `<li>${name}: <strong>${count}</strong></li>`).join("")}</ul></div>`;
const topEntries = (values, limit = 6) => Object.entries(values).slice(0, limit);

function horizontalBars(title, values, limit = 6) {
  const entries = topEntries(values, limit);
  const maximum = Math.max(...entries.map(([, count]) => count), 1);
  return `<figure class="bar-chart"><figcaption>${title}</figcaption>${entries.map(([name, count]) => `<div class="bar-row"><span title="${name}">${name}</span><i><b style="width:${count / maximum * 100}%"></b></i><strong>${count}</strong></div>`).join("")}</figure>`;
}

function volumeChart(values) {
  const entries = Object.entries(values);
  const maximum = Math.max(...entries.map(([, count]) => count), 1);
  return `<figure class="volume-chart"><figcaption>Zaman içindeki alarm yoğunluğu</figcaption><div class="volume-bars">${entries.map(([minute, count]) => `<div title="${minute}: ${count} alarm"><i style="height:${Math.max(8, count / maximum * 100)}%"></i><span>${minute.slice(3)}</span></div>`).join("")}</div></figure>`;
}

function renderCard(card) {
  const node = document.getElementById("card-template").content.firstElementChild.cloneNode(true);
  node.dataset.incidentId = card.incident_id;
  node.querySelector(".priority").textContent = card.priority;
  node.querySelector(".confidence").textContent = card.priority === "P1" ? "S5 kritik alarm" : "S4 büyük alarm";
  node.querySelector("h3").textContent = card.incident_id;
  node.querySelector(".time-range").textContent = `${formatTime(card.start_at)} — ${formatTime(card.end_at)} · ${card.alarm_count} alarm`;
  node.querySelector(".hypothesis p").textContent = card.root_cause_hypothesis;
  node.querySelector(".alternative p").textContent = card.alternative_hypothesis;
  for (const service of card.affected_services) {
    const item = document.createElement("li"); item.textContent = service; node.querySelector(".services").append(item);
  }
  for (const evidence of card.evidence) {
    const item = document.createElement("li"); item.textContent = evidence; node.querySelector(".evidence").append(item);
  }
  node.querySelector(".recommended-action p").textContent = card.recommended_first_action;
  node.querySelector(".owner").textContent = `Sahip: ${card.action_owner}`;
  const status = node.querySelector(".status");
  status.className = statusClass(card.action_status); status.textContent = "Açık";
  return node;
}

function render() {
  const { input_alarm_count, incident_card_count, max_incident_cards, incident_cards, noise_summary, noise_total } = dashboard;
  setText("#processed-count", `${input_alarm_count}/${input_alarm_count}`);
  setText("#card-count", incident_card_count);
  setText("#card-cap", max_incident_cards);
  setText("#noise-count", noise_total.toLocaleString("tr-TR"));
  setText("#reduction", `%${(noise_total / input_alarm_count * 100).toFixed(1).replace(".", ",")}`);
  const cards = document.getElementById("cards"); cards.replaceChildren(...incident_cards.map(renderCard));
  const selection = document.getElementById("evidence-card"); selection.replaceChildren(...incident_cards.map(card => new Option(`${card.incident_id} · ${card.root_cause_hypothesis}`, card.incident_id)));
  const reasons = document.getElementById("noise-reasons");
  reasons.replaceChildren(...Object.entries(noise_summary).map(([reason, count]) => {
    const row = document.createElement("div"); row.innerHTML = `<span>${reasonLabels[reason] || reason}</span><strong>${count.toLocaleString("tr-TR")}</strong>`; return row;
  }));
}

async function load() {
  const response = await fetch("/api/dashboard");
  if (!response.ok) throw new Error("Dashboard data could not be loaded.");
  dashboard = await response.json(); render();
}

document.getElementById("load-evidence").addEventListener("click", async () => {
  const incidentId = document.getElementById("evidence-card").value;
  const feedback = document.getElementById("evidence-feedback");
  const result = document.getElementById("evidence-result");
  try {
    const response = await fetch(`/api/evidence/${encodeURIComponent(incidentId)}`);
    if (!response.ok) throw new Error("Evidence load failed");
    const evidence = await response.json();
    result.hidden = false;
    result.innerHTML = `<p><strong>${evidence.raw_alarm_count}</strong> ham alarm · ${formatTime(evidence.window.start_at)} — ${formatTime(evidence.window.end_at)}</p><div class="visualization-grid">${volumeChart(evidence.minute_counts)}${horizontalBars("En sık alarm türleri", evidence.alarm_type_counts)}${horizontalBars("En çok etkilenen servisler", evidence.service_counts)}${horizontalBars("Veri merkezi / kabin dağılımı", evidence.location_counts)}</div><div class="evidence-grid">${countList("Alarm türleri", evidence.alarm_type_counts)}${countList("Servisler", evidence.service_counts)}${countList("Kaynak sistemler", evidence.source_system_counts)}</div><details><summary>İlk 12 ham alarmı göster</summary><table><thead><tr><th>Saat</th><th>Servis</th><th>Host</th><th>Tip</th><th>S</th></tr></thead><tbody>${evidence.sample_alarms.map(alarm => `<tr><td>${formatTime(alarm.timestamp)}</td><td>${alarm.service}</td><td>${alarm.host}</td><td>${alarm.alarm_type}</td><td>${alarm.severity}</td></tr>`).join("")}</tbody></table></details>`;
    feedback.textContent = `${incidentId} hipotezi, ilgili ham alarm verisiyle yüklendi.`;
  } catch {
    feedback.textContent = "Ham veri yüklenemedi. Sunucunun çalıştığını kontrol edin.";
  }
});

load().catch(() => { document.getElementById("cards").textContent = "Demo verisi yüklenemedi."; });