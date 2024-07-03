FROM mcr.microsoft.com/devcontainers/python:1-3.9-bookworm

ENV PYTHONUNBUFFERED=1

RUN <<EOF
    pipx ensurepath
    pipx install "meltano"
EOF
