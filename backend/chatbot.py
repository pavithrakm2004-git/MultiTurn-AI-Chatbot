
import os
import json
import urllib.request
import urllib.error
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.8-flash"

MAX_HISTORY_MESSAGES = 20

# Persistent conversation storage
STORAGE_FILE = os.path.join(
    os.path.dirname(__file__),
    "conversations.json"
)

def load_conversations():
    if not os.path.exists(STORAGE_FILE):
        return {}

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

def save_conversations(conversations):
    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(conversations, file, indent=4, ensure_ascii=False)

# Load existing conversations when the backend starts
conversations = load_conversations()

def get_chatbot_response(conversation_id, user_message):

    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    if conversation_id not in conversations:
        conversations[conversation_id] = []

    history = conversations[conversation_id] + [
        {
            "role": "user",
            "parts": [{"text": user_message}]
        }
    ]

    # Keep recent messages without starting with an incomplete assistant turn
    if len(history) > MAX_HISTORY_MESSAGES:
        history = history[-MAX_HISTORY_MESSAGES:]

        if history[0]["role"] == "model":
            history = history[1:]

    payload = {
        "system_instruction": {
    "parts": [
        {
            "text": """
You are LearnMate, a friendly and intelligent AI learning assistant.

Your purpose is to help users understand concepts, solve problems,
learn new skills, and get clear answers to their questions.

Follow these guidelines:

1. Explain complex topics in simple, beginner-friendly language.
2. Provide accurate, relevant, and well-structured answers.
3. Use examples when they help users understand a concept.
4. Maintain awareness of the conversation history provided to you.
5. Use relevant information from earlier messages when answering follow-up questions.
6. If a question is unclear, ask the user for clarification.
7. Never invent facts or pretend to know information that is unavailable.
8. Keep answers concise unless the user requests a detailed explanation.
9. Maintain a friendly, respectful, and supportive tone.

Your main goal is to make learning easier and provide useful,
reliable assistance in every conversation.
"""
        }
    ]
},
        "contents": history,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{MODEL}:generateContent?"
        f"key={urllib.parse.quote(API_KEY, safe='')}"
    )

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        assistant_message = result["candidates"][0]["content"]["parts"][0]["text"]

        history.append({
            "role": "model",
            "parts": [{"text": assistant_message}]
        })

        # Save conversation in memory and in JSON file
        conversations[conversation_id] = history
        save_conversations(conversations)

        return assistant_message

    except urllib.error.HTTPError as e:
        error_details = e.read().decode("utf-8")
        raise Exception(f"Gemini API Error: {error_details}")

    except urllib.error.URLError as e:
        raise Exception(f"Connection Error: {e.reason}")
