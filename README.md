# ORKG NLP API

REST API for the ORKG-NLP python [package](https://orkg-nlp-pypi.readthedocs.io/en/latest/).

This API provides an interface to the `orkgnlp`
[services](https://orkg-nlp-pypi.readthedocs.io/en/latest/services/services.html)
as well as for other services. For a full list please check our
[OpenAPI](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/-/blob/1-migrate-nlp-services-convert-pdf/openapi.json) specification

## Prerequisites

We require a python version `3.7` or above.

Requirement by service:

| Service              | Requirement(s)    |
|----------------------|-------------------|
| `/pdf/table/extract` | `Java 8` or above |
| `/pdf/covert`        | [`pdf2htmlEX`](https://github.com/pdf2htmlEX/pdf2htmlEX) |

## How to run

### With ``docker-compose``
```commandline
git clone https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api.git
cd orkg-nlp-api
docker-compose up -d
```

### Manually
```commandline
git clone https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api.git
cd orkg-nlp-api
pip install -r --upgrade requirements
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:4321
```
For local development you may run the web server using ``uvicorn`` with the ``--reload`` option:

```commandline
uvicorn app.main:app --host 0.0.0.0 --port 4321 --reload
```

## API Documentation
After successfully running the application, check the documentation at `localhost:4321/docs`
or `localhost:4321/redoc` (please adapt your `host:port` in case you configured them).
