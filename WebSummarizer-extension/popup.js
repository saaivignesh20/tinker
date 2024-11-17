const chatLog = document.getElementById("chat-log");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

const apiKey = "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";
const model = "gemma2-9b-it";
const memory = [];
const maxTurns = 5;

function addMessage(role, content) {
  memory.push({ role, content });
  if (memory.length > maxTurns * 2) memory.splice(0, memory.length - maxTurns * 2);
}

async function chatWithMemory(userInput) {
  addMessage("user", userInput);

  const messages = [
    { role: "system", content: "You are a helpful assistant with memory of the conversation." },
    ...memory
  ];

  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        messages,
        model,
        temperature: 0.7,
        max_tokens: 1000
      })
    });

    const data = await response.json();
    const assistantResponse = data.choices[0].message.content;

    addMessage("assistant", assistantResponse);
    displayMessage("assistant", assistantResponse);
  } catch (error) {
    displayMessage("assistant", "Error: Unable to process the request.");
    console.error(error);
  }
}

function displayMessage(role, content) {
  const messageDiv = document.createElement("div");
  messageDiv.textContent = `${role === "user" ? "You" : "Assistant"}: ${content}`;
  chatLog.appendChild(messageDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
}

sendBtn.addEventListener("click", () => {
  const userInput = chatInput.value.trim();
  if (userInput) {
    displayMessage("user", userInput);
    chatInput.value = "";
    chatWithMemory(userInput);
  }
});
