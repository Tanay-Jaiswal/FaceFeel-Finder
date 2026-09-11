# FeelFinder — Facebook Comment Emotion Analyzer

A minimal end‑to‑end app that:
- Accepts a Facebook post URL
- Extracts the post ID
- Fetches **all** comments via Graph API (with paging)
- Runs a lightweight keyword‑based sentiment pass
- Shows a pie chart (Chart.js) of Positive / Negative / Neutral

> Drop in your Facebook Graph API token and it works.

---

## 1) Quickstart (Local)

**Requirements**: Python 3.10+

```bash
cd backend
python -m venv .venv
# macOS/Linux:
source ./.venv/bin/activate
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# configure environment
cp .env.example .env
# edit .env and set ACCESS_TOKEN=<your token>

# run
python app.py
# open http://localhost:5000
```

## 2) Environment

Create `backend/.env`:

```env
ACCESS_TOKEN=REPLACE_ME
FB_API_VERSION=v21.0
FLASK_ENV=production
```

> Use a **Page** access token or user token with proper permissions.
> For public posts, ensure the token has access to read comments for that object.

## 3) Notes on Tokens & Permissions

- User/Page tokens expire; consider long‑lived tokens for demos.
- Only public objects (or those your token is authorized for) can be queried.
- Respect rate limits and terms of service.

## 4) Docker (optional)

```bash
# build
docker build -t feelfinder:latest ./backend
# run
docker run --rm -p 5000:5000 --env-file backend/.env feelfinder:latest
```

## 5) Deploy Hints

- Use `gunicorn` (already in requirements) for production.
- Provide `ACCESS_TOKEN` as a secret/variable in your platform.
- If serving behind a proxy, set `X-Forwarded-*` headers or `--forwarded-allow-ips=*`.

## 6) Acknowledgements

This implementation follows the module breakdown and UI concept described in the provided project brief.
