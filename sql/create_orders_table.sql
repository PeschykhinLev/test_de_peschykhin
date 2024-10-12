CREATE TABLE IF NOT EXISTS orders (
    order_id UUID,
    customer_email VARCHAR(255),
    order_date TIMESTAMP,
    amount DECIMAL(10, 2),
    currency VARCHAR(3)
);