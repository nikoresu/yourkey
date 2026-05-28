import json
import uuid
from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from cryptography.fernet import Fernet

app = FastAPI()
templates = Jinja2Templates(directory="templates")

config = json.loads(Path("config.json").read_text())
max_allowed_views: int = config["max_allowed_views"]

key = Fernet.generate_key()
cipher = Fernet(key)

store: dict[str, tuple[bytes, int]] = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"max_allowed_views": max_allowed_views})


@app.post("/create")
async def create(request: Request, secret: str = Form(...), max_views: int = Form(..., ge=1, le=max_allowed_views)):
    secret_id = uuid.uuid4().hex
    encrypted = cipher.encrypt(secret.encode())
    store[secret_id] = (encrypted, max_views)
    link = str(request.base_url) + f"s/{secret_id}"
    return templates.TemplateResponse(request, "link.html", {"link": link})


@app.get("/s/{secret_id}", response_class=HTMLResponse)
async def reveal(secret_id: str, request: Request):
    entry = store.get(secret_id)
    if entry is None:
        return RedirectResponse(url="/")
    encrypted, remaining = entry
    if remaining <= 1:
        del store[secret_id]
    else:
        store[secret_id] = (encrypted, remaining - 1)
    plaintext = cipher.decrypt(encrypted).decode()
    return templates.TemplateResponse(request, "secret.html", {"secret": plaintext})


def start():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
