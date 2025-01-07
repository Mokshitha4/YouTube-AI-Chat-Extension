from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain.chains import LLMChain
from youtube_transcript_api.formatters import TextFormatter

# Initialize FastAPI app
app = FastAPI()

origins = [
    "chrome-extension://enter yout extension origin here",  # extension's origin
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# LLM initialization 
llm = ChatOpenAI(
    endpoint="Your ENDPOINT",
    api_key='Your API key',
    api_version="Your version",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
)

# Pydantic models for request bodies
class QueryRequest(BaseModel):
    question: str
    transcript: str

class VideoIDRequest(BaseModel):
    video_id: str

# Endpoint to get the transcript from YouTube video ID (POST request)
@app.post("/transcript")
async def get_transcript(request: VideoIDRequest):
    try:
        print(request)
        video_id = request.video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
          
        # Format the transcript into plain text
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return {"transcript": formatted_transcript}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to handle the question and get the response from LLM
@app.post("/llm")
async def query_llm(request: QueryRequest):
    try:
        # Get the question and transcript
        question = request.question
        transcript = request.transcript

        # Format the system prompt
        system_prompt = f"""
        Role: You are a helpful assistant designed to answer questions based solely on the content of the video transcript provided below. Your responses must strictly adhere to the information contained in the transcript and avoid adding any external knowledge.

        Video Transcript: {transcript}

        Instructions:
        - Answer questions directly and concisely, using only the information provided in the transcript.
        - If a question cannot be answered based on the transcript, respond with: "The information is not available in the video."
        - Avoid speculation.
        """

        # Create a ChatPromptTemplate using the system prompt and user question
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Chain to process the prompt and get the response
        chain = prompt | llm
        agent_scratchpad = []  # Optional, can store intermediate results
        response = chain.invoke({"input": question, "agent_scratchpad": agent_scratchpad})
        print(response)
        return {"answer": response.content}
    except Exception as e:
        return {"error": str(e)}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
