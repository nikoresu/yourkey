# Secret Share

Share one-time secrets via encrypted, expiring links.

## Dependencies

| Package | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Uvicorn](https://uvicorn.dev/) | ASGI server |
| [Jinja2](https://jinja.palletsprojects.com/) | Template engine |
| [Cryptography](https://cryptography.io/) | Fernet (AES-128-CBC + HMAC-SHA256) encryption |
| [python-multipart](https://github.com/andrew-d/python-multipart) | Form data parsing |
| [HTMX](https://htmx.org/) | Frontend interactivity (loaded from CDN) |

Managed via [uv](https://docs.astral.sh/uv/).

## Usage

```bash
# install dependencies
uv sync

# run the server
uv run uvicorn main:app --reload
```

Open http://localhost:8000. Secrets are stored encrypted in memory and
auto-deleted after being viewed the configured number of times.
