# app_factory.py or main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from base.utils.constant import constant

SECRET_KEY = constant.SECRET_KEY


def get_app() -> FastAPI:
    app = FastAPI(
        title="My Foreign Job",
        description="This is a custom Swagger UI for my API.",
        version="1.0.0",
    )
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    return app
