import ttkbootstrap as tb
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw
import shutil

class MainView(tb.Frame):
    def __init__(self, root, usuario, on_logout):
        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout

        #NAVBAR SUPERIOR (debe ir primero)
        self.navbar = tb.Frame(root, bootstyle="info")
        self.navbar.pack(side="top", fill="x")
        #Logo en ves de texto
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "logo.png")
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((100, 40), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        self.nav_logo = tb.Label(self.navbar, image=self.logo_photo, style="inverse.info.TLabel")
        self.nav_logo.pack(side="left", padx=(20,10), pady=4)
        self.search_frame = tb.Frame(self.navbar, bootstyle="primary")
        self.search_frame.pack(side="left", padx=10, pady=8)
        self.search_var = tk.StringVar()
        self.search_entry = tb.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", ipady=2)
        self.search_entry.insert(0, "Buscar aqui...")
        self.search_btn = tb.Button(self.search_frame, text="🔍", bootstyle="info-outline")
        self.search_btn.pack(side="left", padx=(2,0))
        self.user_menu_btn = tb.Menubutton(self.navbar, text="👤", bootstyle="info", width=4)
        self.user_menu = tk.Menu(self.user_menu_btn, tearoff=0)
        self.user_menu.add_command(label="Mi Perfil", command=self.show_profile)
        self.user_menu.add_command(label="Configuración", command=self.show_settings)
        self.user_menu.add_separator()
        self.user_menu.add_command(label="Cerrar Sesión", command=self.logout)
        self.user_menu_btn["menu"] = self.user_menu
        self.user_menu_btn.pack(side="right", padx=20, pady=4)

        # FRAME PRINCIPAL (sidebar y contenido )
        self.frame = tb.Frame(root)
        self.frame.pack(side="top", fill="both", expand=True)
    
        # Sidebar (Fondo azul primary)
        self.sidebar = tb.Frame(self.frame, width=200, bootstyle="primary")
        self.sidebar.pack(side="left", fill="y")
        #foto de perfil en el sindebar
        foto_path = usuario.get ('foto') or ''
        def make_circle(img_path, size=(80,80)):
            try:
                img = Image.open(img_path).resize(size,Image.LANCZOS).convert("RGBA")
                bigsize = (img.size[0] * 3, img.size[1] * 3)
                mask = Image.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + bigsize, fill=255)
                mask = mask.resize(img.size, Image.LANCZOS)
                img.putalpha(mask)
                bg = Image.new("RGBA", img.size, (255,255,255,0))
                bg.paste(img, (0,0), img)
                return ImageTk.PhotoImage(bg)
            except:
                return None
        self.sidebar_foto = make_circle(foto_path) if foto_path else None
        self.sidebar_foto_label = tb.Label(self.sidebar, image=self.sidebar_foto, style="inverse.primary.Tlabel")
        self.sidebar_foto_label.pack(pady=(20,5))
        tb.Label(self.sidebar, text=f"{usuario['nombre']}", font=("Arial", 10, "bold"), style="inverse.primary.Tlabel").pack(pady=10)
        #Linea sepadora tipo hr
        tk.Frame(self.sidebar, height=2, bg="#e0e0e0", relief="flat").pack(fill="x", padx=16, pady=(0,10))
        # --- OPCION 1: Menu con frames y labels alineados a la izquierda, simulando botones ---
        def crear_menu_sidebar(parent, icono, texto, comando):
            f = tk.Frame(parent, bg='#2563eb')
            f.pack(fill="x", padx=16, pady=2)
            lbl = tb.Label(f, text=f,"{icono} {texto}", font=("Arial", 10), bg='#2563eb', fg='white', anchor="w", padx=8)
            lbl.pack(fill="x") 
            def on_enter(e):
                lbl.config(bg="#1e40af", fg="ffffff")
            def on_leave(e):
                lbl.config(bg="#2563eb")
            def on_click(e):
                comando()
            lbl.bind("<Enter>", on_enter)
            lbl.bind("<Leave>", on_leave)
            lbl.bind("<Button-1>", on_click)
            return f
        crear_menu_sidebar(self.sidebar, "🏠", "Dashboard", self.show_dashboard)
        crear_menu_sidebar(self.sidebar, "🩺", "Doctores", self.show_doctores)
        crear_menu_sidebar(self.sidebar, "👨‍👩‍👧‍👦", "Pacientes", self.show_pacientes)
        crear_menu_sidebar(self.sidebar, "📅", "Citas", self.show_citas)
        # --- FIN OPCIÓN 1 ---
        # --- OPCIÓN 2: Botones clásicos (comentados para revertir si se desea) ---
        # tb.Button(self.sidebar, text="🏠 Dashboard", command=self.show_dashboard, bootstyle="primary").pack(fill="x", pady=2, padx=16)
        # tb.Button(self.sidebar, text="🩺 Doctores", command=self.show_doctores, bootstyle="primary").pack(fill="x", pady=2, padx=16)
        # tb.Button(self.sidebar, text="👨‍👩‍👧‍👦 Pacientes", command=self.show_pacientes, bootstyle="primary").pack(fill="x", pady=2, padx=16)
        # tb.Button(self.sidebar, text="📅 Citas", command=self.show_citas, bootstyle="primary").pack(fill="x", pady=2, padx=16)
        tb.Button(self.sidebar, text="Salir", command=self.logout, bootstyle="primary").pack(fill="x", pady=20, padx=16)

        # Main content
        self.content = tb.Frame(self.frame)
        self.content.pack(side="left", fill="both", expand=True)
        self.show_dashboard()

        #Footer (Azul oscuro)
        self.footer = tb.Frame(root, bootstyle="dark")
        self.footer.pack(side="bottom", fill="x")
        self.footer_left = tb.Label(self.footer, text="", style="inverse.dark.TLabel", anchor="w")
        self.footer_left.pack(side="left", fill="x", expand=True, padx=(20,0), pady=8) 
        self.footer_center = tb.Label(self.footer, text="", style="inverse.dark.TLabel", anchor="center")
        self.footer_center.pack(side="left", fill="x", expand=True, pady=8)
        self.footer_right = tb.Label(self.footer, text="", style="inverse.dark.TLabel", anchor="e")
        self.footer_right.pack(side="left", fill="x", expand=True, padx=(0,20), pady=8) 
        self.update_footer()

