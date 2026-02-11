-- Create Database
CREATE DATABASE smartstock;
USE smartstock;

-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(20)
);

-- PRODUCTS TABLE
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    category VARCHAR(100),
    stock INT,
    expiry DATE
);

-- SALES TABLE
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- CUSTOMER PROFILE TABLE
CREATE TABLE customers_profile (
    user_id INT,
    product_id INT,
    frequency INT,
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- PRODUCT PAIRS TABLE
CREATE TABLE product_pairs (
    product_a INT,
    product_b INT,
    confidence FLOAT,
    FOREIGN KEY (product_a) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (product_b) REFERENCES products(id) ON DELETE CASCADE
);
