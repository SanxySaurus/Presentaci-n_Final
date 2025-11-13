import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from pathlib import Path
import json
import os

ASSETS_DIR = Path(__file__).parent


# ------------------------------------------------------------
#  MAIN APP
# ------------------------------------------------------------
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clínica ECG")
        self.geometry("430x932")
        self.configure(bg="white")
        self.resizable(False, False)

        self._images = {}

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomeFrame, RoleSelectionFrame, LoginFrame,
                  DashboardFrame, UserFormFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.nav_stack = []
        self.current_frame = None

        self.show_frame("WelcomeFrame", push_stack=False)

    def load_image(self, filename, size):
        path = ASSETS_DIR / filename
        try:
            img = Image.open(path).resize(size, Image.LANCZOS)
            tkimg = ImageTk.PhotoImage(img)
            self._images[filename] = tkimg
            return tkimg
        except Exception:
            return None

    def show_frame(self, name, push_stack=True):
        if push_stack and self.current_frame:
            self.nav_stack.append(self.current_frame)
        frame = self.frames[name]
        frame.tkraise()
        self.current_frame = name

    def go_back(self):
        if self.nav_stack:
            prev = self.nav_stack.pop()
            self.show_frame(prev, push_stack=False)


# ------------------------------------------------------------
#  BASE FRAME
# ------------------------------------------------------------
class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

    def create_header_image_or_bar(self):
        img = self.controller.load_image("Encabezado.png", (430, 250))
        if img:
            lbl = tk.Label(self, image=img, bg="white")
            lbl.image = img
        else:
            lbl = tk.Frame(self, bg="#0b63a8", width=430, height=160)
            lbl.pack_propagate(False)
            title = tk.Label(lbl, text="CLINIC", fg="white", bg="#0b63a8",
                             font=("Arial", 20, "bold"))
            title.pack(anchor="nw", padx=20, pady=14)
        lbl.pack(fill="x")


# ------------------------------------------------------------
#  WELCOME SCREEN
# ------------------------------------------------------------
class WelcomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header_image_or_bar()
        self.create_logo_text()
        self.create_login_section()

    def create_logo_text(self):
        img = self.controller.load_image("logo.webp", (180, 120))
        if img:
            lbl_logo = tk.Label(self, image=img, bg="white")
            lbl_logo.image = img
            lbl_logo.pack(pady=(30, 8))
        else:
            lbl_name = tk.Label(self, text="CLÍNICA ECG",
                                font=("Arial", 22, "bold"),
                                fg="#0047AB", bg="white")
            lbl_name.pack(pady=(30, 8))

        lbl_sub = tk.Label(self, text="Bienvenido a tu clínica de confianza",
                           font=("Arial", 12), bg="white")
        lbl_sub.pack(pady=(0, 28))

    def create_login_section(self):
        btn_ingresar = tk.Button(self, text="Ingresar", font=("Arial", 14, "bold"),
                                 bg="#3366CC", fg="white", width=20, height=2,
                                 bd=0, relief="flat",
                                 command=lambda: self.controller.show_frame("RoleSelectionFrame"))
        btn_ingresar.pack(pady=10)


# ------------------------------------------------------------
#  ROLE SELECTION
# ------------------------------------------------------------
class RoleSelectionFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_buttons()

    def create_back_button(self):
        btn_back = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                             bg="#0047AB", fg="white", bd=0, relief="flat",
                             cursor="hand2", command=self.controller.go_back)
        btn_back.place(x=380, y=10, width=40, height=40)

    def create_buttons(self):
        btn_style = {"font": ("Arial", 14, "bold"),
                     "bg": "#3366CC", "fg": "white", "width": 20,
                     "height": 2, "bd": 0, "relief": "flat"}

        container = tk.Frame(self, bg="white")
        container.pack(pady=40)

        for role in ("Administrador", "Doctor", "Paciente"):
            tk.Button(container, text=role, **btn_style,
                      command=lambda r=role: self.open_login(r)).pack(pady=10)

    def open_login(self, role):
        login = self.controller.frames["LoginFrame"]
        login.set_role(role)
        self.controller.show_frame("LoginFrame")


# ------------------------------------------------------------
#  LOGIN
# ------------------------------------------------------------
class LoginFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.role = None
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_form()

    def set_role(self, role):
        self.role = role
        self.lbl_role.config(text=f"Iniciar sesión — {role}")

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_form(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20)

        self.lbl_role = tk.Label(frame, text="Iniciar sesión",
                                 font=("Arial", 12, "bold"), bg="white")
        self.lbl_role.pack(pady=5)

        tk.Label(frame, text="Usuario", bg="white").pack()
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(pady=5)

        tk.Label(frame, text="Contraseña", bg="white").pack()
        self.entry_pass = tk.Entry(frame, show="*")
        self.entry_pass.pack(pady=5)

        btn = tk.Button(frame, text="Inicia sesión", bg="#3366CC",
                        fg="white", width=20, command=self.check_login)
        btn.pack(pady=15)

    def check_login(self):
        if not self.entry_user.get().strip() or not self.entry_pass.get().strip():
            messagebox.showerror("Error", "Completa todos los campos")
            return

        dashboard = self.controller.frames["DashboardFrame"]
        dashboard.set_user(self.entry_user.get(), self.role)

        self.controller.show_frame("DashboardFrame")
        self.controller.nav_stack.clear()


