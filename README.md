# YouTube-AI-Chat-Extension
This Chrome extension allows users to ask questions about a YouTube video they are watching. It leverages a FastAPI backend to fetch the video's transcript and interact with a language model to provide meaningful answers based on the content of the video.

Steps to set-up the extension:
1. Clone the repository
2. Start the FastAPI backend server:
      Ensure you have pip and python installed. Create your virtual environment and activate it and use pip install -r requirements.txt to install the requirements.
      Make sure you have upadated all the variables in main.py.
      Run the FastAPI server: uvicorn main:app --reload.
      The API will be accessible at http://127.0.0.1:8000.
3. Load the extension into Chrome:
    Open Chrome and go to chrome://extensions/.
    Enable "Developer mode" in the top-right corner.
    Click "Load unpacked" and select the extension's directory.
