FROM python:3.7 as requirements-stage
LABEL maintainer="Omar Arab Oghli <Omar.ArabOghli@tib.eu>"

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Splitting in two stages gets rid of poetry, as for now, since it's not required for the application itself.
FROM python:3.7
LABEL maintainer="Omar Arab Oghli <Omar.ArabOghli@tib.eu>"

# Set the locale needed for onnxruntime
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

WORKDIR /orkg-nlp-api

COPY --from=requirements-stage /tmp/requirements.txt /orkg-nlp-api/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /orkg-nlp-api/requirements.txt

COPY ./app /orkg-nlp-api/app

# TODO: how many workers can we offer ?
CMD ["gunicorn", "app.main:app", "--workers", "4",  "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:4321"]