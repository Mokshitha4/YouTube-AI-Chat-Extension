document.getElementById("send").addEventListener("click", async () => {
    const input = document.getElementById("input").value;
    if (!input) return;
  
    const chat = document.getElementById("chat");
    chat.innerHTML += `<div class="userQn">You: ${input}</div>`;
    document.getElementById("input").value=""
    const port = chrome.runtime.connect({name: "YtGpt"})
    port.postMessage(input);
    port.onMessage.addListener(function(msg) {
      chat.innerHTML += `<div class="AiAns">AI: ${msg}</div>`;
    });

  });
  