

DROP DATABASE IF EXISTS seekin_demo;
CREATE DATABASE seekin_demo;


USE seekin_demo;


CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
   

    name VARCHAR(100) NOT NULL,
   

    city VARCHAR(50),
    email VARCHAR(100),
    signup_date DATE
   
);


CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
   
);


CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT,
    

    product_id INT,
  
    quantity INT NOT NULL,
    order_date DATE NOT NULL,

    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);