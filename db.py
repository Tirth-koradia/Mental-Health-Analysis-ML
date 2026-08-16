import os

def get_connection():
    if os.getenv("RENDER"):
        # Production → SQLite
        import sqlite3
        return sqlite3.connect("database.db", check_same_thread=False)
    else:
        # Local → MySQL
        import mysql.connector
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="mental_health_app"
        )
