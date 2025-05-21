class Paciente:
    def __init__(self, id, nombre, sintomas, telefono, direccion, estado, creado_por, creado_en, actualizado_en):
        self.id = id
        self.nombre = nombre
        self.sintomas = sintomas
        self.telefono = telefono
        self.direccion = direccion
        self.estado = estado
        self.creado_por = creado_por
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en