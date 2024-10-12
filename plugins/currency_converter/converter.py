import requests
import psycopg2
from airflow.models import Variable, BaseOperator

# def fetch_and_transform_data(converted_currency):

#     conn_1 = psycopg2.connect(
#         host="host.docker.internal",
#         database="postgres-1",
#         user="postgres",
#         password="postgres",
#         port=5433
#     )
#     cursor_1 = conn_1.cursor()
    
#     cursor_1.execute("SELECT order_id, customer_email, order_date, amount, currency FROM orders")
#     orders = cursor_1.fetchall()

#     cursor_1.close()
#     conn_1.close()
    
#     response = requests.get('https://openexchangerates.org/api/latest.json?app_id={}'.format(Variable.get("my_api_user")))
#     rates = response.json().get('rates', {})
    
#     converted_orders = []
#     for order in orders:
#         order_id, customer_email, order_date, amount, currency = order
#         conversion_rate = rates.get(converted_currency, 1)
#         converted_amount = amount / conversion_rate
#         converted_orders.append((order_id, customer_email, order_date, converted_amount, converted_currency))

#     conn_2 = psycopg2.connect(
#         host="host.docker.internal",
#         database="postgres-2",  
#         user="postgres",
#         password="postgres",
#         port=5434
#     )
#     cursor_2 = conn_2.cursor()
    
    
#     for order in converted_orders:
#         cursor_2.execute("""
#             INSERT INTO orders_converted (order_id, customer_email, order_date, amount, converted_currency)
#             VALUES (%s, %s, %s, %s, %s)
#         """, order)
    
#     conn_2.commit()
#     cursor_2.close()
#     conn_2.close()

# class CurrencyConverterOperator(BaseOperator):

#     def __init__(self, converted_currency, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.converted_currency = converted_currency

#     def execute(self, context):
        
#         converted_orders = self.convert_currency(context)
#         self.insert_converted_orders(converted_orders)
    
#     def convert_currency(self, context):
#         conn_1 = psycopg2.connect(
#             host="host.docker.internal",
#             database="postgres-1",
#             user="postgres",
#             password="postgres",
#             port=5433
#         )
#         cursor_1 = conn_1.cursor()
        
#         cursor_1.execute("SELECT order_id, customer_email, order_date, amount, currency FROM orders")
#         orders = cursor_1.fetchall()

#         cursor_1.close()
#         conn_1.close()
        
#         response = requests.get('https://openexchangerates.org/api/latest.json?app_id={}'.format(Variable.get("my_api_user")))
#         rates = response.json().get('rates', {})
        
#         converted_orders = []

#         for order in orders:
#             order_id, customer_email, order_date, amount, currency = order
#             conversion_rate_to_usd = rates.get(currency)
#             conversion_rate_to_final_currency = rates.get(self.converted_currency)
#             converted_amount = float(amount) / conversion_rate_to_usd * conversion_rate_to_final_currency
#             converted_orders.append((order_id, customer_email, order_date, converted_amount, self.converted_currency))
        
#         return converted_orders
    
#     def insert_converted_orders(self, converted_orders):
#         conn_2 = psycopg2.connect(
#             host="host.docker.internal",
#             database="postgres-2",  
#             user="postgres",
#             password="postgres",
#             port=5434
#         )
        
#         cursor_2 = conn_2.cursor()

#         for order in converted_orders:
#             cursor_2.execute("""
#                 INSERT INTO orders_converted (order_id, customer_email, order_date, amount, converted_currency)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, order)
        
#         conn_2.commit()
#         cursor_2.close()
#         conn_2.close()

# class CurrencyConverterOperator(BaseOperator):

#     def __init__(self, converted_currency, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.converted_currency = converted_currency

#     def execute(self, context):
#         existing_order_ids = self.get_existing_order_ids()
#         converted_orders = self.convert_currency(context, existing_order_ids)
#         self.insert_converted_orders(converted_orders)
    
#     def get_existing_order_ids(self):
#         conn_2 = psycopg2.connect(
#             host="host.docker.internal",
#             database="postgres-2",  
#             user="postgres",
#             password="postgres",
#             port=5434
#         )
#         cursor_2 = conn_2.cursor()
        
