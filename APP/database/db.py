import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="juan", # Cambia por tu contraseña de mySQL
        database="clinica"
    )