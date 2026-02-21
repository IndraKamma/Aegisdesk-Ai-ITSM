const api = (path) => `${location.origin}${path}`;

let ALL_TICKETS = [];
let CURRENT_FILTER = "all"; // all | unsolved | solved

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, (m) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[m]));
}

function isSolvedStatus(status) {
  // backend may use "Resolved" or "Solved" depending on your model
  const s = String(status || "").toLowerCase();
  return s === "resolved" || s === "solved" || s === "closed";
}

function badge(status) {
  if (isSolvedStatus(status)) {
    return `<span class="badge solved">Solved</span>`;
  }
  return `<span class="badge open">Unsolved</span>`;
}

function renderCounts() {
  const all = ALL_TICKETS.length;
  const solved = ALL_TICKETS.filter(t => isSolvedStatus(t.status)).length;
  const unsolved = all - solved;

  const elAll = document.getElementById("countAll");
  const elSolved = document.getElementById("countSolved");
  const elUnsolved = document.getElementById("countUnsolved");

  if (elAll) elAll.textContent = all;
  if (elSolved) elSolved.textContent = solved;
  if (elUnsolved) elUnsolved.textContent = unsolved;
}

function applyFilter(list) {
  if (CURRENT_FILTER === "solved") return list.filter(t => isSolvedStatus(t.status));
  if (CURRENT_FILTER === "unsolved") return list.filter(t => !isSolvedStatus(t.status));
  return list;
}

function setActiveFilterButton() {
  const ids = ["filterAll", "filterUnsolved", "filterSolved"];
  ids.forEach(id => document.getElementById(id)?.classList.remove("active"));

  if (CURRENT_FILTER === "all") document.getElementById("filterAll")?.classList.add("active");
  if (CURRENT_FILTER === "unsolved") document.getElementById("filterUnsolved")?.classList.add("active");
  if (CURRENT_FILTER === "solved") document.getElementById("filterSolved")?.classList.add("active");
}

function row(t) {
  return `
    <tr>
      <td>#${t.id}</td>
      <td>${escapeHtml(t.title)}</td>
      <td>${badge(t.status)}</td>
      <td>${escapeHtml(t.assigned_to || "-")}</td>
      <td class="actions">
        ${
          isSolvedStatus(t.status)
            ? `<button class="btn secondary" disabled>Already Solved</button>`
            : `<button class="btn primary" onclick="markSolved(${t.id})">Mark as Solved</button>`
        }
      </td>
    </tr>
  `;
}

function renderTable() {
  const body = document.getElementById("ticketsBody");
  if (!body) return;

  const visible = applyFilter(ALL_TICKETS);

  if (!visible.length) {
    body.innerHTML = `<tr><td colspan="5" class="muted">No tickets in this view.</td></tr>`;
    return;
  }

  body.innerHTML = visible.map(row).join("");
  setActiveFilterButton();
}

async function refreshTickets() {
  const body = document.getElementById("ticketsBody");
  if (body) body.innerHTML = `<tr><td colspan="5" class="muted">Loading…</td></tr>`;

  const r = await fetch(api("/api/tickets"));
  ALL_TICKETS = await r.json();

  renderCounts();
  renderTable();
}

async function markSolved(id) {
  const technician = prompt("Technician name (example: Indra / Data Center Tech):");
  if (!technician) return;

  const r = await fetch(api(`/api/tickets/${id}`), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      status: "Resolved",         // keep your backend status
      assigned_to: technician
    })
  });

  await r.json(); // ignore output, just refresh
  await refreshTickets();
}

// Hook buttons
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btnRefresh")?.addEventListener("click", refreshTickets);

  document.getElementById("filterAll")?.addEventListener("click", () => {
    CURRENT_FILTER = "all";
    renderTable();
  });

  document.getElementById("filterUnsolved")?.addEventListener("click", () => {
    CURRENT_FILTER = "unsolved";
    renderTable();
  });

  document.getElementById("filterSolved")?.addEventListener("click", () => {
    CURRENT_FILTER = "solved";
    renderTable();
  });

  refreshTickets();
});