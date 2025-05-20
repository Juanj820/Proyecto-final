for database.db import get_connection

class PacienteController:
    def __init__(self):
        self.conn = get_connection()
        
    def listar(self, busqueda='', estado='', pagina=1, por_pagina=10):
        cursor = self.conn.cursor(dictionary=True)
        offset = (pagina - 1) * por_pagina
        query = "SELECT * FROM pacientes WHERE LIKE %s"
        params = [f"%{busqueda}%"]
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        query += "LIMIT %s OFFSET %s"
        params.extend([por_pagina, offset])
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    
    def contar(self, busqueda='', estado=''):
        cursor = self.conn.cursor()
        query = "SELECT COUNT (*) FROM pacientes WHERE nombre LIKE %s"
        params = [f"%{busqueda}%"]
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0]
    
    def crear(self, nombre, sintomas, telefono, direccion, estado, creado_por):
        cursor = self.conn.cursor()
        query = "INSERT INTO pacientes (nombre, sintomas, telefono, direccion, estado, creado_por) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nombre, sintomas, telefono, direccion, estado, creado_por))
        self.conn.commit()
    
    def actualizar(self, id, nombre, sintomas, telefono, direccion, estado):
        cursor = self.conn.cursor()
        query = "UPDATE pacientes SET nombre=%s, sintomas=%s, telefono=%s, direccion=%s, estado=%s WHERE id=%s"
        cursor.execute(query, (nombre, sintomas, telefono, direccion, estado, id))
        self.conn.commit()
        
    def eliminar(self, id):
        cursor = self.conn.cursor()
        query = "DELETE FROM pacientes WHERE id=%s"
        cursor.execute(query, (id,))
        self.conn.commit()