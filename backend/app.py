
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_chatbot_response

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Multi-Turn AI Chatbot API is running!"
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data required"}), 400

        message = data.get("message")
        conversation_id = data.get("conversation_id")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        if not conversation_id:
            import uuid
            conversation_id = str(uuid.uuid4())

        response = get_chatbot_response(
            conversation_id,
            message
        )

        return jsonify({
            "conversation_id": conversation_id,
            "user_message": message,
            "response": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
