CREATE DATABASE  ulula_helper_db;
\connect  ulula_helper_db
CREATE TABLE uses_general_table (
    email TEXT,        
    passsword TEXT, 
    role INTEGER
);

CREATE ROLE ulula_user WITH LOGIN PASSWORD 'ulula_user_password';
GRANT CONNECT ON DATABASE ulula_helper_db TO ulula_user;
GRANT SELECT, INSERT ON TABLE uses_general_table TO ulula_user;