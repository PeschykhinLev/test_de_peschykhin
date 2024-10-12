CREATE TABLE IF NOT EXISTS orders_converted (
    order_id UUID,
    customer_email VARCHAR(255),
    order_date TIMESTAMP,
    amount DECIMAL(10, 2),
    converted_currency VARCHAR(3)
); 