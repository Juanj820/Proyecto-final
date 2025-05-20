import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Cambia por tu contraseña de mySQL
        database="clinica"
    )