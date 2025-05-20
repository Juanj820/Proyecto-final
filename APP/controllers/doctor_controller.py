for database.db import get_connection

class DoctorController:
    def __init__(self):
        self.conn = get_connection()
        
    def listar(self, busqueda='', estado='', pagina=1, por_pagina=10):
        cursor = self.conn.cursor(dictionary=True)
        offset = (pagina - 1) * por_pagina
        query = "SELECT * FROM doctores WHERE (nombre LIKE %s OR departamento LIKE %s)"
        params = [f"%{busqueda}%", f"%{busqueda}%"]
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        query += "LIMIT %s OFFSET %s"
        params.extend([por_pagina, offset])
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    
    def contar(self, busqueda='', estado=''):
        cursor = self.conn.cursor()
        query = "SELECT COUNT (*) FROM dortores WHERE (nombre LIKE %s OR departamento LIKE %s)"
        params = [f"%{busqueda}%", f"%{busqueda}%"]
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0]
    
    def crear(self, nombre, departamento, telefono, estado, creado_por):
        cursor = self.conn.cursor()
        query = "INSERT INTO doctores (nombre, departamento, telefono, estado, creado_por) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nombre, departamento, telefono, estado, creado_por))
        self.conn.commit()
    
    def actualizar(self, id, nombre, departamento, telefono, estado):
        cursor = self.conn.cursor()
        query = "UPDATE doctores SET nombre=%s, departamento=%s, telefono=%s, estado=%s WHERE id=%s"
        cursor.execute(query, (nombre, departamento, telefono, estado, id))
        self.conn.commit()
        
    def eliminar(self, id):
        cursor = self.conn.cursor()
        query = "DELETE FROM doctores WHERE id=%s"
        cursor.execute(query, (id,))
        self.conn.commit()