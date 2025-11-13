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
        print(f"Rol seleccionado: {role}")

def run():
    print("Iniciando la aplicación GUI")
    app = WelcomeApp()
    app.mainloop()

if __name__ == "__main__":
    app = WelcomeApp()
    app.mainloop()
