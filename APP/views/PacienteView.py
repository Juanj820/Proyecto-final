import ttkbootstrap as tb
from tkinter import messagebox, StringVar, IntVar

ESTADOS = ["Admitido", "En Espera"]
SINTOMAS_COMUNES = [
    "Ninguno", "Dolor de cabeza", "Fiebre", "Tos", "Dolor abdominal", "Mareo",
    "Vómito", "Alergia", "Fractura", "Dolor muscular", "Insomnio"
]

class PacienteView:
    def __init__(self, parent, controller, usuario_id):
        self.parent = parent
        self.cotroller = controller
        self.usuario_id = usuario_id
        self.pagina = 1
        self.por_pagina = 5
        self.busqueda = StringVar()
        self.busqueda_estado = StringVar(value="")
        self.total_pagina = 1
        self.total_registros = 0

        self.frame = tb.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        tb.Label(self.frame, text="Gestión de Pacientes", font=("Arial", 18, "bold"), bootstyle="primary").pack(pady=10)

        # Busqueda
        busq_frame = tb.Frame(self.frame)
        busq_frame.pack(pady=5)
        tb.Label(busq_frame, text="Buscar:").pack(side="left")
        self.busq_entry = tb.Entry(busq_frame, textvariable=self.busqueda)
        self.busq_entry.pack(side="left",padx=5)
        tb.Label(busq_frame,text="Estado:").pack(side="left",padx=5)
        self.estado_cd = tb.Combobox(busq_frame, values=["",*ESTADOS], textvariable=self.busqueda_estado, width=12, state="readonly")
        self.estado_cd.pack(side="left")
        tb.Button(busq_frame, text="Buscar", botstyle="success", command=self.buscar).pack(side="left", padx=5)
        
        # Contenedor principal para tabla y botones
        main_container = tb.Frame(self.frame)
        main_container.pack(fill="both", expand=True, padx=30, pady=5)
        
        # Table con espaciado lateral
        table_frame = tb.Frame(main_container)
        table_frame.pack(side="left", fill="both", expand=True,padx=(20, 20))
        self.table = tb.Treeview(table_frame, columns=("id", "nombre", "sintomas", "direccion", "estado"), show="headings", height=7, bootstyle="info")
        self.table.heading("id", text="ID")
        self.table.heading("nombre", text="Nombre")
        self.table.heading("sintomas", text="Sintomas")
        self.table.heading("telefono", text="Teléfono")
        self.table.heading("direccion", text="Dirección")
        self.table.heading("estado", text="Estado")
        self.table.column("id", width=40)
        self.table.column("nombre", width=120)
        self.table.column("sintomas", width=120)
        self.table.column("telefono", width=100)
        self.table.column("direccion", width=140)
        self.table.column("estado", width=90)
        self.table.pack(pady=10, fill="x")    