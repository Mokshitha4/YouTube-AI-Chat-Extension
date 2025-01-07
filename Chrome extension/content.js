// content.js
console.log("Content script loaded on YouTube page.");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "getVideoId") {
    console.log("Received message to get video ID.");
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get("v");
    sendResponse({ videoId });
  }
  return true; // Required for asynchronous response
});
