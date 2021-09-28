from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import datetime

# [START default_args]
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}
# [END default_args]

# [START instantiate_dag]
load_initial_data_dag = DAG(
    '1_load_initial_data',
    default_args=default_args,
    schedule_interval = None,
)

t1 = PostgresOperator(task_id='create_schema',
                      sql="CREATE SCHEMA IF NOT EXISTS dbt_raw_data;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)
                     

t8 = PostgresOperator(task_id='drop_table_station_summary',
                      sql="DROP TABLE IF EXISTS aisles;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t9 = PostgresOperator(task_id='create_station_summary',
                      sql="create table if not exists dbt_raw_data.station_summary (ID float, flow_99 float, flow_max float, flow_median float, flow_total float, n_obs float);",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t10 = PostgresOperator(task_id='load_station_summary',
                      sql="	COPY dbt_raw_data.station_summary FROM '/sample_data/station_summary.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)  

       
t1 >> t8 >> t9 >> t10