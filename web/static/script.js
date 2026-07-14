const askForm = document.getElementById('ask-form');
const learnForm = document.getElementById('learn-form');
const chatLog = document.getElementById('chat-log');
const knowledgeCount = document.getElementById('knowledge-count');
const memoryList = document.getElementById('memory-list');

function appendBubble(text, role = 'nova') {
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function setLoadingState(isLoading) {
  const button = askForm?.querySelector('button');
  if (button) {
    button.disabled = isLoading;
    button.textContent = isLoading ? 'Pensando…' : 'Enviar';
  }
}

async function refreshMemory() {
  const response = await fetch('/memory');
  const concepts = await response.json();
  memoryList.innerHTML = '';

  if (!concepts.length) {
    memoryList.innerHTML = '<div class="memory-item">Ainda não há conhecimento salvo.</div>';
    return;
  }

  concepts.forEach((concept) => {
    const item = document.createElement('div');
    item.className = 'memory-item';
    item.innerHTML = `<strong>${concept.name}</strong><br>${concept.category} · confiança ${concept.confidence}`;
    memoryList.appendChild(item);
  });
}

refreshMemory();

askForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const input = document.getElementById('question-input');
  const question = input.value.trim();
  if (!question) return;

  appendBubble(question, 'user');
  input.value = '';
  setLoadingState(true);

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    appendBubble(data.answer || 'Sem resposta.', 'nova');
  } catch (error) {
    appendBubble('Não consegui responder neste momento.', 'nova');
  } finally {
    setLoadingState(false);
  }
});

learnForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(learnForm);
  const response = await fetch('/learn', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();
  if (data.success) {
    appendBubble('Novo conhecimento salvo com sucesso.', 'nova');
    learnForm.reset();
    await refreshMemory();
    const countResponse = await fetch('/memory');
    const memory = await countResponse.json();
    knowledgeCount.textContent = memory.length;
  } else {
    appendBubble(data.error || 'Não foi possível salvar.', 'nova');
  }
});
