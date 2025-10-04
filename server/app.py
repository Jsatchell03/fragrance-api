import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from agent import agent_executor

load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("message", "")

    if not query:
        return jsonify({"reply": "⚠️ No input received."}), 400

    try:
        response = agent_executor.invoke({"query": query})
        return jsonify({"reply": response["output"]})
    except Exception as e:
        return jsonify({"reply": f"❌ Agent error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
