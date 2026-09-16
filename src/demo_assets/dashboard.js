const statusLabels = { open: "Açık", in_progress: "Çalışılıyor", blocked: "Engelli", resolved: "Çözüldü" };
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

function renderCard(card) {
  const node = document.getElementById("card-template").content.firstElementChild.cloneNode(true);
  node.dataset.incidentId = card.incident_id;
  node.querySelector(".priority").textContent = card.priority;
  node.querySelector(".confidence").textContent = `${card.confidence} güven`;
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
  status.className = statusClass(card.action_status); status.textContent = statusLabels[card.action_status];
  return node;
}

function render() {
  const { input_alarm_count, incident_card_count, max_incident_cards, incident_cards, noise_summary, noise_total } = dashboard;
  setText("#processed-count", `${input_alarm_count}/${input_alarm_count}`);
  setText("#card-count", incident_card_count);
  setText("#card-cap", max_incident_cards);
  setText("#noise-count", noise_total.toLocaleString("tr-TR"));
  setText("#reduction", `%${((1 - incident_card_count / input_alarm_count) * 100).toFixed(1).replace(".", ",")}`);
  const cards = document.getElementById("cards"); cards.replaceChildren(...incident_cards.map(renderCard));
  const selection = document.getElementById("action-card"); selection.replaceChildren(...incident_cards.map(card => new Option(`${card.incident_id} · ${card.action_owner}`, card.incident_id)));
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

document.getElementById("update-action").addEventListener("click", async () => {
  const incidentId = document.getElementById("action-card").value;
  const status = document.getElementById("action-status").value;
  const feedback = document.getElementById("action-feedback");
  try {
    const response = await fetch(`/api/cards/${encodeURIComponent(incidentId)}/action`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status }) });
    if (!response.ok) throw new Error("Update failed");
    const result = await response.json();
    dashboard.incident_cards.find(card => card.incident_id === result.incident_id).action_status = result.action_status;
    render(); document.getElementById("action-card").value = incidentId;
    feedback.textContent = `${incidentId} aksiyonu “${statusLabels[result.action_status]}” durumuna alındı.`;
  } catch {
    feedback.textContent = "Durum güncellenemedi. Sunucunun çalıştığını kontrol edin.";
  }
});

load().catch(() => { document.getElementById("cards").textContent = "Demo verisi yüklenemedi."; });