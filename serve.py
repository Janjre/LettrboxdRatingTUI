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