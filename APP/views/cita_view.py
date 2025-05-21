import ttkbootstrap as tb
from tkinter import messagebox, StringVar, IntVar
from controllers.doctor_controller import DoctorController
from controllers.paciente_controller import PacienteController
import datetime

ESTADOS = ["Promamada", "En consulta", "Finalizada", "Cancelada", "No asistío", "Aprobada", "Pendiente"]

class CitaView:
    def __init__(self, parent, controller,usuario_id):
        self.parent =parent
        self.controller = controller
        self.usuario_id = usuario_id
        self.pagina = 1
        self.por_pagina = 5
        self.busqueda = StringVar()
        self.busqueda_estado =StringVar(value="")
        self.total_paginas = 1
        self.total_registros = 0

        self.frame = tb.Frame (parent)
        self.frame.pack(fill="both", expand=True)
        tb.Label(self.frame, text ="Gestión de citas", font=("Arial", 18, "bold"), bootstyle="primary").pack(pady=10)

        #busqueda
        busq_frame =tb.Frame(self.frame)
        busq_frame.pack(pady=5)
        tb.Label(busq_frame, text="Buscar:").pack(side="left")
        self.busq_entry = tb.Entry(busq_frame, textvariable=self.busqueda)
        self.busq_entry.pack(side="left", padx=5)
        tb.Label(busq_frame, text ="Estado:").pack(side="left", padx=5)
        self.estado_cb = tb.Combobox(busq_frame, value=["",*ESTADOS], textvariable=self.busqueda_estado, width=14, state="readonly")
        self.estado_cb.pack(side="left")
        tb.Button(busq_frame, text="Buscar", bootstyle="success", command=self.buscar).pack(side="left", padx=5)

        # Contenedor principal para tabla y botones
        main_container = tb.Frame(self.frame)
        main_container.pack(fill="both", expand=True, padx=30, pady=5)

        # Tabla con espaciado lateral
        tabla_frame = tb.Frame(main_container)
        tabla_frame.pack(side="left", fill="both", expand=True, padx=(20, 20))
        self.tabla = tb.Treeview(tabla_frame, columns=("id", "id_doctor", "doctor", "id_paciente", "paciente", "fecha", "estado"), show="headings", height=7, bootstyle="info")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("id_doctor", text="ID Doctor")
        self.tabla.heading("doctor", text="Doctor")
        self.tabla.heading("id_paciente", text="ID Paciente")
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("fecha", text="Fecha y Hora")
        self.tabla.heading("estado", text="Estado")
        self.tabla.column("id", width=40)
        self.tabla.column("id_doctor", width=0, stretch=False)
        self.tabla.column("doctor", width=120)
        self.tabla.column("id_paciente", width=0, stretch=False)
        self.tabla.column("paciente", width=120)
        self.tabla.column("fecha", width=140)
        self.tabla.column("estado", width=110)
        self.tabla.pack(pady=10, fill="x")

        # LabelFrame para botones a la derecha, igualando el alto de la tabla
        btns_frame = tb.Labelframe(main_container, text="Acciones", bootstyle="info")
        btns_frame.pack(side="left", fill="y", padx=(10, 0), pady=10, expand=False)
        btns_frame.update_idletasks()
        tabla_height = self.tabla.winfo_reqheight()
        btns_frame.config(height=tabla_height)

        #Botones de accion con menor espacio entre ellos
        tb.Button(btns_frame, text="Nueva Cita", bootstyle="info", command=self.nueva_cita, width=16).pack(pady=6, padx=16)
        tb.Button(btns_frame, text="Editar", bootstyle="warning", command=self.editar_cita, width=16).pack(pady=6, padx=16)
        tb.Button(btns_frame, text="Eliminar", bootstyle="danger", command=self.eliminar_cita, width=16).pack(pady=6, padx=16)

        pag_frame =tb.Frame(self.frame)
        pag_frame.pack(20 , 10)
        self.lbl_pagina =tb.Label(pag_frame, text="")
        self.lbl_pagina.pack(side="left", padx=5)
        tb.Button(pag_frame, text="Anterior", bootstyle="secondary", command=self.pagina_anterior, width=16).pack(side="left", padx= 5)
        tb.Button(pag_frame, text="Siguiente", bootstyle="secondary", command=self.pagina_siguiente, width=16).pack(side="left", padx= 5)
        self.lbl_total=tb.label(pag_frame, text="")
        self.lbl_total.pack(side="left", padx=15)

        self.cargar_tabla()
    def buscar(self):
        self.pagina = 1
        self.cargar_tabla()

    def cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        busq = self.busqueda.get()
        estado = self.busqueda_estado.get()
        citas = self.controller.listar(busq, estado, self.pagina, self.por_pagina)
        for cita in citas:
            self.tabla.insert("", "end", values=(
                cita["id"],
                cita["id_doctor"],
                cita["doctor"],
                cita["id_paciente"],
                cita["paciente"],
                cita["fecha"],
                cita["estado"],
            ))
