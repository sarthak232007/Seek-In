-- ============================================
-- seed_data.sql
-- This fills our empty tables with fake-but-realistic business data,
-- so we have something to actually query and demo.
-- Run this AFTER schema.sql (tables must exist first).
-- ============================================

USE seekin_demo;

-- ============================================
-- Insert customers
-- INSERT INTO tablename (column1, column2...) VALUES (value1, value2...);
-- We don't specify customer_id because AUTO_INCREMENT fills it for us.
-- ============================================
INSERT INTO customers (name, city, email, signup_date) VALUES
('Raj Kumar', 'Lucknow', 'raj.kumar@mail.com', '2025-03-10'),
('Priya Singh', 'Delhi', 'priya.singh@mail.com', '2025-04-22'),
('Aman Verma', 'Kanpur', 'aman.verma@mail.com', '2025-05-15'),
('Sneha Gupta', 'Mumbai', 'sneha.gupta@mail.com', '2025-06-01'),
('Vikram Rathore', 'Jaipur', 'vikram.r@mail.com', '2025-06-20'),
('Anita Desai', 'Pune', 'anita.desai@mail.com', '2025-07-05'),
('Karan Mehta', 'Ahmedabad', 'karan.mehta@mail.com', '2025-08-12'),
('Pooja Nair', 'Chennai', 'pooja.nair@mail.com', '2025-09-18'),
('Rohit Sharma', 'Lucknow', 'rohit.sharma@mail.com', '2025-10-02'),
('Divya Iyer', 'Bangalore', 'divya.iyer@mail.com', '2025-11-11');

-- ============================================
-- Insert products
-- ============================================
INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 45000.00),
('Wireless Mouse', 'Electronics', 599.00),
('Notebook', 'Stationery', 50.00),
('Pen Set', 'Stationery', 120.00),
('Office Chair', 'Furniture', 4500.00),
('Desk Lamp', 'Furniture', 899.00),
('Bluetooth Speaker', 'Electronics', 2200.00),
('Backpack', 'Accessories', 1500.00),
('Water Bottle', 'Accessories', 250.00),
('Monitor', 'Electronics', 12000.00);

-- ============================================
-- Insert orders
-- These reference customer_id and product_id from the tables above.
-- Since we inserted 10 customers and 10 products in order,
-- their IDs will be 1 through 10 for each.
-- ============================================
INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
(1, 1, 1, '2026-01-15'),
(2, 3, 5, '2026-01-16'),
(3, 7, 1, '2026-01-18'),
(4, 5, 2, '2026-01-20'),
(5, 2, 1, '2026-02-01'),
(6, 10, 1, '2026-02-03'),
(7, 4, 10, '2026-02-05'),
(8, 8, 1, '2026-02-10'),
(9, 1, 1, '2026-02-14'),
(10, 6, 2, '2026-02-15'),
(1, 9, 3, '2026-03-01'),
(2, 1, 1, '2026-03-05'),
(3, 3, 2, '2026-03-08'),
(4, 7, 1, '2026-03-10'),
(5, 5, 1, '2026-03-12'),
(6, 2, 1, '2026-03-15'),
(7, 10, 1, '2026-03-18'),
(8, 4, 5, '2026-03-20'),
(9, 6, 1, '2026-03-22'),
(10, 8, 2, '2026-03-25');