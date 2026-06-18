import mysql.connector


class DBManager:
    def __init__(self):
        self.config = {
            "host": "127.0.0.1",
            "port": 3306,
            "password": "1234",
            "database": "Intelligence_db",
            "user": "root"
        }
        self._connection = None

    def get_connection(self):
        if self._connection:
            return self._connection
        self._connection = mysql.connector.connect(
            **self.config
        )
        return self._connection

    def create_database(self):
        curser = self.get_connection().cursor()
        curser.execute("""CREATE DATABASE IF NOT EXISTS Intelligence_db""")
        curser.close()
    
    def create_tables(self):
        curser = self.get_connection().cursor()
        curser.execute("""CREATE TABLE IF NOT exists agents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    specialty VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    completed_missions INT DEFAULT 0,
    failed_missions INT DEFAULT 0,
    agent_rank ENUM("Low", "Junior", "Senior", "Commander")
)""")
        curser.execute("""CREATE TABLE IF NOT exists missions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50),
    description TEXT,
    location VARCHAR(50),
    difficulty INT(10),
    importance INT(10),
    status VARCHAR(50) DEFAULT "NEW",
    risk_level VARCHAR(50),
    assigned_agent_id INT
)""")
        
