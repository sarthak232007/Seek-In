// ============================================
// script.js
// Handles: switching from hero screen to chat screen,
// and sending questions to the Flask backend.
// ============================================

// ----- Screen switching -----
const heroScreen = document.getElementById("hero-screen");
const chatScreen = document.getElementById("chat-screen");
const startBtn = document.getElementById("start-btn");

startBtn.addEventListener("click", () => {
  heroScreen.classList.add("hidden");
  chatScreen.classList.remove("hidden");
  // Auto-focus the input so the user can start typing immediately
  document.getElementById("question-input").focus();
});


// ----- Chat logic (same as before, talks to Flask backend) -----
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");

// This is where your Flask backend runs locally.
const BACKEND_URL = "http://127.0.0.1:5000/ask";

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "message " + (sender === "user" ? "user-message" : "bot-message");
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

// Renders the bot's answer as a clean card (label + answer text)
// instead of a plain gray bubble -- looks more like an analytics
// tool's output, less like a generic chatbot reply.
function addAnswerCard(answerText) {
  const card = document.createElement("div");
  card.className = "answer-card";

  const label = document.createElement("p");
  label.className = "answer-card-label";
  label.textContent = "Answer";

  const text = document.createElement("p");
  text.className = "answer-card-text";
  text.textContent = answerText;

  card.appendChild(label);
  card.appendChild(text);
  chatBox.appendChild(card);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuestion() {
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";
  const thinkingMsg = addMessage("Thinking...", "bot");

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question })
    });

    const data = await response.json();

    // Remove the "Thinking..." message
    chatBox.removeChild(thinkingMsg);

    if (data.success) {
      addAnswerCard(data.answer);
    } else {
      addMessage("Error: " + data.error, "bot");
    }
  } catch (err) {
    chatBox.removeChild(thinkingMsg);
    addMessage("Could not reach the server. Is Flask running?", "bot");
  }
}

sendBtn.addEventListener("click", sendQuestion);
input.addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendQuestion();
});