# ORKG NLP API

[![pipeline status](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/badges/main/pipeline.svg)](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/-/commits/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

REST API for the ORKG-NLP python [package](https://orkg-nlp-pypi.readthedocs.io/en/latest/).

This API provides an interface to the `orkgnlp`
[services](https://orkg-nlp-pypi.readthedocs.io/en/latest/services/services.html)
as well as for other services. For a full list please check our
[OpenAPI](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/-/blob/1-migrate-nlp-services-convert-pdf/openapi.json) specification

## Prerequisites

We require a python version `3.8` or above.
We also require a database connection, whose URI can be specified in the ``.env`` file.

Requirement by service:

| Service                    | Requirement(s)                                           |
|----------------------------|----------------------------------------------------------|
| `/tools/pdf/table/extract` | `Java 8` or above                                        |
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

| Variable                                      | Description                                                                                                                                                                                                                         |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ORKG_NLP_API_PREFIX                           | Prefix of the app routes. Not preferable in development environment                                                                                                                                                                 |
| ORKG_NLP_API_DEACTIVATE_FORCE_DOWNLOAD_MODELS | Models will always be force-downloaded when the app starts unless this variable is provided. Its value does not matter. Please do not provide the value in production, since it's recommended to freshly download all models again. |
| SQLALCHEMY_DATABASE_URI                       | Used to connect to the database (currently we use PostgreSQL).                                                                                                                                                                      |
| ENV                                           | Deployment environment. Possible values: [dev, test, prod]                                                                                                                                                                          |
| POSTGRES_USER                                 | Used by docker-compose to set the user of PostgreSQL image                                                                                                                                                                          |
| POSTGRES_PASSWORD                             | Used by docker-compose to set the password of PostgreSQL image                                                                                                                                                                      |
| POSTGRES_DB                                   | Used by docker-compose to set the database name of PostgreSQL image                                                                                                                                                                 |
| LOG_LEVEL                                     | Used for the Logger. Possible values: [INFO, WARN, DEBUG, ERROR]. Defaults to DEBUG                                                                                                                                                 |
| ORKG_BACKEND_HOST                             | The ORKG backend host. Default value set to the Sandbox host. Should be adjusted accourding to usecase                                                                                                                              |

## Contributors

As an `orkgnlp` services API, numerous individuals have contributed to the development of the code, ranging from single lines to extensive sections. We would like to express our deepest gratitude to the following individuals for their exceptional contributions:
- **[Hamed Babaei Giglou](https://github.com/HamedBabaei) - `Current Maintainer`**
- **[Omar Arab Oghli](https://github.com/omar-araboghli)** - `Main Creator`
- **[Yaser Jaradeh](https://gitlab.com/YaserJaradeh)** - `Contributor`
- **[Manuel Prinz](https://gitlab.com/mprinz)** - `Contributor`
- **[Quentin Münch](https://gitlab.com/QuentinBot)** - `Contributor`

Their dedication and expertise have significantly enriched the codebase, and we are truly grateful for their invaluable contributions.

## License
[MIT](./LICENSE)
