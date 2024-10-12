from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# Custom plugins, available via volume mapping. No need to worry about import issues.
from data_generator.generator import GenerateInsertOrderDataOperator
from currency_converter.converter import CurrencyConverterOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='creating_tables_dag',
    default_args=default_args,
    start_date=datetime.now() - timedelta(hours=2), # or use 'datetime(2024, 10, 12)'
    schedule_interval='@once', 
    catchup=False,
    template_searchpath = ['/opt/airflow/sql']
) as creating_tables_dag:
        
    create_orders_table = SQLExecuteQueryOperator(
        task_id='create_orders_table',
        conn_id='postgres_1',
        sql='create_orders_table.sql'
    )

    create_converted_orders_table = SQLExecuteQueryOperator(
        task_id='create_converted_orders_table',
        conn_id='postgres_2',
        sql='create_converted_orders_table.sql'
    )

create_orders_table >> create_converted_orders_table

with DAG(
    dag_id='generate_orders_dag',
    default_args=default_args,
    start_date=datetime.now() - timedelta(hours=2), # or use 'datetime(2024, 10, 12)'
    schedule_interval='*/10 * * * *', 
    catchup=True # set for testing
) as generate_orders_dag:
    
    generate_orders_task = GenerateInsertOrderDataOperator(
        task_id='generate_orders_task',
        batch_size=5000,
        postgres_conn_id='postgres_1'
    )

with DAG(
    dag_id='transform_and_transfer_dag',
    default_args=default_args,
    start_date=datetime.now() - timedelta(hours=2), # or use 'datetime(2024, 10, 12)'
    schedule_interval='@hourly',
    catchup=True # set for testing
) as transform_and_transfer_dag:
    
    transform_and_transfer_data = CurrencyConverterOperator(
        task_id='transform_and_transfer_task',
        converted_currency='EUR',
        postgres_conn_id_1='postgres_1',
        postgres_conn_id_2='postgres_2'
    )
