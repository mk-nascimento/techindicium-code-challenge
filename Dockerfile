FROM python:3.11-slim-bookworm AS base
ENV PYTHONUNBUFFERED=1

RUN <<EOF
    apt-get update
    apt-get install git -qqy
    apt-get clean
EOF
RUN python -m pip install --no-cache-dir --quiet --upgrade --user pip "meltano==3.4" wheel

ENV PATH=${PATH}:/root/.local/bin

FROM base AS installer
ENV TAP_POSTGRES_PASSWORD=thewindisblowing
WORKDIR /project

COPY . .
RUN rm -rf .meltano
RUN <<EOF
    meltano install
    meltano invoke airflow:initialize
    meltano invoke airflow users create -e admin@localhost -f admin -l localhost -r Admin -p pass -u admin
EOF

FROM installer AS scheduler

EXPOSE 8793

CMD meltano invoke airflow scheduler

FROM installer AS webserver

EXPOSE 8080

CMD meltano invoke airflow:ui