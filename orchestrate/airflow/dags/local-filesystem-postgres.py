import json
import os
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "catchup": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "concurrency": 1,
}
PROJECT_ROOT = os.getenv("MELTANO_PROJECT_ROOT", os.getcwd())


def increment_datetime(date):
    date_format = "%Y-%m-%d"
    dt = datetime.strptime(date, date_format)
    dt = dt + timedelta(1)
    return dt.strftime(date_format)


def create_csv_file_definition(date):
    date = increment_datetime(date)
    data_path = os.path.join(PROJECT_ROOT, "data")
    csv_path = os.path.join(data_path, "csv", date)
    postgres_path = os.path.join(data_path, "postgres")

    files_definition = []
    csv, postgres = os.listdir(csv_path), os.listdir(postgres_path)
    for file in postgres:
        postgres_file_path = os.path.join(postgres_path, file, date, f"{file}.csv")
        table = {"entity": file.split("-")[1], "path": postgres_file_path}
        files_definition.append(table)
    for file in csv:
        csv_file_path = os.path.join(csv_path, file)
        table = {"entity": file.split(".")[0].split("-")[1], "path": csv_file_path}
        files_definition.append(table)

    with open(f"{PROJECT_ROOT}/def.json", "w") as file_json:
        json.dump(files_definition, file_json, indent=2)


args = DEFAULT_ARGS.copy()
with DAG(
    "local-filesystem-postgres",
    tags=["custom", "tap-csv", "target-postgres"],
    catchup=False,
    default_args=args,
    schedule_interval="@daily",
    start_date=datetime(2024, 7, 1),
    max_active_runs=1,
) as dag:
    csv_local_task = ExternalTaskSensor(
        task_id="csv-local-task",
        external_dag_id="meltano_csv-local-filesystem",
        allowed_states=["success"],
        mode="reschedule",
        timeout=60*2.5,
        poke_interval=45,
    )
    postgres_local_task = ExternalTaskSensor(
        task_id="postgres-local-task",
        external_dag_id="meltano_postgres-local-filesystem",
        allowed_states=["success"],
        mode="reschedule",
        timeout=60*2.5,
        poke_interval=45,
    )
    get_csv_file_definition = PythonOperator(
        task_id="get-csv-file-definition",
        python_callable=create_csv_file_definition,
        op_kwargs={"date": "{{ ds }}"},
    )
    set_file_definition = BashOperator(
        task_id="set-file-definition",
        bash_command="meltano config tap-local set csv_files_definition /project/def.json",
    )
    csv_to_postgres = BashOperator(
        task_id="local-csv-to-postgres",
        bash_command="meltano el tap-local target-postgres",
    )

    csv_local_task >> get_csv_file_definition
    postgres_local_task >> get_csv_file_definition
    set_file_definition >> csv_to_postgres
    get_csv_file_definition >> csv_to_postgres