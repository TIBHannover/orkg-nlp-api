import os

from fastapi import FastAPI

from app.common.util import io
from app.routers import clustering, annotation, pdf


def create_app():
    app = FastAPI(title='ORKG-NLP-API')

    _configure_app(app)
    _save_openapi_specification(app)

    return app


def _configure_app(app):
    app.include_router(clustering.router)
    app.include_router(annotation.router)
    app.include_router(pdf.router)


def _save_openapi_specification(app):
    app_dir = os.path.dirname(os.path.realpath(__file__))
    io.write_json(app.openapi(), os.path.join(app_dir, '..', 'openapi.json'))
