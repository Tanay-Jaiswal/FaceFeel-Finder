# FeelFinder — Facebook Comment Emotion Analyzer

A lightweight Flask app that analyzes Facebook post comments and summarizes their overall emotional tone.

Features:
- Accepts a Facebook post URL
- Extracts the post ID
- Fetches comments via the Facebook Graph API with pagination
- Runs a simple sentiment pass on comment text
- Shows a pie chart and overall emotion summary
- Includes a local demo mode for testing without a real token

This project is designed as a local demo/prototype and is best used with a valid Facebook access token when testing real public posts. The app includes a sample demo mode so it can be tested without live API access.

---

## 1) Quickstart (Local)

Requirements: Python 3.10+

```bash
cd backend
python -m venv .venv

# macOS/Linux:
source ./.venv/bin/activate
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# configure environment
copy .env.example .env
# or: cp .env.example .env
# then add your ACCESS_TOKEN if you want live Facebook analysis

# run the app
python app.py
# open http://localhost:5000
```

You can also test the app without a token by clicking the Demo Data button in the UI.

---

## 2) Environment Variables

Create `backend/.env`:

```env
ACCESS_TOKEN=REPLACE_ME
FB_API_VERSION=v21.0
FLASK_ENV=development
```

Notes:
- `ACCESS_TOKEN` is optional for the demo mode
- For live analysis, use a valid Facebook Page or user token with proper permissions
- The token must be authorized to access the Facebook post you are testing

---

## 3) Demo Mode

This app includes a built-in sample dataset so you can test the interface locally without a Facebook token.

Use the Demo Data button in the browser to:
- validate the UI flow
- test the chart rendering
- check the overall sentiment summary
- keep the project working while you polish it locally

---

## 4) Notes on Tokens & Permissions

- Tokens can expire or have limited permissions
- Public posts are easiest to test with a valid token
- Respect Facebook rate limits and platform terms of service
- Never commit your real access token to GitHub or any public repo

---

## 5) Docker (Optional)

```bash
# build
docker build -t feelfinder:latest ./backend

# run
docker run --rm -p 5000:5000 --env-file backend/.env feelfinder:latest
```

---

## 6) Deployment Notes

- Use `gunicorn` for production-style serving
- Store `ACCESS_TOKEN` in a local environment or secret manager
- If behind a proxy, configure `X-Forwarded-*` headers or `--forwarded-allow-ips=*`

---

## 7) Acknowledgements

This project is a lightweight demo inspired by the original project brief and is intended for local experimentation and learning.
