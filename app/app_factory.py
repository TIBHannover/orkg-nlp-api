import os

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.errors import OrkgNlpApiError
from app.common.util import io
from app.db.connection import Base, engine
from app.routers import clustering, annotation, pdf, text, feedback

_registered_services = []


def create_app():
    app = FastAPI(
        title='ORKG-NLP-API',
        root_path=os.getenv('ORKG_NLP_API_PREFIX', ''),
    )

    _configure_app_routes(app)
    _configure_exception_handlers(app)
    _create_database_tables()
    _save_openapi_specification(app)

    return app


def _configure_app_routes(app):
    app.include_router(clustering.router)
    app.include_router(annotation.router)
    app.include_router(pdf.router, prefix='/tools')
    app.include_router(text.router, prefix='/tools')
    app.include_router(feedback.router)


def _configure_exception_handlers(app):

    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    async def orkg_nlp_api_exception_handler(request: Request, exc: OrkgNlpApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                'location': exc.class_name,
                'detail': exc.detail
            })
        )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(OrkgNlpApiError, orkg_nlp_api_exception_handler)


def _create_database_tables():
    if os.environ.get('ENV') != 'test':
        Base.metadata.create_all(bind=engine)


def _save_openapi_specification(app):
    app_dir = os.path.dirname(os.path.realpath(__file__))
    io.write_json(app.openapi(), os.path.join(app_dir, '..', 'openapi.json'))
