ARG VERSION=3.10.0-slim

FROM python:$VERSION as python-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \  
  && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat \  
  && rm -rf /var/lib/apt/lists/*

# create separate user as good practice to avoid using root user
RUN adduser app --home /home/app --shell /bin/bash --disabled-password
USER app
WORKDIR /home/app

# install python project dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# dev stage
FROM python-base as dev

USER app

# Expect project to be volume mounts for local development
ENTRYPOINT ["bin/entrypoint.sh"]
CMD ["python", "src/main.py"]

# build stage
FROM python-base as build

USER app

RUN chmod +x bin/*.sh

COPY --chown=app:app . .

ENTRYPOINT ["bin/entrypoint.sh"]
CMD ["python", "src/main.py"]