CREATE DATABASE sanjeevani_sync;
USE sanjeevani_sync;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE medicine_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    medicine_name VARCHAR(100),
    time TIME
);
