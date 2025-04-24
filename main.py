from starlette.middleware.cors import CORSMiddleware

from app.app import make_app

_app = make_app()

app = CORSMiddleware(
    app=_app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


__all__ = [app]