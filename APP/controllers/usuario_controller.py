from database.db import get_connection

class UsuarioController:
    def __init__(self):
        self.conn = get_connection()
    
    def login(self, usuario, password):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE usuario=%s AND password=%s"
        cursor.execute(query,(usuario, password))
        return cursor.fetchone()
    
    def actulizar(self, id, nombre, usuario, password=None, foto=None):
        cursor = self.conn.cursor()
        if password and foto:
            query = "UPDATE usuarios SET nombre=%s, usuario=%s, password=%s, foto=%s, actualizado_en=NOW() WHERE id=%s"
            cursor.execute(query, (nombre, usuario, password, foto, id))     
        elif password:
            query = "UPDATE usuarios SET nombre=%s, usuario=%s, password=%s, actualizado_en=NOW() WHERE id=%s"
            cursor.execute(query, (nombre, usuario, password, id))
        elif foto:
            query = "UPDATE usuarios SET nombre=%s, usuario=%s, foto=%s, actualizado_en=NOW() WHERE id=%s"
            cursor.execute(query, (nombre, usuario, foto, id))
        else:
            query = "UPDATE usuarios SET nombre=%s, usuario=%s, actualizado_en=NOW() WHERE id=%s"
            cursor.execute(query, (nombre, usuario, id))
        self.conn.commit()
    
    def obtener_por_id(self, id):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE id=%s"
        cursor.execute(query,(id,))
        return cursor.fetchone()
