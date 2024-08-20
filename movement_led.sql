-- Drop database energy_management;


CREATE DATABASE energy_management;

USE energy_management;

CREATE TABLE energy_usage_daily (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date date,
    energy_usage float
);


