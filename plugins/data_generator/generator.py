import pandas as pd
import uuid
from datetime import datetime, timedelta
from random import uniform, choice
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator

class GenerateInsertOrderDataOperator(BaseOperator):

    def __init__(self, batch_size, postgres_conn_id = 'postgres_1', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch_size = batch_size
        self.postgres_conn_id = postgres_conn_id
    
    def execute(self, context):
        currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'CNY', 'HKD', 'NZD']
        
        data = {
            'order_id': [],
            'customer_email': [],
            'order_date': [],
            'amount': [],
            'currency': []
        }
    
        for _ in range(self.batch_size):
            order_id = str(uuid.uuid4())
            data['order_id'].append(order_id)
            data['customer_email'].append(f"customer{order_id[:5]}@gmail.com")
            order_date = datetime.now() - timedelta(days=uniform(0, 7))
            data['order_date'].append(order_date.strftime('%Y-%m-%d %H:%M:%S'))
            data['amount'].append(round(uniform(1, 1000), 2))
            data['currency'].append(choice(currencies))

        df = pd.DataFrame(data)
        pg_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        engine = pg_hook.get_sqlalchemy_engine()        
        df.to_sql('orders', con=engine, if_exists='append', index=False, method='multi', chunksize=1000)
        self.log.info(f"Successfully inserted {self.batch_size} records into orders table")

