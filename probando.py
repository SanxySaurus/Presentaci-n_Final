import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

class WelcomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clínica ECG")
        self.geometry("430x932")
        self.configure(bg="white")

        self.create_header()
        self.create_logo_text()
        self.create_login_section()
        self.create_footer()

    def create_header(self):
        """Encabezado con imagen médica"""
        try:
            img_header = Image.open("Encabezado.png").resize((430, 250))
            self.header_img = ImageTk.PhotoImage(img_header)
            lbl_header = tk.Label(self, image=self.header_img, bg="white")
            lbl_header.pack()
        except:
            lbl_header = tk.Label(self, bg="#003366", width=430, height=12)
            lbl_header.pack()

    def create_logo_text(self):
        """Logo y nombre de la clínica"""
        try:
            img_logo = Image.open("logo.webp").resize((180, 120))
            self.logo_img = ImageTk.PhotoImage(img_logo)
            lbl_logo = tk.Label(self, image=self.logo_img, bg="white")
            lbl_logo.pack(pady=(40, 10))
        except:
            lbl_name = tk.Label(self, text="CLÍNICA ECG", font=("Arial", 22, "bold"), fg="#0047AB", bg="white")
            lbl_name.pack(pady=(40, 10))

        lbl_sub = tk.Label(self, text="Bienvenido a tu clínica de confianza", font=("Arial", 12), bg="white")
        lbl_sub.pack(pady=(0, 30))

    def create_login_section(self):
        """Botón principal e hipervínculo"""
        btn_ingresar = tk.Button(self, text="Ingresar", font=("Arial", 14, "bold"),
                                 bg="#3366CC", fg="white", width=20, height=2,
                                 bd=0, relief="flat", command=self.on_login)
        btn_ingresar.pack(pady=10)

        # 🔹 Texto: ¿Aún no tienes una cuenta? Regístrate aquí
        frame_text = tk.Frame(self, bg="white")
        frame_text.pack(pady=(10, 30))

        lbl_text = tk.Label(frame_text, text="¿Aún no tienes una cuenta? ", font=("Arial", 10), bg="white")
        lbl_text.pack(side="left")

        lbl_link = tk.Label(frame_text, text="Regístrate aquí", font=("Arial", 10, "underline"),
                            fg="#FF9900", bg="white", cursor="hand2")
        lbl_link.pack(side="left")
        lbl_link.bind("<Button-1>", lambda e: self.on_register())

    def create_footer(self):
        """Texto legal inferior"""
        lbl_terms = tk.Label(self, text="Al registrarte aceptas nuestros Términos y Condiciones,\n"
                                        "y nuestra Política de Privacidad.",
                             font=("Arial", 8), bg="white", fg="gray")
        lbl_terms.pack(side="bottom", pady=20)

    def on_login(self):
        """Abrir nueva ventana de selección de rol"""
        self.withdraw()
        RoleSelection(self)

    def on_register(self):
        print("Registro de nuevo usuario")


