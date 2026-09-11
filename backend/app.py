import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from utils.facebook import extract_post_id, fetch_all_comments, FacebookAPIError, _get_access_token
from utils.sentiment import summarize

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)


def _demo_comments():
    return [
        {"message": "This is amazing and I love it!"},
        {"message": "So cool, I am excited to try it."},
        {"message": "This is really disappointing and frustrating."},
        {"message": "The vibe is okay, not great but fine."},
        {"message": "I hate how slow it feels."},
        {"message": "Looks good overall and super useful."},
        {"message": "Average experience, nothing special."},
        {"message": "Terrible design and poor quality."},
    ]


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
        demo_mode = bool(data.get("demo"))
        post_link = (data.get("post_link") or "").strip()

        if demo_mode:
            comments = _demo_comments()
            analysis = summarize(comments)
            analysis["demo"] = True
            return jsonify(analysis), 200

        if not post_link:
            return jsonify({"error": "No post link provided"}), 400

        try:
            _get_access_token()
        except FacebookAPIError:
            comments = _demo_comments()
            analysis = summarize(comments)
            analysis["demo"] = True
            return jsonify(analysis), 200

        post_id = extract_post_id(post_link)
        comments = fetch_all_comments(post_id)
        if not comments:
            return jsonify({"error": "No comments found"}), 404
        analysis = summarize(comments)
        return jsonify(analysis), 200
    except FacebookAPIError as e:
        message = str(e)
        status_code = 503 if "ACCESS_TOKEN" in message else 400
        return jsonify({"error": message}), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

if __name__ == "__main__":
    # Dev server
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
