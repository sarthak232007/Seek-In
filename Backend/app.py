

from flask import Flask, request, jsonify
from flask_cors import CORS

from obfuscation import fake_to_real
from nl_to_sql import generate_sql_from_question
from validator import is_query_safe
from db import run_query
from insight_generator import generate_insight

app = Flask(__name__)
CORS(app)  


@app.route("/ask", methods=["POST"])
def ask():
    """
    Main endpoint. Frontend sends a JSON body like:
    { "question": "Show me customers from Lucknow" }

    We return a JSON response like:
    { "success": true, "answer": "...", "sql": "...", "rows": [...] }
    """

    data = request.json
    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({"success": False, "error": "No question provided."}), 400


    try:
        fake_sql = generate_sql_from_question(user_question)
    except Exception as e:
        error_text = str(e)
        if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
            return jsonify({
                "success": False,
                "error": "AI service is temporarily rate-limited (free tier daily limit reached). Please wait a few minutes and try again."
            }), 429
        return jsonify({"success": False, "error": f"AI error: {error_text}"}), 500

    
    real_sql = fake_to_real(fake_sql)

   
    safe, reason = is_query_safe(real_sql)
    if not safe:
        return jsonify({
            "success": False,
            "error": f"Query blocked for safety: {reason}",
            "sql": real_sql
        }), 400

    
    try:
        rows = run_query(real_sql)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}",
            "sql": real_sql
        }), 500

    
    try:
        answer = generate_insight(user_question, rows)
    except Exception as e:
        error_text = str(e)
        if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
            
            answer = f"(AI summary temporarily unavailable due to rate limit) Raw results: {rows}"
        else:
            answer = f"Could not generate a summary: {error_text}"

    return jsonify({
        "success": True,
        "answer": answer,
        "sql": real_sql,
        "rows": rows
    })


@app.route("/", methods=["GET"])
def health_check():
    """Simple route to confirm the server is running."""
    return jsonify({"status": "Seek-IN backend is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)