
chrome.runtime.onConnect.addListener(function(port) {
  port.onMessage.addListener(async function(message){
    if (message) {
      try {
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tabs.length === 0) {
          port.postMessage("No active tab found. Please open a YouTube video.");
        }
        const question= message
        const tab = tabs[0];
        if (!tab || !tab.id) {
          port.postMessage("Could not access the active tab. Please try again.");
        }

        const urlParams = new URLSearchParams(new URL(tab.url).search);
        const videoId= urlParams.get("v");
        console.log(videoId)
        // Fetch transcript and query LLM
        const transcript = await fetchTranscript(videoId);
        console.log(question, transcript);
        const answer = await queryLLM(question, transcript);
        port.postMessage(answer);
        console.log(answer)
      } catch (error) {
        console.error("Error in background script:", error);
        port.postMessage("An unexpected error occurred.");
      }

      return true; // Ensures async response works
    }
  });
});

  async function fetchTranscript(VideoId) {
    const response = await fetch("http://127.0.0.1:8000/transcript", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({video_id: VideoId }),
    });
    let data= await response.json()
    console.log(data)
    return  data.transcript;
  }
  
  async function queryLLM(Question, Transcript) {
    const response = await fetch("http://127.0.0.1:8000/llm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question:Question, transcript:Transcript }),
    });
    const data = await response.json();
    return data.answer;
  }
  