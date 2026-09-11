import os
import requests
from typing import Dict, List

class FacebookAPIError(RuntimeError):
    pass

def _get_access_token() -> str:
    token = (os.getenv("ACCESS_TOKEN", "") or "").strip()
    if not token or token == "REPLACE_ME":
        raise FacebookAPIError("ACCESS_TOKEN not set. Put it in .env or environment.")
    return token

def _get_graph_api_url() -> str:
    env_url = os.getenv("FB_API_URL") or os.getenv("API_URL")
    if env_url:
        return env_url.rstrip("/")
    api_version = (os.getenv("FB_API_VERSION") or "v21.0").strip("/")
    return f"https://graph.facebook.com/{api_version}"

def extract_post_id(url: str) -> str:
    """
    Handles common FB URL shapes.
    """
    if not url:
        raise ValueError("Empty post URL")
    u = url.strip()
    if "story_fbid=" in u:
        # ?story_fbid=<id>&id=<pageid>
        return u.split("story_fbid=")[1].split("&")[0]
    if "/posts/" in u:
        return u.split("/posts/")[1].split("/")[0]
    # permalink.php?story_fbid=... handled above;
    # fallback to last segment
    return u.strip("/").split("/")[-1]

def fetch_all_comments(post_id: str, fields: str = "message", limit: int = 100) -> List[Dict]:
    """
    Graph API paging loop to collect all comments for a post.
    """
    token = _get_access_token()
    api_base = _get_graph_api_url()
    url = f"{api_base}/{post_id}/comments"
    params = {"access_token": token, "limit": limit, "fields": fields}
    out: List[Dict] = []
    while True:
        r = requests.get(url, params=params, timeout=20)
        if r.status_code != 200:
            try:
                err = r.json().get("error", {})
            except Exception:
                err = {"message": r.text}
            raise FacebookAPIError(f"Graph API error: {err}")
        data = r.json() or {}
        out.extend(data.get("data", []))
        paging = data.get("paging", {})
        next_url = paging.get("next")
        if not next_url:
            break
        # for next hops, we pass full URL (already carries token)
        url = next_url
        params = {}  # token and limit embedded in next
    return out
