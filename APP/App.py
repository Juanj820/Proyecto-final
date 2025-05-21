import ttkbootstrap as tb
from views.login_view import LoginView
from views.main_view import MainView
from controllers.usuario_controller import UsuarioController

class App:
    def __init__(self):
        self.root = tb.window(themename="morph")
        self.root.title("sistema de Gestion Clinica")

        #Iniciar controladores
        self.usuario_controller = UsuarioController()

        #Inicializar vista de Login
        self.login_view = LoginView(
            self.root,
            self.usuario_controller,
            self.on_login_success
        )
    def on_login_succes(self, user):
        #crear y mostrar la vista principal
        self.main_view = MainView(
            self.root,
            user,
            self.logout
        )    
    def logout(self):
        #Usar el nuevo metodo de logout
        self.login_view.logout()

    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = App()
    app.run()
