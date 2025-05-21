import ttkbootstrap as tb
from tkinter import LEFT, RIGHT, BOTH, X
import tkinter as  tk
import sys
import os
from datetime import datetime
import time

#Agregar el directorio raiz al patch de python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.doctor_controller import DoctorController
from controllers.paciente_controller import PacienteController
from controllers.cita_controller import CitaController

class DashboardView:
    def __init__(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()
        self.parent = parent
        self.frame = tb.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)
        
        #Titulo y colores
        colores =["danger", "warning", "info"]
        iconos =["","",""]
        titulos=["Total Doctores", "Total Pacientes", "Total Citas"]
        #Obtener datos
        total_doctores=DoctorController().contar()
        total_pacientes=PacienteController().contar()
        total_citas=CitaController().contar()
        totales =[total_doctores, total_pacientes, total_citas]
        #Creae estilos personalizzados para los totales

        style =tb.Style()
        style.configure("TotalDanger.TLabel", background="#dc3545", foreground="white", font=("Arial", 14, "bold"), anchor="center")
        style.configure("TotalWarning.TLabel", background="#ffc107", foreground="white", font=("Arial", 14, "bold"), anchor="center")
        style.configure("Totalinfo.TLabel", background="#0dcaf0", foreground="white", font=("Arial", 14, "bold"), anchor="center")
        #footer personalizado
        style.configure("footerAzul.TLabel", background="#007bff", foreground="white", font=("Arial", 10), anchor="center")
        
        #Tarjetas resumen
        cards_frame =tb.Frame(self.frame)
        cards_frame.pack(pady=20)
        for i, (color, icono, titulo, total) in enumerate(zip(colores, iconos, titulos, totales)):
        #card con estilo de color
            card=tb.Frame(cards_frame, style=f"{color}.TFrame", width=220, height=130)
            card.pack(side=LEFT, padx=18)
            card.pack_propagate(False)

            #Obtener color real del estilo
            style = tb.Style()
            card_bg =style.lookup(f"{color}.TFrame", "background")
            if not card_bg or card_bg in ("", "SistemButtonFace", None):
                card_bg ="#dc3545" if color=="danger" else ("#ffc107" if color=="warnig" else "#0dcaf0")
            
            #contenedor principal con padding
            main_frame=tb.Frame(card, style=f"{color}.TFrame")
            main_frame.pack(fill="both", expand= True, padx=10, pady=10)

            #contenedor para el icono
            icon_frame = tb.Frame(main_frame, style=f"{color}.Tframe")
            icon_frame.pack(fill="x", pady=(0,5))

            #icono (mas pequeño)
            tb.Label(icon_frame, text=icono, font=("Arial", 28), 
                    style=f"{color}.inverse.TLavel").pack()
            
            #Contenedor para titulo y total
            info_frame = tb.Frame(main_frame, style=f"{color}.TFrame")
            info_frame.pack(fill="x", padx=(5,0))

            #Titulo
            tb.Label(info_frame,text=titulo, font=("Arial", 11, "bold"),
                    style=f"{color}.inverse.TLabel").pack()
                    
            #Total debajo del titulo con estilo personalizado
            total_frame=tb.Frame(info_frame, style=f"{color}.TFrame")
            total_frame.pack(fill="x", pady=(5,0))
            total_style = "TotalDanger.TLabel" if color=="danger" else ("TotalWarning.TLabel" if color=="Warning" else "TotalInfo.TLabel")
            tb.Label(total_frame, text=str(total), style=total_style).pack(fill="x")

        #Tablas de recientes
        tablas_frame = tb.Frame(self.frame)
        tablas_frame.pack(pady=20, fill=X)

        #Doctores recientes
        doctores =DoctorController().listar(por_pagina=5)
        tabla_doc_frame=tb.Labelframe(tablas_frame, text="Doctores recientes", bootstyle="info")
        tabla_doc_frame.pack(side=LEFT,padx=20, fill=X, expand=True)
        tabla_doc = tb.Treeview(tabla_doc_frame, columns=("nombre", "departamento", "telefono", "estado"), 
                                show="headings", height=6, bootstyle="info")
        tabla_doc.heading("nombre", text="Nombre")
        tabla_doc.heading("departamento", text="Departamento")
        tabla_doc.heading("telefono", text="Telefono")
        tabla_doc.heading("estado", text="Estado")
        tabla_doc.column("nombre", width=120)
        tabla_doc.column("departamento", width=120)
        tabla_doc.column("telefono", width=90)
        tabla_doc.column("estado", width=80)
        tabla_doc.pack(fill=X, padx=5, pady=5)

        for d in doctores:
            tabla_doc.insert("", "end", values=(d["nombre"],d["departamento"],d["telefono"],d["estado"] ))
        
        # Pacientes recientes
        pacientes=PacienteController().listar(por_pagina=5)
        tabla_pac_frame=tb.Labelframe(tablas_frame, text="Pacientes Recientes", bootstyle="info")
        tabla_pac_frame.pack(side=RIGHT, padx=20, fill=X, expand=True)
        tabla_pac = tb.Treeview(tabla_pac_frame, columns=("nombre", "sintomas", "telefono", "direccion", "estado"),
                                show="headings", height=6, bootstyle="info")
        tabla_pac.heading("nombre", text="Nombre")
        tabla_pac.heading("sintomas", text="Sintomas")
        tabla_pac.heading("telefono", text="Telefono")
        tabla_pac.heading("direccion", text="Direccion")
        tabla_pac.heading("estado", text="Estado")
        tabla_pac.column("nombre", width=120)
        tabla_pac.column("sintomas", width=120)
        tabla_pac.column("telefono", width=90)
        tabla_pac.column("direccion", width=120)
        tabla_pac.column("estado", width=80)
        tabla_pac.pack(fill=X, padx=5, pady=5)

        for p in pacientes:
            tabla_pac.insert("", "end", values=(p["nombre"], p["sintomas"], p["telefono"], p["direccion"], p["estado"]))

        #footer
        footer_frame =tb.Frame(self.frame)
        footer_frame.pack(side="bottom", fill=X, pady=10)
        self.footer_label = tb.Label(footer_frame, text="Sistema de gestion Clinica -Dashboard", style="")
        self.footer_label.pack(fill="x")

    def update_footer(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.footer_label.config(
            text=f"Usuario:{self.usuario['nombre']}  Fecha y hora: {now} 2025 Solutiones Tecnologicas"
        )
        self.parent.after(1000, self.update_footer)

        time.sleep(2) #esperar 2 segundos



