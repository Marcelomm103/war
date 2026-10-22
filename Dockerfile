FROM node:22.23.4-bookworm-slim AS node

FROM python:3.11-slim-bookworm

COPY --from=node /usr/local/ /usr/local/

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/home/dev/.venv \
    PATH="/home/dev/.venv/bin:${PATH}"

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        git \
        openssh-client \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libxtst6 \
        tesseract-ocr \
        tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

RUN npm install --global npm@10.9.9 \
    && groupadd --gid 1000 dev \
    && useradd --uid 1000 --gid dev --create-home --shell /bin/bash dev

WORKDIR /workspace
COPY --chown=dev:dev . .

USER dev

RUN python3 -m venv "${VIRTUAL_ENV}" \
    && python -m pip install --upgrade pip setuptools==83.0.0 \
    && python -m pip install \
        --index-url https://pypi.org/simple \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        "torch==2.14.1" \
    && python -m pip install \
        -e "lib/war_game_engine[test,quality]" \
        -e "lib/war_AI[test,quality,service,training]" \
        -e "lib/war_analyzer[test,quality,vision]" \
        pip-audit==2.10.1 \
    && python -m pip check \
    && mkdir -p lib/war_analyzer/pwa/node_modules

EXPOSE 5173
