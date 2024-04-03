FROM python:3.11-slim-bullseye

ENV PATH="${PATH}:/root/.local/bin" \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_NO_CACHE_DIR=off \
  PORT=8000 \
  PYTHONDONTWRITEBYTECODE=1 \
  # https://pythonspeed.com/articles/python-c-extension-crashes/
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  # poetry
  POETRY_VERSION=1.6.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR="/var/cache/pypoetry"

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  xz-utils \
  mime-support \
  \
  && echo "\nInstalling poetry package manager:" \
  && echo "https://github.com/python-poetry/poetry" \
  && curl -sSL --compressed "https://install.python-poetry.org" | python \
  && poetry --version \
  \
  echo "\nCleaning cache:" \
  && apt purge --autoremove -y curl xz-utils \
  && apt clean -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /root/.poetry/lib/poetry/_vendor/py2.7 \
  && rm -rf /root/.poetry/lib/poetry/_vendor/py3.5 \
  && rm -rf /root/.poetry/lib/poetry/_vendor/py3.6 \
  && rm -rf /root/.poetry/lib/poetry/_vendor/py3.7 \
  && rm -rf /root/.poetry/lib/poetry/_vendor/py3.8;

WORKDIR /opt/store
COPY pyproject.toml ./

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  git \
  && poetry install --no-dev --no-root && rm -rf ${POETRY_CACHE_DIR} \
  echo "\nCleaning cache:" \
  && apt purge --autoremove -y build-essential git \
  && apt clean -y \
  && rm -rf /root/.cache \
  && rm -rf /usr/local/src \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf ${POETRY_CACHE_DIR};

COPY . .

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]

EXPOSE ${PORT}

CMD ["uwsgi", "./store/uwsgi.ini"]