def show_dashboard(self):
    for widget in self.content.winfo_children():
        widget.destroy()
    from views.dashboard_view import DashboardView
    DashboardView(self.content)

def show_doctores(self):
    for widget in self.content.winfo_children():
        widget.destroy()
    from controllers.doctor_controller import DoctorController
    from views.doctor_view import DoctorView
    DoctorView(self.content, DoctorController(), self.usuario['id'])

def show_pacientes(self):
    for widget in self.content.winfo_children():
        widget.destroy()
    from controllers.paciente_controller import PacienteController
    from views.paciente_view import PacienteView
    PacienteView(self.content, PacienteController(), self.usuario['id'])

def show_citas(self):
    for widget in self.content.winfo_children():
        widget.destroy()
    from controllers.cita_controller import CitaController
    from views.cita_view import CitaView
    CitaView(self.content, CitaController(), self.usuario['id'])

def logout(self):
    try:
        messagebox.showinfo("Hasta pronto", f"Hasta pronto, {self.usuario['nombre']}")
        #Destruir todos los widgests antes de cerrar sesion
        if hasattr(self, 'footer'):
            self.footer.destroy()
        if hasattr(self, 'frame'):
            self.frame.destroy()
        if hasattr(self, 'navbar'):
            self.navbar.destroy()
        #llamar a on_logout que reiniciara la aplicacion
        self.on_logout()
    except Exception as e:
        print(f"Error al cerrar sesión: {e}")
        #Forzar el reinicio de la aplicacion
        self.on_logout()

