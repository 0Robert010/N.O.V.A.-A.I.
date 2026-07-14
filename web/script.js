const memoryCount = document.getElementById('memory-count');
const metricKnowledge = document.getElementById('metric-knowledge');
const metricCategories = document.getElementById('metric-categories');
const metricLast = document.getElementById('metric-last');
const metricTime = document.getElementById('metric-time');
const activityLog = document.getElementById('activity-log');
const canvas = document.getElementById('stats-chart');
const runLearningButton = document.getElementById('run-learning');

async function loadStats() {
  const response = await fetch('/stats');
  const data = await response.json();

  if (memoryCount) memoryCount.textContent = data.knowledge_count ?? 0;
  if (metricKnowledge) metricKnowledge.textContent = data.knowledge_count ?? 0;
  if (metricCategories) metricCategories.textContent = (data.categories || []).length;
  if (metricLast) metricLast.textContent = data.last_learning || 'Sem atividade';
  if (metricTime) metricTime.textContent = `${data.learning_time_seconds || 0}s`;

  if (activityLog && data.knowledge_count > 0) {
    const line = document.createElement('div');
    line.className = 'line';
    line.textContent = `[${new Date().toLocaleTimeString()}] Memória atualizada com sucesso.`;
    activityLog.appendChild(line);
  }

  renderChart(data);
}

function renderChart(data) {
  if (!canvas) return;
  const context = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  context.clearRect(0, 0, width, height);

  context.strokeStyle = 'rgba(66, 245, 255, 0.25)';
  context.lineWidth = 1;
  for (let index = 0; index <= 4; index += 1) {
    const y = 20 + index * 32;
    context.beginPath();
    context.moveTo(20, y);
    context.lineTo(width - 20, y);
    context.stroke();
  }

  const value = Math.min(140, (data.knowledge_count || 0) * 8 + 20);
  context.strokeStyle = '#42f5ff';
  context.lineWidth = 3;
  context.beginPath();
  context.moveTo(20, height - 20);
  context.lineTo(80, height - 40);
  context.lineTo(140, height - 80);
  context.lineTo(200, height - 60);
  context.lineTo(260, height - 20);
  context.lineTo(300, height - 90);
  context.stroke();

  context.fillStyle = '#ff4fd8';
  context.fillRect(20, height - 20, 8, -value + 20);
}

async function runLearningCycle() {
  if (!runLearningButton) return;
  runLearningButton.disabled = true;
  runLearningButton.textContent = 'Processando...';

  const response = await fetch('/learning/run', { method: 'POST' });
  const data = await response.json();
  if (activityLog) {
    const line = document.createElement('div');
    line.className = 'line';
    line.textContent = `[${new Date().toLocaleTimeString()}] ${data.status}: ${data.processed_count} arquivo(s) processado(s).`;
    activityLog.appendChild(line);
  }

  await loadStats();
  runLearningButton.disabled = false;
  runLearningButton.textContent = 'Executar ciclo de aprendizado';
}

runLearningButton?.addEventListener('click', runLearningCycle);
loadStats();
