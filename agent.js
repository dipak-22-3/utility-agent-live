function utility(task) {
  return (task.impact * task.urgency) / (task.effort + task.risk);
}

function explain(task) {
  return `${task.name} selected because:
Impact (${task.impact}) × Urgency (${task.urgency})
is higher than Effort (${task.effort}) + Risk (${task.risk}).`;
}

function run() {
  const input = document.getElementById("input").value;
  let tasks;

  try {
    tasks = JSON.parse(input);
  } catch {
    alert("Invalid JSON input");
    return;
  }

  tasks = tasks.map(t => ({
    ...t,
    utility: Number(utility(t).toFixed(2))
  }));

  tasks.sort((a, b) => b.utility - a.utility);

  // Save memory
  localStorage.setItem("lastDecision", JSON.stringify(tasks));

  document.getElementById("output").textContent =
    tasks.map(t => `${t.name} → Utility: ${t.utility}`).join("\n");

  document.getElementById("explanation").textContent =
    explain(tasks[0]);
}

// Load memory on refresh
window.onload = () => {
  const memory = localStorage.getItem("lastDecision");
  if (memory) {
    document.getElementById("output").textContent =
      JSON.parse(memory).map(t => `${t.name} → Utility: ${t.utility}`).join("\n");
  }
};
