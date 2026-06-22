
const heroScreen = document.getElementById("hero-screen");
const chatScreen = document.getElementById("chat-screen");
const startBtn = document.getElementById("start-btn");

startBtn.addEventListener("click", () => {
  heroScreen.classList.add("hidden");
  chatScreen.classList.remove("hidden");
  
  document.getElementById("question-input").focus();
});



const chatBox = document.getElementById("chat-box");
const input = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");


const BACKEND_URL = "http://127.0.0.1:5000/ask";

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "message " + (sender === "user" ? "user-message" : "bot-message");
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}


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