class RoleSelection(tk.Toplevel):
    """Ventana de selección de rol"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Seleccionar Rol")
        self.geometry("430x932")
        self.configure(bg="white")

        self.create_header()
        self.create_back_button()
        self.create_buttons()
        self.create_footer()

    def create_header(self):
        """Encabezado"""
        try:
            img_header = Image.open("Encabezado.png").resize((430, 250))
            self.header_img = ImageTk.PhotoImage(img_header)
            lbl_header = tk.Label(self, image=self.header_img, bg="white")
            lbl_header.pack()
        except:
            lbl_header = tk.Label(self, bg="#003366", width=430, height=12)
            lbl_header.pack()

    def create_back_button(self):
        """Botón de volver"""
        btn_back = tk.Button(self, text="←", font=("Arial", 20, "bold"),
                             bg="#0047AB", fg="white", bd=0, relief="flat",
                             cursor="hand2", command=self.go_back)
        btn_back.place(x=380, y=10, width=40, height=40)

    def create_buttons(self):
        """Botones de rol"""
        btn_style = {"font": ("Arial", 14, "bold"),
                     "bg": "#3366CC",
                     "fg": "white",
                     "width": 20,
                     "height": 2,
                     "bd": 0,
                     "relief": "flat"}

        tk.Button(self, text="Administrador", **btn_style,
                  command=lambda: self.select_role("Administrador")).pack(pady=20)
        tk.Button(self, text="Doctor", **btn_style,
                  command=lambda: self.select_role("Doctor")).pack(pady=20)
        tk.Button(self, text="Paciente", **btn_style,
                  command=lambda: self.select_role("Paciente")).pack(pady=20)

    def create_footer(self):
        lbl_terms = tk.Label(self, text="Al registrarte aceptas nuestros Términos y Condiciones,\n"
                                        "y nuestra Política de Privacidad.",
                             font=("Arial", 8), bg="white", fg="gray")
        lbl_terms.pack(side="bottom", pady=20)

    def go_back(self):
        self.destroy()
        self.parent.deiconify()


    def select_role(self, role):
        self.withdraw()
        LoginWindow(self, role)


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, role):
        super().__init__(parent)
        self.role = role
        self.parent = parent
        self.title(f"Inicio de sesión - {role}")
        self.geometry("430x932")
        self.configure(bg="white")

        self.create_header()
        self.create_back_button()
        self.create_login_form()

    def create_header(self):
        try:
            img_header = Image.open("Encabezado.png").resize((430, 250))
            self.header_img = ImageTk.PhotoImage(img_header)
            lbl_header = tk.Label(self, image=self.header_img, bg="white")
            lbl_header.pack()
        except:
            lbl_header = tk.Label(self, bg="#003366", width=430, height=12)
            lbl_header.pack()

    def create_back_button(self):
        btn_back = tk.Button(self, text="←", font=("Arial", 20, "bold"),
                             bg="#0047AB", fg="white", bd=0, relief="flat",
                             cursor="hand2", command=self.go_back)
        btn_back.place(x=380, y=10, width=40, height=40)

    def create_login_form(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20)

        # Etiqueta usuario
        lbl_user = tk.Label(frame, text="Escribe tu usuario", font=("Arial", 10, "bold"),
                            fg="black", bg="white")
        lbl_user.pack(anchor="w", padx=40)

        self.entry_user = tk.Entry(frame, font=("Arial", 12), width=30, fg="black", bd=1, relief="solid")
        self.entry_user.pack(pady=5, ipady=5)

        self.lbl_error = tk.Label(frame, text="", fg="red", bg="white", font=("Arial", 9))
        self.lbl_error.pack(anchor="w", padx=40)

        lbl_forgot_user = tk.Label(frame, text="¿Olvidaste tu usuario?", font=("Arial", 9),
                                   fg="#3366CC", bg="white", cursor="hand2")
        lbl_forgot_user.pack(anchor="e", padx=40)

        # Contraseña
        lbl_pass = tk.Label(frame, text="Contraseña", font=("Arial", 10, "bold"),
                            fg="black", bg="white")
        lbl_pass.pack(anchor="w", padx=40, pady=(10, 0))

        self.entry_pass = tk.Entry(frame, font=("Arial", 12), show="*", width=30, fg="black", bd=1, relief="solid")
        self.entry_pass.pack(pady=5, ipady=5)

        lbl_forgot_pass = tk.Label(frame, text="¿Olvidaste tu contraseña?", font=("Arial", 9),
                                   fg="#3366CC", bg="white", cursor="hand2")
        lbl_forgot_pass.pack(anchor="e", padx=40, pady=(5, 20))

        btn_login = tk.Button(frame, text="Inicia sesión", font=("Arial", 13, "bold"),
                              bg="#3366CC", fg="white", width=25, height=2,
                              bd=0, relief="flat", command=self.check_login)
        btn_login.pack(pady=10)

        lbl_register = tk.Label(frame, text="¿Aún no tienes una cuenta? ",
                                font=("Arial", 9), bg="white")
        lbl_register.pack(side="left", padx=(60, 0), pady=10)

        lbl_link = tk.Label(frame, text="Regístrate aquí", font=("Arial", 9, "underline"),
                            fg="#FF9900", bg="white", cursor="hand2")
        lbl_link.pack(side="left")

    def check_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        # Ejemplo de validación (aquí luego conectas tu JSON)
        if username != "admin" or password != "1234":
            self.lbl_error.config(text="¡Usuario incorrecto!", fg="red")
            self.entry_user.config(highlightbackground="red", highlightcolor="red", fg="red")
        else:
            self.lbl_error.config(text="Acceso correcto", fg="green")

    def go_back(self):
        self.destroy()
        self.parent.deiconify()

def run():
    print("Iniciando la aplicación GUI")
    app = WelcomeApp()
    app.mainloop()


if __name__ == "__main__":
    app = WelcomeApp()
    app.mainloop()
