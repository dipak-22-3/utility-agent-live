function utility(task) {
  return (task.impact * task.urgency) / (task.effort + task.risk);
}

function runAgent(tasks) {
  return tasks
    .map(task => ({
      ...task,
      utility: Number(utility(task).toFixed(2))
    }))
    .sort((a, b) => b.utility - a.utility);
}
function explain(task) {
  return `${task.name} prioritized because impact (${task.impact}) × urgency (${task.urgency}) 
          outweighs effort (${task.effort}) + risk (${task.risk}).`;
}

