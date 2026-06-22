-- ============================================
-- schema.sql
-- This file creates the actual structure (tables) of our database.
-- Think of this like defining Mongoose Schemas, but stricter —
-- here we MUST define every column and its data type upfront.
-- ============================================

-- Step 1: Create a fresh database (like creating a new MongoDB database)
-- DROP DATABASE first so you can re-run this file safely while testing,
-- without "already exists" errors.
DROP DATABASE IF EXISTS seekin_demo;
CREATE DATABASE seekin_demo;

-- Step 2: Tell MySQL "every command after this happens inside seekin_demo"
-- (like switching to a specific MongoDB database with `use seekin_demo`)
USE seekin_demo;

-- ============================================
-- TABLE 1: customers
-- Stores info about each customer who buys from the business.
-- ============================================
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    -- AUTO_INCREMENT = MySQL fills this in automatically (1, 2, 3...)
    -- PRIMARY KEY = this column uniquely identifies each row (like Mongo's _id)

    name VARCHAR(100) NOT NULL,
    -- VARCHAR(100) = text, max 100 characters
    -- NOT NULL = this field is required, can't be left empty

    city VARCHAR(50),
    email VARCHAR(100),
    signup_date DATE
    -- DATE = stores a calendar date like 2026-01-15
);

-- ============================================
-- TABLE 2: products
-- Stores info about each product the business sells.
-- ============================================
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
    -- DECIMAL(10, 2) = a number with up to 10 digits total, 2 after the decimal
    -- This is the correct type for money — never use plain numbers for currency,
    -- it avoids rounding errors that happen with floating point numbers.
);

-- ============================================
-- TABLE 3: orders
-- This is the "relational" part — it LINKS customers and products together
-- instead of repeating their data. This is the core difference from MongoDB,
-- where you might have embedded the customer/product info directly.
-- ============================================
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT,
    -- This stores just the ID number of a customer, not their full info.
    -- It's called a "foreign key" — a pointer to a row in another table.

    product_id INT,
    -- Same idea — points to a row in the products table.

    quantity INT NOT NULL,
    order_date DATE NOT NULL,

    -- These two lines create the actual "link" between tables.
    -- They tell MySQL: "customer_id here MUST match a real customer_id
    -- in the customers table" — this prevents orphaned/invalid data.
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);