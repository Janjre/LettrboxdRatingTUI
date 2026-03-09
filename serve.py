import os
from textual_serve.server import Server

server = Server(
    "python main.py",
    host="localhost",
    port=int(os.environ.get("PORT", 8000))
)
server.serve()

