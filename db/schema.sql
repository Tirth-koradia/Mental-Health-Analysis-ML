CREATE DATABASE IF NOT EXISTS mental_health_app;
USE mental_health_app;

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_text TEXT,
    predicted_label VARCHAR(50),
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);