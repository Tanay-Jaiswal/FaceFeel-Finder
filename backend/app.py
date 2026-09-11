import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from utils.facebook import extract_post_id, fetch_all_comments, FacebookAPIError
from utils.sentiment import summarize

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/")
def index():
    # render the HTML page
    return render_template("index.html")

@app.post("/fetch_comments")
def fetch_and_analyze():
    try:
        data = request.get_json(force=True, silent=False) or {}
        post_link = data.get("post_link", "").strip()
        if not post_link:
            return jsonify({"error": "No post link provided"}), 400
        post_id = extract_post_id(post_link)
        comments = fetch_all_comments(post_id)
        if not comments:
            return jsonify({"error": "No comments found"}), 404
        analysis = summarize(comments)
        return jsonify(analysis), 200
    except FacebookAPIError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

if __name__ == "__main__":
    # Dev server
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
