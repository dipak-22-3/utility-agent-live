// ===== Persistent Weights =====
let weights = JSON.parse(localStorage.getItem("weights")) || {
  impact: 1,
  urgency: 1,
  effort: 1,
  risk: 1
};

function saveWeights() {
  localStorage.setItem("weights", JSON.stringify(weights));
}

// ===== Utility Function (Adaptive) =====
function utility(task) {
  return (
    (weights.impact * task.impact +
      weights.urgency * task.urgency) /
    (weights.effort * task.effort +
      weights.risk * task.risk)
  );
}

// ===== Explanation =====
function explain(task) {
  return `${task.name} chosen because weighted impact (${weights.impact}) 
and urgency (${weights.urgency}) outweigh weighted effort (${weights.effort}) 
and risk (${weights.risk}).`;
}

// ===== Run Agent =====
function run() {
  let tasks;
  try {
    tasks = JSON.parse(document.getElementById("input").value);
  } catch {
    alert("Invalid JSON");
    return;
  }

  tasks = tasks.map(t => ({
    ...t,
    utility: Number(utility(t).toFixed(2))
  }));

  tasks.sort((a, b) => b.utility - a.utility);

  localStorage.setItem("lastDecision", JSON.stringify(tasks));

  document.getElementById("output").textContent =
    tasks.map(t => `${t.name} → Utility: ${t.utility}`).join("\n");

  document.getElementById("explanation").textContent =
    explain(tasks[0]);
}

// ===== Feedback Learning =====
function feedback(type) {
  if (type === "good") {
    weights.impact += 0.1;
    weights.urgency += 0.1;
  } else {
    weights.effort += 0.1;
    weights.risk += 0.1;
  }
  saveWeights();
  alert("Agent learned from feedback");
}

// ===== Load Memory =====
window.onload = () => {
  const memory = localStorage.getItem("lastDecision");
  if (memory) {
    document.getElementById("output").textContent =
      JSON.parse(memory)
        .map(t => `${t.name} → Utility: ${t.utility}`)
        .join("\n");
  }
};
