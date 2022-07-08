# ORKG NLP API

[![pipeline status](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/badges/main/pipeline.svg)](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/-/commits/main)

REST API for the ORKG-NLP python [package](https://orkg-nlp-pypi.readthedocs.io/en/latest/).

This API provides an interface to the `orkgnlp`
[services](https://orkg-nlp-pypi.readthedocs.io/en/latest/services/services.html)
as well as for other services. For a full list please check our
[OpenAPI](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/-/blob/1-migrate-nlp-services-convert-pdf/openapi.json) specification

## Prerequisites

We require a python version `3.7` or above.
We also require a database connection, whose URI can be specified in the ``.env`` file. 

Requirement by service:

| Service                    | Requirement(s)    |
|----------------------------|-------------------|
| `/tools/pdf/table/extract` | `Java 8` or above |
| `/tools/pdf/covert`        | [`pdf2htmlEX`](https://github.com/pdf2htmlEX/pdf2htmlEX) |

## How to run

### With ``docker-compose``

```commandline
git clone https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api.git
cd orkg-nlp-api
```

create a file called `.env` and define the needed environment variables.
Please use `.env.example` as an example. Then run:

```commandline
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


## Environment Variables
The following environment variables can be used inside the docker container
and are defined in the `.env` file.

| Variable                | Description                                                                         |
|-------------------------|-------------------------------------------------------------------------------------|
| ORKG_NLP_API_PREFIX     | Prefix of the app routes. Not preferable in development environment                 |
| SQLALCHEMY_DATABASE_URI | Used to connect to the database (currently we use PostgreSQL).                      |
| ENV                     | Deployment environment. Possible values: [dev, test, prod]                          |
| POSTGRES_USER           | Used by docker-compose to set the user of PostgreSQL image                          |                                                                     |
| POSTGRES_PASSWORD       | Used by docker-compose to set the password of PostgreSQL image                      |                                                                    |
| POSTGRES_DB             | Used by docker-compose to set the database name of PostgreSQL image                 |
| LOG_LEVEL               | Used for the Logger. Possible values: [INFO, WARN, DEBUG, ERROR]. Defaults to DEBUG |