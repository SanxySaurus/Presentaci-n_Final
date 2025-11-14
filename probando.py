import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
import json
from tkinter import messagebox
from tkinter import ttk


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

        if self.role == "Administrador":
            # Abrir panel de administración directamente
            self.destroy()
            self.parent.destroy()  # Cerramos ventana de selección de rol
            AdminFunciones(None)
        elif self.role == "Doctor":
            # Aquí puedes abrir un panel de doctor (por ahora solo mensaje)
            self.lbl_error.config(text="Acceso correcto Doctor", fg="green")
        else:
            if username == "" or password == "":
                self.lbl_error.config(text="¡Usuario o contraseña vacíos!", fg="red")
            else:
                self.lbl_error.config(text="Acceso correcto Paciente", fg="green")


    def go_back(self):
        self.destroy()
        self.parent.deiconify()


USERS_FILE = os.path.join(os.path.dirname(__file__), "usuarios.json")

class AdminJSON:
    """Clase que maneja la gestión de usuarios en usuarios.json"""

    @staticmethod
    def cargar_usuarios():
        """Carga la lista de usuarios desde el JSON"""
        if not os.path.exists(USERS_FILE):
            return []
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
                if not isinstance(usuarios, list):
                    return []
                return usuarios
        except Exception:
            return []

    @staticmethod
    def guardar_usuarios(usuarios):
        """Guarda la lista de usuarios en el JSON"""
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=4)

    @classmethod
    def crear_usuario(cls, usuario):
        """
        Agrega un nuevo usuario.
        usuario: dict con campos 'nombre', 'documento', 'telefono', 'rol', 'edad', 'peso'
        """
        usuarios = cls.cargar_usuarios()
        # Evitar duplicado por documento
        if any(u.get("documento") == usuario.get("documento") for u in usuarios):
            return False, "Ya existe un usuario con ese documento."
        usuarios.append(usuario)
        cls.guardar_usuarios(usuarios)
        return True, "Usuario registrado correctamente."

    @classmethod
    def actualizar_usuario(cls, documento, nuevos_datos):
        """
        Actualiza un usuario existente por documento.
        nuevos_datos: dict con los campos a actualizar
        """
        usuarios = cls.cargar_usuarios()
        for idx, u in enumerate(usuarios):
            if u.get("documento") == documento:
                usuarios[idx].update(nuevos_datos)
                cls.guardar_usuarios(usuarios)
                return True, "Datos actualizados correctamente."
        return False, "Usuario no encontrado."

    @classmethod
    def eliminar_usuario(cls, documento):
        """
        Elimina un usuario por documento
        """
        usuarios = cls.cargar_usuarios()
        for idx, u in enumerate(usuarios):
            if u.get("documento") == documento:
                usuarios.pop(idx)
                cls.guardar_usuarios(usuarios)
                return True, "Usuario eliminado correctamente."
        return False, "Usuario no encontrado."

    @classmethod
    def listar_usuarios(cls):
        """
        Retorna la lista completa de usuarios
        """
        return cls.cargar_usuarios()