def update_footer (self):
    try:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.footer_left.config(text=f"Usuario: {self.usuario['nombre']}")
        self.footer_center.config(text="© 2025 Soluciones Tecnológicas")
        self.footer_right.config(text=f"{now}")
        self.root.after(1000, self.update_footer)
    except:
        # Si la ventana se ha ddestruido, no hacemos nada 
        pass

    def show_profile(self):
        messagebox.showinfo("Mi Perfil", f"Usuario: {self.usuario['nombre']}")

    def show_settings (self):
        from controllers.usuario_controller import UsuarioController
        user = self.usuario
        win = tk.Toplevel(self.root)
        win.title("Configuración de usuario")
        win.geometry("350x500")
        win.resizable(False, False)
        #Foto de perfil
        foto_path = user.get ('foto') or ''
        img_frame = tk.Frame(win)
        img_frame.pack(pady=(10,0))
        def cargar_img(path):
            try:
                img = Image.open(path)
                img = img.resize((80,80), Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except:
                return None
        self.foto_actual = cargar_img(foto_path) if foto_path else None
        self.foto_label = tk.Label(img_frame, image=self.foto_actual)
        self.foto_label.pack()
        def seleccionar_foto():
            from tkinter import filedialog
            file = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg;*.gif")])
            if file:
                img = cargar_img(file)
                if img:
                    self.foto_label.configure(image=img)
                    self.foto_label.image = img
                    self.nueva_foto = file
        self.nueva_foto = None
        tk.Button(img_frame, text="Cambiar foto", command=seleccionar_foto).pack(pady=4)
        # Etiquetas y campos
        tk.Label(win, text="Nombre:").pack(anchor="w", padx=20, pady=(20,0))
        nombre_var = tk.StringVar(value=user['nombre'])
        tk.Entry(win, textvariable=nombre_var).pack(fill="x", padx=20)
        tk.Label(win, text="Usuario:").pack(anchor="w", padx=20, pady=(10,0))
        usuario_var = tk.StringVar(value=user['usuario'])
        tk.Entry(win, textvariable=usuario_var).pack(fill="x", padx=20)
        tk.Label(win, text="Contraseña (dejar vacío para no cambiar):").pack(anchor="w", padx=20, pady=(10,0))
        password_var = tk.StringVar()
        tk.Entry(win, textvariable=password_var, show="*").pack(fill="x", padx=20)
        # Solo lectura: rol y fechas
        tk.Label(win, text=f"Rol: {user.get('rol', '')} (no editable)").pack(anchor="w", padx=20, pady=(10,0))
        tk.Label(win, text=f"Creado en: {user.get('creado_en', '')}").pack(anchor="w", padx=20, pady=(2,0))
        tk.Label(win, text=f"Actualizado en: {user.get('actualizado_en', '')}").pack(anchor="w", padx=20, pady=(2,0))
        # Botón guardar
        def guardar():
            nombre = nombre_var.get().strip()
            usuario_nuevo = usuario_var.get().strip()
            password = password_var.get().strip()
            foto_final = user.get('foto')
            if self.nueva_foto:
                ext = os.path.splitext(self.nueva_foto)[1]
                nombre_archivo = f"user_{user['id']}{ext}"
                destino = os.path.join("assets", "images", "perfiles", nombre_archivo)
                shutil.copy2(self.nueva_foto, destino)
                foto_final = destino.replace("\\", "/")
            if not nombre or not usuario_nuevo:
                messagebox.showerror("Error", "Nombre y usuario son obligatorios.")
                return
            try:
                UsuarioController().actualizar(user['id'], nombre, usuario_nuevo, password if password else None, foto_final)
                self.usuario['nombre'] = nombre
                self.usuario['usuario'] = usuario_nuevo
                self.usuario['foto'] = foto_final
                messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")
        tk.Button(win, text="Guardar", command=guardar).pack(pady=20)
