import os
import json
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from starlette.middleware.cors import CORSMiddleware

from constants import FALLBACK_MESSAGE, MODEL_NAME, RESPONSE_MIME_TYPE, FALLBACK_RESPONSE, STATUS_NEEDS_CONTEXT, \
    STATUS_NOT_FOUND
from models import ChatRequest, LLMResponse
from utils import load_context_files, load_main_context_file

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

MAIN_CONTEXT = load_main_context_file()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_sessions = {}


def initial_prompt() -> str:
    return f"""
        You are an intelligent assistant helping investors understand the company based on internal data.
        
        You have access to the company's structure as described in the following context. Do not mention 'JSON', 'slides', or filenames to the user. Respond professionally and confidently as if you're part of Investor Relations.
        
        If you cannot answer with the current data:
        - Respond clearly that you need additional data.
        - Specify the required file(s) by name in the format: Germany.json, UK.json, etc.
        - Do not guess.
        
        If you still can't answer after receiving additional data, respond with:
        "{FALLBACK_MESSAGE}"
        
        Company structure:
        {json.dumps(MAIN_CONTEXT)}
    """


def get_or_create_chat_session(session_id: str) -> Any:
    if session_id not in chat_sessions:
        chat = client.chats.create(
            model=MODEL_NAME,
            config={
                "response_mime_type": RESPONSE_MIME_TYPE,
                "response_schema": LLMResponse,
            },
        )
        chat.send_message(initial_prompt())
        chat_sessions[session_id] = chat
    return chat_sessions[session_id]


def send_message_and_parse(chat_session: Any, prompt_text: str) -> LLMResponse | None:
    try:
        response = chat_session.send_message(prompt_text)
        return response.parsed
    except Exception as e:
        print(f"Error sending message or parsing response: {e}")
        return None


def handle_additional_context(chat_session: Any, requested_files: list) -> dict:
    extra_context = load_context_files(requested_files)
    if not extra_context:
        return FALLBACK_RESPONSE

    context_message = f"Here is additional context from {requested_files}:\n{json.dumps(extra_context)}. \n Answer the question now"
    parsed_response = send_message_and_parse(chat_session, context_message)

    if not parsed_response or parsed_response.status == STATUS_NOT_FOUND:
        return FALLBACK_RESPONSE

    return {"response": parsed_response.answer}


def process_chat_request(chat_session, prompt):
    parsed_response = send_message_and_parse(chat_session, prompt)

    if not parsed_response:
        return FALLBACK_RESPONSE

    if parsed_response.status == STATUS_NEEDS_CONTEXT:
        return handle_additional_context(chat_session, parsed_response.requested_files)

    if parsed_response.status == STATUS_NOT_FOUND:
        return FALLBACK_RESPONSE

    return {"response": parsed_response.answer}


@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    prompt = request.prompt

    chat_session = get_or_create_chat_session(session_id)

    return process_chat_request(chat_session, prompt)