#Calcular total de paginas y registros
        total= self.controller.contar(busq, estado)
        self.total_registros =total
        self.total_paginas = max(1, (total + self.por_pagina -1)//self.por_pagina)
        self.lbl_pagina.config(text=f"pagina{self.pagina} de {self.total_paginas}")
        self.lbl_total.config(text=f"Total registros: {self.total_registros}")

    def pagina_anterior(self):
        if self.pagina > 1:
            self.pagina -=1
            self.cargar_tabla()
            

    def pagina_siguiente(self):            
        if self.pagina < self.total_paginas:
            self.pagina +=1
            self.cargar_tabla()

    def nueva_cita(self):
        self.formulario_cita()

    def editar_cita(self):
        seleccionado =self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione una cita para editar.")
            return
        valores =self.tabla.item(seleccionado[0], "values")
        #Convertir a diccionario para compatibilidad con el formulario
        valores_dict = {
            'id': valores[0],
            'id_doctor': valores[1],
            'doctor': valores[2],
            'id_paciente': valores[3],
            'paciente': valores[4],
            'fecha': valores[5],
            'estado': valores[6]     
        }
        self.formulario_cita(valores_dict)

    def eliminar_cita(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione una cita para eliminar")
            return
        valores = self.tabla.item(seleccionado[0], "values")
        if messagebox.askyesno("Confirma", f"¿Eliminar la cita de {valores[4]} con {valores[2]}?"):
            try:
                self.controller.eliminar(valores[0])
                self.cargar_tabla()
                messagebox.showwarning("Exito", "Cita elminidada correctamente.")
            except Exception as e:
                messagebox.showwarning("Error", f"No se puede eliminar:{e}")
        
    def formulario_cita(self, valores=None):
        win=tb.Toplevel(self.frame)
        win.title("Formulario de Cita")
        win.geometry("450x500") 
        win.resizable(False, False)

        form_frame =tb.Frame(win, padding =20)
        form_frame.pack(fill="both", expand=True)

        tb.Label(form_frame, text="Por favor ingrese la informacion de la cita", font=("Aral", 11)).grid(row=0, column=0, columnspan=2, pady=(0,15))
        #Crear diccionario para mapear id a texto

        doctores = DoctorController().listar(por_pagina=1000)
        pacientes = PacienteController().listar(por_pagina=1000)
        doctores_dict = {str(d['id']): f"{d['nombre']} ({d['departamento']})" for d in doctores}
        pacientes_dict = {str(p['id']): f"{p['nombre']}" for p in pacientes}     
        listar_doctores_nombres = [f"{d['nombre']} ({d['departamento']})" for d in doctores]    
        listar_pacientes_nombres = [f"{p['nombre']}" for p in pacientes]
        listar_doctores_ids = [str(d['id']) for d in doctores]
        listar_pacientes_ids =[str(p['id']) for p in pacientes]

        #Variables
        id_doctor = StringVar()
        id_paciente=StringVar()
        fecha = StringVar(value=datetime.date.today().Strftime("%Y-%m-%d"))
        hora = StringVar(value="08:00:00")
        estado=StringVar(value=ESTADOS[0])

        #Campos del formulario con grid layout

        tb.Label(form_frame, text="Doctor:").grid(row=1, column=0, sticky="e", pady=5, padx=5 )
        doctor_cb =tb.Combobox(form_frame, Values=listar_doctores_nombres, state="readonly", width=28)
        doctor_cb.grid(row=1, column=1, pady=5, padx=5)

        tb.Label(form_frame, text="Paciente:").grid(row=2, column=0, sticky="e",pady=5,padx=5 )
        paciente_cb= tb.Combobox(form_frame, Values=listar_pacientes_nombres, state="readonly", width=28)
        paciente_cb.grid(row=2, column=1, pady=5, padx=5)
        
        tb.Label(form_frame, text="Fecha:").grid(row=3, column=0, sticky="e",pady=5,padx=5 )
        fecha_entry = tb.Entry(form_frame, textvariable=fecha, width=28)
        fecha_entry.grid(row=3, column=1, pady=5, padx=5)
        tb.Label(form_frame, text="(YYYY-MM-DD)").grid(row=3, column=2, sticky="w", pady=5)

        tb.Label(form_frame, text="Hora:").grid(row=4, column=0, sticky="e",pady=5,padx=5 )
        hora_entry =tb.Entry(form_frame, textvariable=hora, width=28)
        hora_entry.grid(row=4, column=1, pady=5, padx=5)
        tb.Label(form_frame, text="(HH-MM-SS)").grid(row=4, column=2,sticky="w", pady=5, padx=5)

        tb.Label(form_frame, text="Estado:").grid(row=5, column=0, sticky="e",pady=5,padx=5 )
        estado_cb =tb.Combobox(form_frame, Values=ESTADOS, textvariable=estado, state="readonly", width=28)
        estado_cb.grid(row=5, column=1, pady=5, padx=5)
       
        #Busqueda rapida de pacientes
        def on_paciente_key(event):
            texto = paciente_cb.get().lower()
            filtrados =[p['nombre'] for p in pacientes if texto in p['nombre'].lower()]
            paciente_cb['values'] = filtrados if filtrados else listar_pacientes_nombres
        paciente_cb.bind('<KeyRelease>', on_paciente_key)

        #Inicializacion de valores

        if valores:
            doctor_id = str(valores.get('id_doctor'))
            paciente_id =str(valores.get('id_paciente'))
             #Seleccionar doctor por ID
            if doctor_id in doctores_dict:
                doctor_cb.set(doctores_dict[doctor_id])
                id_doctor.set(doctor_id)
            else:
                doctor_cb.set(listar_doctores_nombres[0] if listar_doctores_nombres else "")
                id_doctor.set(listar_doctores_ids[0] if listar_pacientes_ids else "")
            
            #Seleccionar paciente por ID
            if paciente_id in pacientes_dict:
                paciente_cb.set(pacientes_dict[paciente_id])
                id_paciente.set(doctor_id)
            else:
                paciente_cb.set(listar_pacientes_nombres[0] if listar_pacientes_nombres else "")
                id_paciente.set(listar_pacientes_ids[0] if listar_pacientes_ids else "") 
            #Fecha y hora
            fecha_valor= valores.get('fecha', '') 
            if fecha_valor:
                try:
                    partes=fecha_valor.split('')
                    if len(partes) >= 2:
                        fecha.set(partes[0])
                        hora.set(partes[1])
                    else:
                        fecha .set(datetime.date.today().strftime("%Y-%m-%d"))
                        hora.set("08:00:00") 
                except:
                    fecha .set(datetime.date.today().strftime("%Y-%m-%d"))
                    hora.set("08:00:00")  
            #Estado
            estado_valor = valores.get('estado', '')
            if estado_valor in ESTADOS:
                estado.set(estado_valor)
            else:
                estado.set(ESTADOS[0])
        else:
            doctor_cb.set(listar_doctores_nombres [0] if listar_doctores_nombres else "")
            id_doctor.set(listar_doctores_ids[0] if listar_doctores_ids else "")
            paciente_cb.set(listar_pacientes_nombres [0] if listar_pacientes_nombres else "")
            id_paciente.set(listar_pacientes_ids[0] if listar_pacientes_ids else "")
        
        #Sincronizar seleccion de combobox con variable id
        def on_doctor_select(event):
            nombre = doctor_cb.get()
            for did, texto in doctores_dict.items():
                if texto == nombre:
                    id_doctor.set(did)
                    break
        doctor_cb.bind('<<ComboboxSelected>>', on_doctor_select)

        def on_paciente_select(event):
            nombre =paciente_cb.get()
            for did, texto in pacientes_dict.items():
                if texto == nombre:
                    id_paciente.set(did)
                    break
        paciente_cb.bind('<<ComboboxSelected>>', on_paciente_select)

        def validar_fecha(fecha_str):
            try:
                datetime.datetime.strftime(fecha_str, "%Y:%m:%d")
                return True
            except ValueError:
                return False
        def validar_hora(hora_str):
            try:
                datetime.datetime.strftime(hora_str, "%H:%M:%S")
                return True
            except ValueError:
                return False
               
        def guardar():
            if not id_doctor.get() or not id_paciente.get() or not fecha.get() or not hora.get():
                messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
                return
            if not validar_fecha(fecha.get()):
                messagebox.showwarning("Aviso", "Formato de fecha invalido. use YYYY-MM-DD")
                return
            if not validar_hora(hora.get()):
                messagebox.showwarning("Aviso", "Formato de hora invalido. use HH:MM:SS")
                return
            try:
                fecha_hora = f"{fecha.get()} {hora.get()}"
                if valores:
                    self.controller.actualizar(
                        valores['id'],
                        id_doctor.get(),
                        id_paciente.get(),
                        fecha_hora,
                        estado.get()
                    )
                    messagebox.showwarning("Exito", "Cita actualizada correctamente.")
                else:
                    self.controller.crear(
                        id_doctor.get(),
                        id_paciente.get(),
                        fecha_hora,
                        estado.get()
                    )
                    messagebox.showwarning("Exito", "Cita creada correctamente.")
                win.destroy()
                self.cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", f"Nose puede guardar: {e}")
        
        #Frame para botones con mejor espaciado
        btn_frame = tb.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=18)

        tb.Button(btn_frame, text="Guardar", bootstyle="Success", 
                  command=guardar, width=12).pack(side="left", padx=8)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger", 
                  command=win.destroy, width=12).pack(side="left", padx=8)
             



            


