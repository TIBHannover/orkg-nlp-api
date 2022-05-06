# ORKG NLP API

REST API for the ORKG-NLP python [package](https://orkg-nlp-pypi.readthedocs.io/en/latest/).

## How to run

We require a python version `3.7` or above.

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

## API Documentation
After successfully running the application, check the documentation at `localhost:4321/docs`
or `localhost:4321/redoc` (please adapt your `host:port` in case you configured them).
