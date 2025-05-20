import ttkbootstrap as tb
from tkinter import messagebox
import threading
import time
from PIL import Image, ImageTk
import os

class LoginView:
    def __init__(self, root, usuario_controller, on_login_success):
        self.root =root
        self.usuario_controller = usuario_controller
        self.onlogin_success =on_login_success

         #Configurar tamaño y posicion de la entana login
        self.root.geometry("400x500") #Aumentado el alto para el logo
        self.root.resizable(False, False)#No permitir redimensionar

        #central la ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth()//2) - (width//2)
        y=(self.root.winfo_screenheight()//2) - (height//2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        #Frame principal con padding 
        self.frame = tb.Frame(root, padding=20)
        self.frame.pack(expand=True)

        #Cargar y mostrar el logo
        try:
            #Intentar cargar el logo desde la carpeta assets/images
            logo_path = os.path.join ("assets", "images", "logo_blue.png")
            if not os.path.exists(logo_path):
                #Si no existe, usar el logo por defecto
                logo_path = os.path.join("assets", "images", "logo_blue.png")

            #Cargar y redimensionar la imagen
            logo_img = Image.open(logo_path)
            #Calcular el nuevo tmaño manteniendo la proporcion
            width=200 #Ancho deseado
            ratio = width /logo_img.width
            height = int(logo_img.height * ratio)
            logo_img = logo_img.resize((width, height), Image.Resampling.LANCZOS)

            #Convertir a photoImage
            self.logo_photo = ImageTk.photoImage(logo_img)

            #mostrar el logo
            logo_label = tb.Label(self.frame, image=self.logo_photo)
            logo_label.pack(pady=(0,20))
        except Exception as e:
            print(f"Error al cargar el logo : {e}")

        #Titulo del login
        tb.Label(self.frame, text="Iniciar Sesion:", font=("Arial", 16, "bold"), bootstyle="primary").pack(pady=(0,20))

        #Campos de entrada
        tb.Label(self.frame, text="Usuario:", font=("Arial", 10)).pack(anchor="w", pady=(0,5))
        self.usuario_entry = tb.Entry(self.frame, width=30, font=("Arial", 10))
        self.usuario_entry.pack(pady=(0,10))

        tb.Label(self.frame, text="Contraseña:", font=("Arial", 10)).pack(anchor="w", pady=(0,5))
        self.password_entry = tb.Entry(self.frame, width=30, font=("Arial", 10))
        self.password_entry.pack(pady=(0,20))

        #Boton de login
        tb.Button(self.frame, text="Ingresar", command=self.login, bootstyle="primary", width=20).pack(pady=10)

    def cerrar_aplicacion(self):
        time.sleep(2) # Esperar 2 segundos
        self.root.destroy()#Cerrar la aplicacion completamente
        self.root.quit()#Asegurar que la aplicacion se cierre

    def centrar_ventana(self):
        #Actualizar la ventana para obtener las dimensiones correctas
        self.root.update.idletask()
        #Obtener dimensiones de la ventana
        Width = self.root.winfo_width()
        height = self.root.winfo_height()
        #Calcular posicion x, y para centrar
        x=(self.root.winfo_screenwidth()//2)-(Width//2)
        #Ajustar la posicion vertical para que el footer sea visible
        y=(self.root.winfo_screenheight()//2)-(height//2)-50
        #Centrar la ventana
        self.root.geometry(f'{Width}x{height}+{x}+{y}')
    
    def login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        user = self.usuario_controller.login(usuario, password)
        if user:
            #Destruir el frame de login antes de mostrar el mensaje
            self.frame.destroy()
            #Restaurar el tamaño de la ventana principal
            self.root.geometry("1200x700")
            self.root.resizable(True, True)
            #Centrar la ventana principal
            self.centrar_ventana()
            #Mostrar mensaje de bienvenida y continuar
            messagebox.showinfo("Bienvenido", f"Bienvenido {user['nombre']} al sistema.")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.usuario_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')

    def logout(self):
        #Iniciar el cierre en un hilo separado
        threading.Thread(target=self.cerrar_aplicacion, daemon=True).start()
            
