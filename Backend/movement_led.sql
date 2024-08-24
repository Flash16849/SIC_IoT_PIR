CREATE DATABASE energy_management;

USE energy_management;

-- Drop database energy_management;
-- Drop table energy_usage_monthly;
-- Drop table energy_usage_daily;


CREATE TABLE energy_usage_daily (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date date unique key,
    e_usage_daily float
);

-- CREATE TABLE energy_usage_weekly (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     date date,
--     e_usage_weekly float
-- );

CREATE TABLE energy_usage_monthly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month int,
    e_usage_monthly float
);
