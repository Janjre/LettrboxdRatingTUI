import os
from textual_serve.server import Server

port = int(os.environ.get("PORT", 8000))
host = "0.0.0.0" if "PORT" in os.environ else "localhost"
public_url = os.environ.get("RENDER_EXTERNAL_URL")  # Render sets this automatically

server = Server(
    "python main.py",
    host=host,
    port=port,
    public_url=public_url
)
server.serve()

""" NOTES FOR NEXT TIME
- Use textual-serve not textual serve — the CLI is for local dev only. For any real deployment you need a serve.py using the Server class directly.
- Your serve.py needs three things for Render: host="0.0.0.0", port from the PORT env var, and public_url from RENDER_EXTERNAL_URL. All three are injected automatically by Render.
- Use "PORT" in os.environ to detect Render — it's more reliable than checking for the RENDER variable.
- textual-serve must be in requirements.txt — it's a separate package from textual and Render won't have it otherwise.
- The public_url parameter is the critical one — without it, textual-serve hardcodes http://0.0.0.0 into the page HTML, which breaks under HTTPS. This is what caused most of the pain here.
- Render's free tier sleeps after 15 minutes of inactivity — set up a free UptimeRobot monitor pinging your URL every 5 minutes if you want it always on.
"""