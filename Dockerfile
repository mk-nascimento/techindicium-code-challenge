FROM meltano/meltano:v3.4-python3.11

COPY . .

RUN <<EOF
    meltano install
    meltano invoke airflow:initialize
    meltano invoke airflow users create -e admin@localhost -f admin -l localhost -r Admin -p pass -u admin
    meltano invoke airflow scheduler &
EOF


CMD ["invoke", "airflow", "webserver"]