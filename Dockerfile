FROM python:3.11-slim-bookworm AS base
ENV PYTHONUNBUFFERED=1 PATH=${PATH}:/root/.local/bin

RUN <<EOF
    apt-get update
    apt-get install curl git -qqy
    apt-get clean
EOF
RUN python -m pip install --no-cache-dir --quiet --upgrade --user pip "meltano==3.4" wheel


FROM base AS installer
ENV TAP_POSTGRES_PASSWORD=thewindisblowing
WORKDIR /project

COPY . .
RUN rm -rf .meltano
RUN <<EOF
    meltano install
    meltano invoke airflow:initialize
    meltano invoke airflow:create-admin -p pass
EOF

FROM installer AS ui

EXPOSE 8080 8793

CMD meltano invoke airflow standalone