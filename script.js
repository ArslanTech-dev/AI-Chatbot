document.getElementById('chat-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('message');
  const message = input.value.trim();
  if (!message) return;

  appendMessage('user', message);
  input.value = '';

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    appendMessage('bot', data.reply);
  } catch (err) {
    appendMessage('bot', 'Error: Could not reach server.');
  }
});

function appendMessage(sender, text) {
  const box = document.getElementById('chat-box');
  const div = document.createElement('div');
  div.className = `message ${sender}`;
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}