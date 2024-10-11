## Test Task (DE) - Peschykhin Lev

## Project Structure

```plaintext
airflow-project/
├── dags/
│   └── dag.py
├── plugins/
│   ├── data_generator/
│   │   └── generator.py
│   └── currency_converter/
│       └── converter.py
├── sql/
│   ├── create_orders_table.sql
│   └── create_converted_orders_table.sql
│
├── .env
├── docker-compose.yaml
└── README.md
```

## DAG Definitions

This file (`dags/dag.py`) contains the definitions for three Airflow DAGs:

1. `creating_tables_dag`: Runs once to set up the necessary database tables.
   - Creates an orders table in the first Postgres (`postgres-1`) database.
   - Creates a converted orders table in the second Postgres (`postgres-2`) database.

2. `generate_orders_dag`: Runs every 10 minutes to generate and insert order data in the first Postgres (`postgres-1`) database.
   - Uses a custom `GenerateInsertOrderDataOperator` to create and insert 5000 orders per run.

3. `transform_and_transfer_dag`: Runs hourly to transform 'unique' data from the first Postgres (`postgres-1`) database and transfer it to the second Postgres (`postgres-2`) database.
   - Uses a custom `CurrencyConverterOperator` to convert order amounts to any desires `converted_currency` (`EUR` by default).

SQL scripts for table creation are stored in the `/opt/airflow/sql` directory.

The `currency_converter/converter.py` file contains the logic for converting order amounts with API request to `openexchangerates.org`.

## Postgres-1 Database Details

### Orders Table

- **Table Name**: `orders`
- **Description**: Stores the original order information generated by the `GenerateInsertOrderDataOperator`.
- **Columns**:
  - `order_id` (UUID): Unique identifier for each order
  - `customer_email` (VARCHAR): Email address of the customer
  - `order_date` (TIMESTAMP): Date and time when the order was placed
  - `amount` (NUMERIC): Original order amount
  - `currency` (VARCHAR): Original currency (randomly chosen) of the order (e.g., USD, EUR, GBP)

- **Connection Details**:
  - Host: host.docker.internal
  - Database: postgres-1
  - User: postgres
  - Password: postgres
  - Port: 5433

## Postgres-2 Database Details

### Converted Orders Table

- **Table Name**: `orders_converted`
- **Description**: Stores the order information after currency conversion, as processed by the `CurrencyConverterOperator`.
- **Columns**:
  - `order_id` (UUID): Unique identifier for each order (same as in Postgres-1)
  - `customer_email` (VARCHAR): Email address of the customer
  - `order_date` (TIMESTAMP): Date and time when the order was placed
  - `amount` (NUMERIC): Converted order amount in the desired currency
  - `converted_currency` (VARCHAR): The currency to which the amount has been converted

- **Connection Details**:
  - Host: host.docker.internal
  - Database: postgres-2
  - User: postgres
  - Password: postgres
  - Port: 5434

## Docker Compose Configuration

`docker-compose.yml` file has been customized to support our specific Airflow project requirements:

1. **Additional Postgres Databases**: 
   - `postgres1`
   - `postgres2`
   - The original `postgres` service remains for Airflow logs.

2. **SQL Scripts Volume**:
   - Added a new volume mapping: `${AIRFLOW_PROJ_DIR:-.}/sql:/opt/airflow/sql`
   - This allows SQL scripts in the local `sql` directory to be accessible within the Airflow containers.

## API KEY
   - Value: '873e6dea131a4ed19d337c44ee7f36c6'
   - Purpose: This is the API key for accessing the OpenExchangeRates API, declares in `.env` file. I will leave it here for testing purposes ;)

3. **Disabled Example DAGs**

## Quick Testing Guide

### 1. Start the Airflow Environment

Run the following command in the project directory, after booting up Docker Desktop:
```bash
docker-compose up
```
Wait till we get 'healthy' status on all containers, it may take a some time.

<img width="1199" alt="image" src="https://github.com/user-attachments/assets/82f01456-6f88-43ab-a649-03f1a11cb7ad">

### 2. Access Airflow Web UI

Open `http://localhost:8080` in your browser. Log in with:
- Username: airflow
- Password: airflow

Go to 'Admin > Connection' and connect to postgres-1 and postgres-2

<img width="1425" alt="image" src="https://github.com/user-attachments/assets/bd0424cf-4178-45b3-a00e-0a5060e64b26">

### 3. Run DAGs

1. Run `creating_tables_dag` to set up database tables.
2. Run `generate_orders_dag` to start generating orders data.
3. Run `transform_and_transfer_dag` to convert data and transfer.

<img width="1407" alt="image" src="https://github.com/user-attachments/assets/15049370-7e1a-4835-bcbd-0ed7f94e03ed">

### 4. Verify Data

Connect to databases and check data:

1. `Postgres-1`:

<img width="937" alt="image" src="https://github.com/user-attachments/assets/cb93de3b-4f08-4d1f-9b86-139ff500e7de">

2. `Postgres-2` (converted data):

<img width="978" alt="image" src="https://github.com/user-attachments/assets/548287ca-a990-4bb5-8d9c-3eda3c5e3053">

## Takeaways and Concerns
- It was a great first hands on expereince in combiling tools like Docker, AirFlow, Postgres all together.
- Concerned about dedicating a whole DAG for a single tasks, as it might be inneficieant, but due to interal scheduling ('@once', '*/10 * * * *', '@hourly') found spliting the tasks a way to go.
- `CurrencyConverterOperator` might be revised and rebuild to avoid multiple connections to the dbs.

