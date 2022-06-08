FROM python:3.7 as requirements-stage
LABEL maintainer="Omar Arab Oghli <Omar.ArabOghli@tib.eu>"

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Splitting in two stages gets rid of poetry, as for now, since it's not required for the application itself.
FROM ubuntu:bionic
LABEL maintainer="Omar Arab Oghli <Omar.ArabOghli@tib.eu>"

# Install java for ExtractTable
# Install python 3.7
# Register the python version in alternatives
# Set python 3.7 as the default python
# Upgrade pip to latest version
RUN apt-get clean && apt-get update && \
    apt-get -qqy install locales curl python3.7 python3.7-dev python3.7-distutils wget default-jre && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 && \
    update-alternatives --set python /usr/bin/python3.7 && \
    curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py

# Set the locale needed for onnxruntime
RUN apt-get install -y locales && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install pdf2htmlEX for ConvertPdf
RUN wget -O pdf2html.deb https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb && \
    apt-get -qqy install ./pdf2html.deb

WORKDIR /orkg-nlp-api

COPY --from=requirements-stage /tmp/requirements.txt /orkg-nlp-api/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /orkg-nlp-api/requirements.txt

COPY ./app /orkg-nlp-api/app

# TODO: how many workers can we offer ?
CMD ["gunicorn", "app.main:app", "--workers", "4",  "--timeout", "0", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:4321"]