class AdminCrearModern(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Crear Usuario")
        self.geometry("430x600")
        self.configure(bg="#1B2A47")  # Fondo similar a la imagen

        # Tarjeta superior con ECG
        top_frame = tk.Frame(self, bg="#2A3B5F", height=150)
        top_frame.pack(fill="x")
        tk.Label(top_frame, text="CLINIC ECG", fg="white", bg="#2A3B5F",
                 font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(top_frame, text="📈", bg="#2A3B5F", fg="cyan", font=("Arial", 40)).pack()

        # Frame principal de formulario
        form_frame = tk.Frame(self, bg="#1B2A47", padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)

        labels = ["Nombre completo", "Número de documento", "Teléfono", "Rol", "Edad", "Peso"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg="#1B2A47", fg="white").grid(row=i, column=0, sticky="w", pady=5)
            if text == "Rol":
                combo = tk.Combobox(form_frame, values=["Administrador","Doctor","Paciente"])
                combo.grid(row=i, column=1, pady=5, sticky="ew")
                self.entries[text] = combo
            else:
                entry = tk.Entry(form_frame)
                entry.grid(row=i, column=1, pady=5, sticky="ew")
                self.entries[text] = entry

        form_frame.columnconfigure(1, weight=1)

        # Botón Registrar usuario
        btn = tk.Button(self, text="Registrar usuario", bg="#00AEEF", fg="white",
                        font=("Arial", 12, "bold"), command=self.guardar_usuario)
        btn.pack(pady=20, ipadx=10, ipady=5)

        tk.Button(self, text="Volver", command=self.volver).pack()

    def guardar_usuario(self):
        messagebox.showinfo("Info", "Aquí se registraría el usuario")

    def volver(self):
        self.destroy()
        self.parent.deiconify()


class AdminCrear(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Crear Usuario")
        self.geometry("430x500")
        self.configure(bg="white")

        tk.Label(self, text="Registrar Nuevo Usuario", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(self, bg="white")
        frame.pack(pady=10, padx=10)

        labels = ["Nombre", "Documento", "Teléfono", "Rol", "Edad", "Peso"]
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(frame, text=text+":", bg="white").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[text] = entry

        tk.Button(self, text="Guardar", bg="#3366CC", fg="white", width=20,
                  command=self.guardar_usuario).pack(pady=10)
        tk.Button(self, text="Cancelar", command=self.volver).pack()

    def guardar_usuario(self):
        usuario = { 
            "nombre": self.entries["Nombre"].get().strip(),
            "documento": self.entries["Documento"].get().strip(),
            "telefono": self.entries["Teléfono"].get().strip(),
            "rol": self.entries["Rol"].get().strip().capitalize(),
            "edad": self.entries["Edad"].get().strip(),
            "peso": self.entries["Peso"].get().strip()
        }
        exito, msg = AdminJSON.crear_usuario(usuario)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.volver()
        else:
            messagebox.showerror("Error", msg)

    def volver(self):
        self.destroy()
        self.parent.deiconify()


class AdminActualizar(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Actualizar Usuario")
        self.geometry("430x500")
        self.configure(bg="white")
        self.usuario = None

        tk.Label(self, text="Actualizar Usuario", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Documento:", bg="white").grid(row=0, column=0, padx=5)
        self.entry_doc = tk.Entry(search_frame)
        self.entry_doc.grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Buscar", command=self.buscar_usuario).grid(row=0, column=2, padx=5)

        self.form_frame = tk.Frame(self, bg="white")
        self.form_frame.pack(pady=10)

    def buscar_usuario(self):
        doc = self.entry_doc.get().strip()
        usuarios = AdminJSON.listar_usuarios()
        self.usuario = next((u for u in usuarios if u["documento"] == doc), None)
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        if not self.usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            return

        labels = ["Nombre", "Teléfono", "Rol", "Edad", "Peso"]
        self.entries = {}
        for i, key in enumerate(["nombre","telefono","rol","edad","peso"]):
            tk.Label(self.form_frame, text=labels[i]+":", bg="white").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(self.form_frame)
            entry.insert(0, self.usuario[key])
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[key] = entry

        tk.Button(self.form_frame, text="Guardar Cambios", bg="#3366CC", fg="white",
                  command=self.guardar_cambios).grid(row=len(labels), columnspan=2, pady=10)

    def guardar_cambios(self):
        nuevos_datos = {k: e.get().strip() for k, e in self.entries.items()}
        exito, msg = AdminJSON.actualizar_usuario(self.usuario["documento"], nuevos_datos)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.volver()
        else:
            messagebox.showerror("Error", msg)

    def volver(self):
        self.destroy()
        self.parent.deiconify()


class AdminEliminar(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Eliminar Usuario")
        self.geometry("400x200")
        self.configure(bg="white")

        tk.Label(self, text="Eliminar Usuario", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(self, text="Documento:", bg="white").pack(pady=5)
        self.entry_doc = tk.Entry(self)
        self.entry_doc.pack(pady=5)

        tk.Button(self, text="Eliminar", bg="#d9534f", fg="white", command=self.eliminar_usuario).pack(pady=10)
        tk.Button(self, text="Volver", command=self.volver).pack(pady=5)

    def eliminar_usuario(self):
        doc = self.entry_doc.get().strip()
        exito, msg = AdminJSON.eliminar_usuario(doc)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.volver()
        else:
            messagebox.showerror("Error", msg)

    def volver(self):
        self.destroy()
        self.parent.deiconify()


class AdminListar(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Lista de Usuarios")
        self.geometry("700x400")
        self.configure(bg="white")

        tk.Label(self, text="Usuarios Registrados", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        cols = ("nombre","documento","rol","telefono","edad","peso")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=110, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refrescar", command=self.cargar_usuarios).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Volver", command=self.volver).pack(side="left", padx=5)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = AdminJSON.listar_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=(u["nombre"], u["documento"], u["rol"],
                                                u["telefono"], u["edad"], u["peso"]))

    def volver(self):
        self.destroy()
        self.parent.deiconify()

class AdminFunciones(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Panel de Administrador")
        self.geometry("430x600")
        self.configure(bg="white")

        tk.Label(self, text="Panel de Administrador", font=("Arial", 16, "bold"), bg="white").pack(pady=20)

        # Botones para funciones
        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#3366CC", "fg": "white", "width": 25, "height": 2}

        tk.Button(self, text="Crear Usuario", command=lambda: AdminCrear(self), **btn_style).pack(pady=10)
        tk.Button(self, text="Actualizar Usuario", command=lambda: AdminActualizar(self), **btn_style).pack(pady=10)
        tk.Button(self, text="Eliminar Usuario", command=lambda: AdminEliminar(self), **btn_style).pack(pady=10)
        tk.Button(self, text="Listar Usuarios", command=lambda: AdminListar(self), **btn_style).pack(pady=10)
        

    def cerrar_sesion(self):
        self.destroy()

def run():
    print("Iniciando la aplicación GUI")
    app = WelcomeApp()
    app.mainloop()


if __name__ == "__main__":
    app = WelcomeApp()
    app.mainloop()

