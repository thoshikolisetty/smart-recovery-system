-- Active: 1744542276429@@127.0.0.1@3306
CREATE DATABASE IF NOT EXISTS lost_and_found;

USE lost_and_found;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    password VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    location VARCHAR(255),
    date DATE,
    category ENUM('Lost', 'Found'),
    description TEXT,
    image_path VARCHAR(255),
    posted_by VARCHAR(100)
);
