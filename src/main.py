import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import routes


def setup_settings(app: FastAPI) -> None:
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def start_application() -> FastAPI:
    app = FastAPI(title="SHIFT", version="0.1.1")

    setup_settings(app)

    app.include_router(router=routes)

    return app


app: FastAPI = start_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)