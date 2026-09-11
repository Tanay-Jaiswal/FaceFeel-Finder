# FeelFinder

FeelFinder is a lightweight local demo app for analyzing Facebook post comments and summarizing their emotional tone.

It accepts a Facebook post URL, extracts the post ID, fetches comments through the Facebook Graph API, and classifies each comment as positive, negative, or neutral. The project includes a demo mode for local testing without live API access, which makes it easier to explore the app and refine the user experience without needing a token.

## Features
- Paste a Facebook post URL
- Extract the post ID from the URL
- Fetch comments via the Facebook Graph API
- Classify comments as positive, negative, or neutral
- Show a visual emotion distribution chart
- Include a demo mode for local testing

## Tech Stack
- Python
- Flask
- Requests
- Chart.js

## Local Setup

Requirements:
- Python 3.10+

```bash
cd backend
python -m venv .venv

# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt

# create the environment file
copy .env.example .env
# or: cp .env.example .env

# edit backend/.env if you want live Facebook analysis
python app.py
```

Then open:
- http://localhost:5000

## Environment Variables

Create `backend/.env` with:

```env
ACCESS_TOKEN=YOUR_FACEBOOK_ACCESS_TOKEN
FB_API_VERSION=v21.0
FLASK_ENV=development
```

Notes:
- `ACCESS_TOKEN` is required for live Facebook analysis
- The app also includes a built-in demo dataset for local testing
- Keep your token local and do not commit it to GitHub

## Demo Mode

The app includes a built-in sample dataset so you can test the interface without a live Facebook token.

Use the “Use Demo Data” button in the browser to:
- validate the UI flow
- preview the chart and summary output
- test the app without external API access
- keep development local and safe

## Notes
- This project is a demo/prototype and not a production-grade sentiment engine
- Live Graph API requests depend on valid Facebook permissions and public post access
- Respect Facebook API limits and platform terms of service

## Docker (Optional)

```bash
# build
docker build -t feelfinder:latest ./backend

# run
docker run --rm -p 5000:5000 --env-file backend/.env feelfinder:latest
```

## Deployment Notes
- Use `gunicorn` for production-style serving
- Store access tokens in a secure environment or secret manager
- If behind a reverse proxy, configure forwarded headers appropriately

## Acknowledgements

This project is a lightweight local demo inspired by the original project brief and intended for learning, experimentation, and portfolio use.
