CREATE DATABASE IF NOT EXISTS Client_Query_System;
USE Client_Query_System;


CREATE TABLE users (
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('Client', 'Support') NOT NULL
);

CREATE TABLE queries (
    query_id INT AUTO_INCREMENT PRIMARY KEY,
    mail_id VARCHAR(150) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    query_heading VARCHAR(255) NOT NULL,
    query_description TEXT NOT NULL,
    status ENUM('Open','Closed') DEFAULT 'Open',
    query_created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    query_closed_time DATETIME NULL
);


INSERT INTO queries
(mail_id, mobile_number, category, query_heading, query_description, status, query_created_time, query_closed_time)
VALUES
('arun@gmail.com','9876543210','Login','Login Issue','Unable to login','Open','2025-01-10 10:00:00',NULL),
('kavya@gmail.com','9876543211','Payment','Payment Failed','UPI failed','Closed','2025-01-09 09:00:00','2025-01-09 10:00:00'),
('ramesh@gmail.com','9876543212','Account','Password Reset','Reset link missing','Open','2025-01-11 12:00:00',NULL),
('divya@gmail.com','9876543213','Technical','App Crash','App crashes','Closed','2025-01-08 14:00:00','2025-01-08 16:00:00'),
('suresh@gmail.com','9876543214','Account','Account Locked','Locked out','Open','2025-01-12 15:00:00',NULL),
('meena@gmail.com','9876543215','Profile','Profile Update','Cannot update profile','Closed','2025-01-07 11:00:00','2025-01-07 12:30:00');



SELECT * FROM users;

SELECT * FROM queries;


-- Create user with native password plugin
CREATE USER 'streamlit_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Dharani@12345';

-- Grant privileges on your database
GRANT ALL PRIVILEGES ON Client_Query_System.* TO 'streamlit_user'@'localhost';

FLUSH PRIVILEGES;

SELECT user, host FROM mysql.user WHERE user='streamlit_user';

SELECT user, host, plugin FROM mysql.user WHERE user='streamlit_user';





