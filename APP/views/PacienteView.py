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
        self.controller = controller
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
        self.estado_cd = tb.Combobox(busq_frame, values=["", *ESTADOS], textvariable=self.busqueda_estado, width=12, state="readonly")
        self.estado_cd.pack(side="left")
        tb.Button(busq_frame, text="Buscar", bootstyle="success", command=self.buscar).pack(side="left", padx=5)
        
        # Contenedor principal para tabla y botones
        main_container = tb.Frame(self.frame)
        main_container.pack(fill="both", expand=True, padx=30, pady=5)
        
        # Table con espaciado lateral
        tabla_frame = tb.Frame(main_container)
        tabla_frame.pack(side="left", fill="both", expand=True,padx=(20, 20))
        self.tabla = tb.Treeview(tabla_frame, columns=("id", "nombre", "sintomas", "direccion", "estado"), show="headings", height=7, bootstyle="info")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("sintomas", text="Sintomas")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("direccion", text="Dirección")
        self.tabla.heading("estado", text="Estado")
        self.tabla.column("id", width=40)
        self.tabla.column("nombre", width=120)
        self.tabla.column("sintomas", width=120)
        self.tabla.column("telefono", width=100)
        self.tabla.column("direccion", width=140)
        self.tabla.column("estado", width=90)
        self.tabla.pack(pady=10, fill="x")
        
        #LabelFame para botones a la derecha, igualando el alto de la tabla
        btns_frame = tb.Labelframe(main_container, text="Acciones", bootstyle="info")
        btns_frame.pack(side="left", fill="y", padx=(10, 0), pady=10, expand=False)
        btns_frame.update_idletasks()
        tabla_height = self.tabla.winfo_reqheight()
        btns_frame.config(height=tabla_height)
        
        # Botones de accióm con menor espacio entre ellos
        tb.Button(btns_frame, text="Nuevo Paciente", bootstyle="info", command=self.nuevo_paciente, width=16).pack(pady=6, padx=16)
        tb.Button(btns_frame, text="Editar", bootstyle="warning", command=self.editar_paciente, width=16).pack(pady=6, padx=16)
        tb.Button(btns_frame, text="Eliminar", bootstyle="danger", command=self.eliminar_paciente, width=16).pack(pady=6, padx=16)
        
        # Paginación con botones más paqueños
        pag_frame = tb.Frame(self.frame)
        pag_frame.pack(pady=(20, 10))
        self.lbl_pagina = tb.Label(pag_frame, text="")
        self.lbl_pagina.pack(side="left", padx=5)
        tb.Button(pag_frame, text="Anterior", bootstyle="secondary", command=self.pagina_anterior, width=8).pack(side="left", padx=5)
        tb.Button(pag_frame, text="Siguiente", bootstyle="secondary", command=self.pagina_siguiente, width=8).pack(side="left", padx=5)
        self.lbl_total = tb.Label(pag_frame, text="")
        self.lbl_total.pack(side="left", padx=15)
        
        self.cargar_tabla ()
    
    def buscar(self):
        self.pagina = 1
        self.cargar_tabla()
    
    def cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        busq = self.busqueda.get()
        estado = self.busqueda_estado.get()
        pacientes = self.controller.listar(busq, estado, self.pagina, self.por_pagina)
        for pac in pacientes:
            self.tabla.insert("","end", values=(pac["id"], pac["nombre"], pac["sintomas"], pac["telefono"], pac["direccion"], pac["estado"]))
        #Calcular total de páginas y registros
        total = self.controller.contar(busq, estado)
        self.total_registros = total
        self.total_paginas = max(1, (total + self.por_pagina -1) // self.por_pagina)
        self.lbl_pagina.config(text=f"Página {self.pagina} de {self.total_pagina}")
        self.lbl_total.config(text=f"Total registros: {self.total_registros}")
        
    def pagina_anterior(self):
        if self.pagina > 1:
            self.pagina -=1
            self.cargar_tabla()
    
    def pagina_siguiente(self):
        if self.pagina < self.total_paginas:
            self.pagina +=1
            self.cargar_tabla()
            
    def nuevo_paciente(self):
        self.formulario_paciente()
        
    def editar_paciente(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un paciente para editar.")
            return
            valores = self.tabla.item(seleccionado[0], "values")
            self.formulario_paciente(valores)
            
    def eliminar_paciente(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un paciente para eliminar.")
            return    
        valores =self.tabla.item(seleccionado[0], "values")
        if messagebox.askyesno("confirmar", f"¿Eliminar al Paciente {valores[1]} ?"):
            try:
                self.controller.eliminar(valores[0])
                self.cargar_tabla()
                messagebox.showinfo("Éxito", f"Paciente {valores[1]} eliminado correctamente")
            except Exception as e:
                if '1451' in str(e):
                    messagebox.showerror(
                        "no se puede eliminar",
                        f"No se puede eliminar elñ paciente '{valores[1]}' porque tiene citas asociadas.\nEliminar primero las citas relacionadas."
                    )
                else:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")
    
    def formulario_paciente(self, valores=None):
        win = tb.Toplevel(self.frame)
        win.title("Formulario de Paciente")
        win.geometry("400x380")
        win.resizable(False, False)
        
        form_frame= tb.Frame(win, padding=20)
        form_frame.pack(fill="both", expand=True)
        
        tb.Label(form_frame, text="Por favor ingrese la información del paciente",
                font=("Arial", 11)).grid(row=0, column=0, columnspan=2, pady=(0,15))
                
        nombre = StringVar(value=valores[1] if valores else "")
        sintomas = StringVar(value=valores[2] if valores else SINTOMAS_COMUNES[0])
        telefono = StringVar(value=valores[3] if valores else "")
        direccion = StringVar(value=valores[4] if valores else "")
        estado = StringVar(value=valores[5] if valores else ESTADOS[0])
        
        #Campos del formulario con grid layout
        tb.Label(form_frame, text="nombre").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        tb.Entry(form_frame, textvariable=nombre, width=28).grid(row=1, column=1, pady=5, padx=5)
        
        tb.Label(form_frame, text="síntomas").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        sintomas.cb =tb.Combobox(form_frame, values=SINTOMAS_COMUNES, textvariable=sintomas, state="readonly", width=26)
        sintomas.cb.grid(row=2, column=1, pady=5, padx=5)
        
        tb.Label(form_frame, text="Teléfono").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        tb.Entry(form_frame, textvariable=nombre, width=28).grid(row=3, column=1, pady=5, padx=5)
        
        tb.Label(form_frame, text="Dirección").grid(row=4, column=0, sticky="e", pady=5, padx=5)
        tb.Entry(form_frame, textvariable=nombre, width=28).grid(row=4, column=1, pady=5, padx=5)
        
        tb.Label(form_frame, text="Estado").grid(row=4, column=0, sticky="e", pady=5, padx=5)
        
        estado_cb =tb.Combobox(form_frame, values=ESTADOS, textvariable=estado,state="readonly", width=26)
        estado_cb.grid(row=5, column=1, padx=5, pady=5)
        
        def guardar():
            if not nombre.get() or not sintomas.get() or not telefono.get() or not direccion.get():
                messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
                return
            
            try:
                if valores:
                    self.controller.actualizar(valores[0], nombre.get(), sintomas.get(),
                                        telefono.get(), direccion.get(), estado.get())
                    messagebox.showinfo("Exito", "Paciente actualizado correctamente.")
                else:
                    self.controller.crear(nombre.get(), sintomas.get(),
                                            telefono.get(), direccion.get(), estado.get(), self.usuario_id)
                    messagebox.showinfo("Exito", "Paciente creado correctamente.")
                    win.destroy()
                    self.cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")
                
            #Frame para botones con mejor espaciado
            btn_frame =tb.Frame(form_frame)
            btn_frame.grid(row=6, column=0, columnspan=2, pady=18)
            
            tb.Button(btn_frame, text="Guardar", bootstyle="success",
                    command=guardar, width=12).pack(side="left", padx=8)
            tb.Button(btn_frame, text="Cancelar", bootstyle="danger",
                    command=win.destroy, width=12).pack(side="left", padx=8)