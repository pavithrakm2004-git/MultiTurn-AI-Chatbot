# MultiTurn AI Chatbot

A multi-turn AI chatbot built using Python, Flask, and the Google Gemini API. The chatbot maintains conversation history, allowing users to ask follow-up questions and receive context-aware responses.

## Features

- **Gemini API Integration:** Uses Google Gemini to generate AI responses.
- **Multi-Turn Conversations:** Maintains conversation history using unique conversation IDs.
- **Context Window Management:** Keeps the most recent 20 messages to manage the context sent to the LLM.
- **Persistent Storage:** Saves conversation history locally in a JSON file.
- **System Prompt:** Uses a defined AI assistant personality called LearnMate.
- **Error Handling:** Handles API errors and connection failures.
- **Web Interface:** Provides a simple chat interface using HTML, CSS, and JavaScript.
- **Environment Variables:** Stores the Gemini API key securely using a `.env` file.

## Technologies Used

- Python
- Flask
- Google Gemini API
- HTML
- CSS
- JavaScript
- JSON
- python-dotenv
- Flask-CORS

## Project Structure

```text
MultiTurn-AI-Chatbot/
│
├── backend/
│   ├── app.py
│   ├── chatbot.py
│  
│
├── frontend/
│   └── index.html
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/pavithrakm2004-git/MultiTurn-AI-Chatbot.git
```

### 2. Navigate to the project directory

```bash
cd MultiTurn-AI-Chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key.

**Important:** Never upload your `.env` file or expose your API key on GitHub.

### 7. Run the backend

From the project root directory:

```bash
python backend/app.py
```

The Flask backend will run at:

`http://127.0.0.1:5000`

### 8. Open the chatbot interface

Open `frontend/index.html` in your web browser while the Flask backend is running.

## API Endpoint

### POST `/chat`

Accepts a user message and conversation ID and returns an AI-generated response.

**Example request:**

```json
{
    "message": "Explain machine learning",
    "conversation_id": "conversation-001"
}
```

**Example response:**

```json
{
    "conversation_id": "conversation-001",
    "user_message": "Explain machine learning",
    "response": "Machine learning is a branch of AI..."
}
```

If a conversation ID is not provided, the backend generates a new one.

## Conversation and Context Management

The chatbot maintains a separate conversation history for each conversation ID.

For every new message:

1. The user's message is added to the conversation history.
2. The recent conversation messages are sent to Gemini.
3. Gemini generates a response using the available context.
4. The assistant's response is added to the history.
5. The updated history is saved in `backend/conversations.json`.

To manage the context window, the chatbot retains up to 20 recent messages rather than sending unlimited conversation history.

## Testing

The chatbot was tested for:

- Successful Gemini API communication.
- Multi-turn conversation memory.
- Follow-up questions referring to earlier messages.
- Separate conversation histories using different conversation IDs.
- Conversation history persistence after restarting the backend.
- Context window management.

## Future Improvements

- Token-based context window management.
- Conversation summarisation for older messages.
- Improved conversation storage using a database.
- Deployment for public access.

## Author

Developed as an internship project to demonstrate multi-turn conversational AI, LLM API integration, backend development, and context window management.