from datetime import datetime

def registrar_accion(usuario_id, accion, descripcion):
    # Aqui podrias guardar en un archivo o tabla de auditoria
    with open("auditoria.log", "a") as f:
        f.write(f"{datetime.now()} - Usuario {usuario_id} - {accion}: {descripcion}\n")