# ------------------------------------------------------------
#  DASHBOARD
# ------------------------------------------------------------
class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.username = None
        self.role = None
        self.create_ui()

    def create_ui(self):
        self.create_header_image_or_bar()

        actions = tk.Frame(self, bg="white")
        actions.pack(pady=20)

        cfg = {"font": ("Arial", 14, "bold"), "bg": "#1e73b8", "fg": "white",
               "width": 28, "height": 2, "bd": 0}

        tk.Button(actions, text="Crear Usuario", command=self.on_crear, **cfg).pack(pady=10)
        tk.Button(actions, text="Actualizar Usuario", command=self.on_actualizar, **cfg).pack(pady=10)
        tk.Button(actions, text="Eliminar Usuario", command=self.on_eliminar, **cfg).pack(pady=10)
        tk.Button(actions, text="Listar Usuarios", command=self.on_listar, **cfg).pack(pady=10)

        bottom = tk.Frame(self, bg="white")
        bottom.pack(side="bottom", fill="x", pady=15)

        self.lbl_user = tk.Label(bottom, text="", bg="white")
        self.lbl_user.pack(side="left", padx=10)

        tk.Button(bottom, text="Cerrar sesión", bg="#777", fg="white",
                  command=self.logout).pack(side="right", padx=10)

    def set_user(self, user, role):
        self.username = user
        self.role = role
        self.lbl_user.config(text=f"Usuario: {user}  |  Rol: {role}")

    def logout(self):
        self.controller.show_frame("WelcomeFrame")
        self.controller.nav_stack.clear()

    # acciones CRUD
    def on_crear(self):
        self.controller.frames["UserFormFrame"].open_for("crear")

    def on_actualizar(self):
        self.controller.frames["UserFormFrame"].open_for("actualizar")

    def on_eliminar(self):
        self.controller.frames["UserFormFrame"].open_for("eliminar")

    def on_listar(self):
        self.controller.frames["UserFormFrame"].open_for("listar")


# ------------------------------------------------------------
#  USER FORM (CRUD)
# ------------------------------------------------------------
class UserFormFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.action = None

        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_form()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_form(self):
        self.form = tk.Frame(self, bg="white")
        self.form.pack(pady=20)

        self.entry_nombre = self.create_entry("Nombre completo")
        self.entry_documento = self.create_entry("Número de documento")
        self.entry_telefono = self.create_entry("Teléfono")

        tk.Label(self.form, text="Rol", bg="white").pack()
        self.var_rol = tk.StringVar()
        self.combo_rol = ttk.Combobox(self.form, values=["Administrador", "Doctor", "Paciente"],
                                      state="readonly", textvariable=self.var_rol, width=30)
        self.combo_rol.pack(pady=5)

        row = tk.Frame(self.form, bg="white")
        row.pack()

        tk.Label(row, text="Edad", bg="white").grid(row=0, column=0)
        self.entry_edad = tk.Entry(row, width=10)
        self.entry_edad.grid(row=1, column=0, padx=5)

        tk.Label(row, text="Peso", bg="white").grid(row=0, column=1)
        self.entry_peso = tk.Entry(row, width=10)
        self.entry_peso.grid(row=1, column=1, padx=5)

        self.btn_action = tk.Button(self.form, text="", bg="#3366CC",
                                    fg="white", font=("Arial", 13),
                                    width=25, height=2, command=self.on_action)
        self.btn_action.pack(pady=20)

    def create_entry(self, text):
        tk.Label(self.form, text=text, bg="white").pack()
        entry = tk.Entry(self.form, width=30)
        entry.pack(pady=5)
        return entry

    # ------- JSON I/O -------
    def load_users(self):
        if not os.path.exists("usuarios.json"):
            return []
        try:
            with open("usuarios.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_users(self, users):
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    # ------- OPEN FORM -------
    def open_for(self, action):
        self.action = action
        self.btn_action.config(text=action.capitalize() + " usuario")

        for entry in (self.entry_nombre, self.entry_documento,
                      self.entry_telefono, self.entry_edad, self.entry_peso):
            entry.delete(0, tk.END)
        self.var_rol.set("")

        self.controller.show_frame("UserFormFrame")

    def get_user_data(self):
        return {
            "nombre": self.entry_nombre.get().strip(),
            "documento": self.entry_documento.get().strip(),
            "telefono": self.entry_telefono.get().strip(),
            "rol": self.var_rol.get(),
            "edad": self.entry_edad.get().strip(),
            "peso": self.entry_peso.get().strip()
        }

    # ------- CRUD -------
    def on_action(self):
        users = self.load_users()
        doc = self.entry_documento.get().strip()

        existing = next((u for u in users if u["documento"] == doc), None)

        if self.action == "crear":
            if existing:
                messagebox.showerror("Error", "El usuario ya existe.")
                return
            users.append(self.get_user_data())
            self.save_users(users)
            messagebox.showinfo("OK", "Usuario creado.")

        elif self.action == "actualizar":
            if not existing:
                messagebox.showerror("Error", "El usuario no existe.")
                return
            idx = users.index(existing)
            users[idx] = self.get_user_data()
            self.save_users(users)
            messagebox.showinfo("OK", "Usuario actualizado.")

        elif self.action == "eliminar":
            if not existing:
                messagebox.showerror("Error", "El usuario no existe.")
                return
            users.remove(existing)
            self.save_users(users)
            messagebox.showinfo("OK", "Usuario eliminado.")

        elif self.action == "listar":
            if not users:
                messagebox.showinfo("Lista", "No hay usuarios.")
            else:
                msg = "\n".join([f"{u['nombre']} — {u['documento']}" for u in users])
                messagebox.showinfo("Listado de usuarios", msg)

        self.controller.go_back()


# ------------------------------------------------------------
#  RUN
# ------------------------------------------------------------
def run():
    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    run()
