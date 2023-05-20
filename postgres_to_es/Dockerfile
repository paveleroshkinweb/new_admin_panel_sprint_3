ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION} as python-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \  
  && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat \  
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

RUN groupadd -r app \
  && useradd -d /app -r -g app app \
  && chown app:app -R /app


FROM python-base as dev

USER app

ENTRYPOINT ["bin/entrypoint.sh"]

CMD ["python", "src/main.py"]


FROM python-base as build

USER app

COPY --chown=app:app . .

RUN chmod +x bin/*.sh

ENTRYPOINT ["bin/entrypoint.sh"]

CMD ["python", "src/main.py"]
