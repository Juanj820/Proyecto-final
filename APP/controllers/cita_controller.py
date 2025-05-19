for database.db import get_connection

class CitaController:
    def __init__(self):
        self.conn = get_connection()
        
    def listar(self, busqueda='', estado='', pagina=1, por_pagina=10):
        cursor = self.conn.cursor(dictionary=True)
        offset = (pagina - 1) * por_pagina
        query = """
            SELECT c.id, d.id as id_doctor, d.nombre as doctor, d.departamento as departamento_doctor,
                    p.id as id_paciente, p.nombre as paciente, c.fecha, c.estado
            FROM citas c
            JOIN doctores d ON c.id_doctor = d.id
            JOIN pacientes p ON C.id_paciente = p.id
            WHERE (d.nombre LIKE %s OR p.nombre LIKE %s)
        """
        params = [f"%{busqueda}%", f"%{busqueda}%"]
        if estado:
            query += " AND c.estado = %s"
            params.append(estado)
        query += "ORDER BY c.fecha DESC LIMIT %s OFFSET %s"
        params.extend([por_pagina, offset])
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    
    def contar(self, busqueda='', estado=''):
        cursor = self.conn.cursor()
        query = """
            SELECT COUNT(*)
            FROM citas c
            JOIN doctores d ON c.id_doctor = d.id
            JOIN pacientesn p ON c.id_paciente = p.id
            WHERE (d.nombre LIKE %s OR p.nombre LIKE %s)
        """
        params = [f"%{busqueda}%", f"%{busqueda}%"]
        if estado:
            query += " AND c.estado = %s"
            params.append(estado)
        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0]
    
    def crear(self, id_doctor, id_paciente, fecha, estado, creado_por):
        cursor = self.conn.cursor()
        query = "INSERT INTO citas (id_doctor, id_paciente, fecha, estado, creado_por) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (id_doctor, id_paciente, fecha, estado, creado_por))
        self.conn.commit()
    
    def actualizar(self, id, id_doctor, id_paciente, fecha, estado):
        cursor = self.conn.cursor()
        query = "UPDATE citas SET id_doctor=%s, id_paciente=%s, fecha=%s, estado=%s WHERE id=%s"
        cursor.execute(query, (id_doctor, id_paciente, fecha, estado, id))
        self.conn.commit()
        
    def eliminar(self, id):
        cursor = self.conn.cursor()
        query = "DELETE FROM citas  WHERE id=%s"
        cursor.execute(query, (id,))
        self.conn.commit()
    
    