#         cursor_2.execute("SELECT order_id FROM orders_converted")
#         existing_order_ids = set(row[0] for row in cursor_2.fetchall())
        
#         cursor_2.close()
#         conn_2.close()
        
#         return existing_order_ids
    
#     def convert_currency(self, context, existing_order_ids):
#         conn_1 = psycopg2.connect(
#             host="host.docker.internal",
#             database="postgres-1",
#             user="postgres",
#             password="postgres",
#             port=5433
#         )
#         cursor_1 = conn_1.cursor()
        
#         cursor_1.execute("SELECT order_id, customer_email, order_date, amount, currency FROM orders")
#         orders = cursor_1.fetchall()

#         cursor_1.close()
#         conn_1.close()
        
#         response = requests.get('https://openexchangerates.org/api/latest.json?app_id={}'.format(Variable.get("my_api_user")))
#         rates = response.json().get('rates', {})
        
#         converted_orders = []

#         for order in orders:
#             order_id, customer_email, order_date, amount, currency = order

#             if order_id not in existing_order_ids:
#                 conversion_rate_to_usd = rates.get(currency)
#                 conversion_rate_to_final_currency = rates.get(self.converted_currency)
#                 converted_amount = float(amount) / conversion_rate_to_usd * conversion_rate_to_final_currency
#                 converted_orders.append((order_id, customer_email, order_date, converted_amount, self.converted_currency))
        
#         return converted_orders
    
#     def insert_converted_orders(self, converted_orders):
#         conn_2 = psycopg2.connect(
#             host="host.docker.internal",
#             database="postgres-2",  
#             user="postgres",
#             password="postgres",
#             port=5434
#         )
        
#         cursor_2 = conn_2.cursor()

#         for order in converted_orders:
#             cursor_2.execute("""
#                 INSERT INTO orders_converted (order_id, customer_email, order_date, amount, converted_currency)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, order)
        
#         self.log.info(f"Successfully transformed and transferred {len(converted_orders)} records")
        
#         conn_2.commit()
#         cursor_2.close()
#         conn_2.close()

import requests
from airflow.models import Variable, BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

class CurrencyConverterOperator(BaseOperator):

    def __init__(self, converted_currency, postgres_conn_id_1, postgres_conn_id_2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.converted_currency = converted_currency
        self.postgres_conn_id_1 = postgres_conn_id_1
        self.postgres_conn_id_2 = postgres_conn_id_2

    def execute(self, context):
        existing_order_ids = self.get_existing_order_ids()
        converted_orders = self.convert_currency(context, existing_order_ids)
        self.insert_converted_orders(converted_orders)
    
    def get_existing_order_ids(self):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id_2)
        existing_order_ids = hook.get_pandas_df("SELECT order_id FROM orders_converted")
        return set(existing_order_ids['order_id'])
    
    def convert_currency(self, context, existing_order_ids):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id_1)
        
        orders = hook.get_pandas_df("SELECT order_id, customer_email, order_date, amount, currency FROM orders")
        
        response = requests.get('https://openexchangerates.org/api/latest.json?app_id={}'.format(Variable.get("my_api_user")))
        rates = response.json().get('rates', {})
        
        converted_orders = []

        for _, order in orders.iterrows():
            if order['order_id'] not in existing_order_ids:
                conversion_rate_to_usd = rates.get(order['currency'])
                conversion_rate_to_final_currency = rates.get(self.converted_currency)
                converted_amount = float(order['amount']) / conversion_rate_to_usd * conversion_rate_to_final_currency
                converted_orders.append((
                    order['order_id'],
                    order['customer_email'],
                    order['order_date'],
                    converted_amount,
                    self.converted_currency
                ))
        
        return converted_orders
    
    def insert_converted_orders(self, converted_orders):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id_2)
        
        hook.insert_rows(table='orders_converted', rows=converted_orders, target_fields=['order_id', 'customer_email', 'order_date', 'amount', 'converted_currency'])
        
        self.log.info(f"Successfully transformed and transferred {len(converted_orders)} records")