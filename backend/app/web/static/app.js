const api = (path) => `${location.origin}${path}`;


function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, m => ({
    "&":"&amp;",
    "<":"&lt;",
    ">":"&gt;",
    '"':"&quot;",
    "'":"&#39;"
  }[m]));
}


function solvedBadge(status){

  if(status === "Resolved")
    return `<span class="badge solved">Solved</span>`;

  return `<span class="badge open">Unsolved</span>`;
}


function row(ticket){

return `
<tr>

<td>#${ticket.id}</td>

<td>${escapeHtml(ticket.title)}</td>

<td>${solvedBadge(ticket.status)}</td>

<td>${escapeHtml(ticket.assigned_to ?? "-")}</td>

<td>

<button class="btn secondary"
onclick="markSolved(${ticket.id})">
Mark Solved
</button>

</td>

</tr>
`;
}


async function refreshTickets(){

const body = document.getElementById("ticketsBody");

body.innerHTML =
`<tr><td colspan="5">Loading...</td></tr>`;


const r =
await fetch(api("/api/tickets"));

const tickets =
await r.json();


if(!tickets.length){

body.innerHTML =
`<tr><td colspan="5">No tickets</td></tr>`;

return;
}


body.innerHTML =
tickets.map(row).join("");

}


async function markSolved(id){

const technician =
prompt("Technician name:");

if(!technician) return;


await fetch(api(`/api/tickets/${id}`),{

method:"PATCH",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({

status:"Resolved",

assigned_to: technician

})

});


refreshTickets();

}


document.addEventListener(
"DOMContentLoaded",
refreshTickets
);