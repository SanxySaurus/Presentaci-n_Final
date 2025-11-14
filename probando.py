import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
from pathlib import Path
import json
import os
import csv

ASSETS_DIR = Path(__file__).parent

# -----------------------
# Archivos y carpetas
# -----------------------
USUARIOS_FILE = "usuarios.json"
REGISTROS_ECG_CSV = "registros_ecg.csv"   # opcional (no obligatorio para la imagen fija)
DESCRIP_FILE = "descripcion_ecg.json"
ECG_DIR = Path("ecg")                     # carpeta donde estará ecg.png
ECG_DIR.mkdir(exist_ok=True)

# Asegurar archivos base
if not os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

if not os.path.exists(DESCRIP_FILE):
    with open(DESCRIP_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4, ensure_ascii=False)

# -----------------------
# Helpers JSON / CSV
# -----------------------
def load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_ecg_index_from_csv():
    # opcional, no usado para la imagen fija pero lo dejo disponible
    data = {}
    if not os.path.exists(REGISTROS_ECG_CSV):
        return data
    try:
        with open(REGISTROS_ECG_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = (row.get("documento") or "").strip()
                ecg_id = (row.get("ecg_id") or "").strip() or "ecg"
                imgfile = (row.get("image_file") or "").strip() or "ecg.png"
                if not doc:
                    continue
                data.setdefault(doc, {})[ecg_id] = imgfile
    except Exception:
        return {}
    return data

# -----------------------
# MainApp (mantengo nombre y comportamiento)
# -----------------------
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clínica ECG")
        self.geometry("430x932")
        self.configure(bg="white")
        self.resizable(False, False)

        self._images = {}
        self.current_user_doc = None  # document asociada al usuario que inicia (si aplica)

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomeFrame, RoleSelectionFrame, LoginFrame,
                  DashboardFrame, UserFormFrame, DoctorPanelFrame,
                  ECGViewerFrame, DoctorRecordFrame, PatientPanelFrame,
                  PatientECGFrame, PatientDescriptionFrame):
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

            # limpiar pantallas al regresar
            try: self.frames["LoginFrame"].clear_fields()
            except: pass
            try: self.frames["UserFormFrame"].clear_fields()
            except: pass
            try: self.frames["DoctorPanelFrame"].clear_fields()
            except: pass
            try: self.frames["ECGViewerFrame"].clear_fields()
            except: pass
            try: self.frames["PatientPanelFrame"].clear_fields()
            except: pass

            self.show_frame(prev, push_stack=False)

# -----------------------
# BaseFrame (igual)
# -----------------------
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

    def create_back_button(self):
        btn_back = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                             bg="#0047AB", fg="white", bd=0, relief="flat",
                             cursor="hand2", command=self.controller.go_back)
        btn_back.place(x=380, y=10, width=40, height=40)

# -----------------------
# WelcomeFrame (igual)
# -----------------------
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
                           font=("Arial", 12), bg="white", fg="black")
        lbl_sub.pack(pady=(0, 28))

    def create_login_section(self):
        btn_ingresar = tk.Button(
            self,
            text="Ingresar",
            font=("Arial", 14, "bold"),
            bg="#3366CC",
            fg="white",
            width=20,
            height=2,
            bd=0,
            relief="flat",
            command=lambda: self.controller.show_frame("RoleSelectionFrame")
        )
        btn_ingresar.pack(pady=10)

        frame_links = tk.Frame(self, bg="white")
        frame_links.pack(pady=(5, 15))

        lbl_no_cuenta = tk.Label(
            frame_links,
            text="¿Aún no tienes una cuenta?",
            font=("Arial", 11),
            bg="white",
            fg="black"
        )
        lbl_no_cuenta.pack(side="left")

        btn_registro = tk.Button(
            frame_links,
            text="Regístrate aquí",
            font=("Arial", 11, "underline"),
            fg="#e6ac00",
            bg="white",
            bd=0,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Registro", "Funcionalidad de registro pendiente")
        )
        btn_registro.pack(side="left", padx=4)

        lbl_legal = tk.Label(
            self,
            text="Al registrarte aceptas nuestros Términos y Condiciones,\ny nuestra Política de Privacidad.",
            font=("Arial", 9),
            bg="white",
            fg="black",
            justify="center"
        )
        lbl_legal.pack(side="bottom", pady=20)

# -----------------------
# RoleSelectionFrame (igual)
# -----------------------
class RoleSelectionFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_buttons()
        self.create_extra_texts()

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
        login.clear_fields()
        login.set_role(role)
        self.controller.show_frame("LoginFrame")

    def create_extra_texts(self):
        lbl_legal = tk.Label(
            self,
            text="Al registrarte aceptas nuestros Términos y Condiciones,\ny nuestra Política de Privacidad.",
            font=("Arial", 9),
            bg="white",
            fg="black",
            justify="center"
        )
        lbl_legal.pack(side="bottom", pady=15)

# -----------------------
# LoginFrame (modificado para tus reglas de acceso)
# -----------------------
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

    def clear_fields(self):
        try:
            self.entry_user.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
        except:
            pass

    def check_login(self):
        usuario = self.entry_user.get().strip()
        contrasena = self.entry_pass.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        # ADMINISTRADOR: cualquier usuario y contraseña
        if self.role == "Administrador":
            dashboard = self.controller.frames["DashboardFrame"]
            dashboard.set_user(usuario, self.role)
            # No asociamos documento al admin
            self.controller.show_frame("DashboardFrame")
            self.controller.nav_stack.clear()
            return

        # DOCTOR / PACIENTE: usuario debe existir en usuarios.json (buscamos por 'usuario' o 'nombre' o 'documento'),
        # pero la contraseña se ignora (permite cualquier contraseña)
        usuarios = load_json(USUARIOS_FILE) or []
        encontrado = None
        for u in usuarios:
            # normalizar a str
            uname = str(u.get("usuario") or u.get("nombre") or "")
            docu = str(u.get("documento") or "")
            if (uname and uname.lower() == usuario.lower()) or (docu and docu == usuario):
                # además requerimos que el rol coincida
                if u.get("rol") == self.role:
                    encontrado = u
                    break
        if not encontrado:
            messagebox.showerror("Error", "Usuario no encontrado para este rol.")
            return

        # acceso permitido
        dashboard = self.controller.frames["DashboardFrame"]
        # mostrar el nombre de usuario o documento según disponible
        display_user = encontrado.get("usuario") or encontrado.get("nombre") or encontrado.get("documento") or usuario
        dashboard.set_user(display_user, self.role)

        # almacenar documento si existe
        if encontrado.get("documento"):
            self.controller.current_user_doc = encontrado.get("documento")
            # también pasar documento a frames relevantes
            try:
                self.controller.frames["DoctorPanelFrame"].current_doc = encontrado.get("documento")
            except: pass
            try:
                self.controller.frames["PatientPanelFrame"].current_doc = encontrado.get("documento")
            except: pass

        self.controller.show_frame("DashboardFrame")
        self.controller.nav_stack.clear()

# -----------------------
# DashboardFrame (mantengo formato)
# -----------------------
class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.username = None
        self.role = None
        self.create_ui()

    def create_ui(self):
        self.create_header_image_or_bar()

        self.actions = tk.Frame(self, bg="white")
        self.actions.pack(pady=20)

        cfg = {"font": ("Arial", 14, "bold"), "bg": "#1e73b8", "fg": "white",
               "width": 28, "height": 2, "bd": 0}

        self.btn_crear = tk.Button(self.actions, text="Crear Usuario", command=self.on_crear, **cfg)
        self.btn_actualizar = tk.Button(self.actions, text="Actualizar Usuario", command=self.on_actualizar, **cfg)
        self.btn_eliminar = tk.Button(self.actions, text="Eliminar Usuario", command=self.on_eliminar, **cfg)
        self.btn_listar = tk.Button(self.actions, text="Listar Usuarios", command=self.on_listar, **cfg)

        self.btn_crear.pack(pady=10)
        self.btn_actualizar.pack(pady=10)
        self.btn_eliminar.pack(pady=10)
        self.btn_listar.pack(pady=10)

        bottom = tk.Frame(self, bg="white")
        bottom.pack(side="bottom", fill="x", pady=18)
        self.lbl_user = tk.Label(bottom, text="", bg="white")
        self.lbl_user.pack(side="left", padx=18)
        tk.Button(bottom, text="Cerrar sesión", bg="#777", fg="white",
                  command=self.logout).pack(side="right", padx=18)

    def set_user(self, user, role):
        self.username = user
        self.role = role
        self.lbl_user.config(text=f"Usuario: {user}  |  Rol: {role}")

        # mostrar/ocultar botones sin cambiar formato
        if role == "Administrador":
            self.btn_crear.pack(pady=10)
            self.btn_actualizar.pack(pady=10)
            self.btn_eliminar.pack(pady=10)
            self.btn_listar.pack(pady=10)
        else:
            # esconder CRUD
            self.btn_crear.pack_forget()
            self.btn_actualizar.pack_forget()
            self.btn_eliminar.pack_forget()
            self.btn_listar.pack_forget()

            # eliminar posibles botones anteriores
            for w in self.actions.winfo_children():
                if isinstance(w, tk.Button) and w.cget("text") in ("Panel Doctor", "Panel Paciente", "Ver ECG (Explorar)"):
                    w.destroy()

            if role == "Doctor":
                tk.Button(self.actions, text="Panel Doctor", command=lambda: self.controller.show_frame("DoctorPanelFrame"), **cfg).pack(pady=10)
                tk.Button(self.actions, text="Ver ECG (Explorar)", command=lambda: self.controller.show_frame("ECGViewerFrame"), **cfg).pack(pady=10)
            elif role == "Paciente":
                tk.Button(self.actions, text="Panel Paciente", command=lambda: self.controller.show_frame("PatientPanelFrame"), **cfg).pack(pady=10)

    def logout(self):
        try: self.controller.frames["LoginFrame"].clear_fields()
        except: pass
        try: self.controller.frames["UserFormFrame"].clear_fields()
        except: pass
        try: self.controller.frames["ECGViewerFrame"].clear_fields()
        except: pass

        # limpiar documento asociado
        self.controller.current_user_doc = None

        self.controller.show_frame("WelcomeFrame")
        self.controller.nav_stack.clear()

    def on_crear(self):
        self.controller.frames["UserFormFrame"].open_for("crear")

    def on_actualizar(self):
        self.controller.frames["UserFormFrame"].open_for("actualizar")

    def on_eliminar(self):
        self.controller.frames["UserFormFrame"].open_for("eliminar")

    def on_listar(self):
        self.controller.frames["UserFormFrame"].open_for("listar")

# -----------------------
# UserFormFrame (mantengo formato)
# -----------------------
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

    def clear_fields(self):
        for entry in (self.entry_nombre, self.entry_documento,
                      self.entry_telefono, self.entry_edad, self.entry_peso):
            try: entry.delete(0, tk.END)
            except: pass
        try: self.var_rol.set("")
        except: pass

    def load_users(self):
        if not os.path.exists(USUARIOS_FILE):
            return []
        try:
            with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_users(self, users):
        with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def open_for(self, action):
        self.action = action
        self.btn_action.config(text=action.capitalize() + " usuario")
        self.clear_fields()
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

    def on_action(self):
        users = self.load_users()
        doc = self.entry_documento.get().strip()

        existing = next((u for u in users if u.get("documento") == doc), None)

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
            if not messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este usuario?"):
                return
            users.remove(existing)
            self.save_users(users)
            messagebox.showinfo("OK", "Usuario eliminado.")

        elif self.action == "listar":
            if not users:
                messagebox.showinfo("Lista", "No hay usuarios.")
            else:
                msg = "\n".join([f"{u.get('nombre','')} — {u.get('documento','')}" for u in users])
                messagebox.showinfo("Listado de usuarios", msg)

        self.controller.go_back()

# -----------------------
# ECGViewerFrame (muestra la imagen fija ecg/ecg.png)
# -----------------------
class ECGViewerFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._found = False
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_ui()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, relief="flat",
                        cursor="hand2", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_ui(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=10, fill="both", expand=True)

        tk.Label(frame, text="Documento del paciente", bg="white").pack(pady=(6,0))
        self.entry_doc = tk.Entry(frame, width=30)
        self.entry_doc.pack(pady=6)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Buscar registros", bg="#3366CC", fg="white",
                  command=self.find_records).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Mostrar ECG", bg="#1e73b8", fg="white",
                  command=self.show_ecg).pack(side="left", padx=6)

        self.lbl_image = tk.Label(self, bg="white")
        self.lbl_image.pack(pady=12)
        self._tkimg = None

    def clear_fields(self):
        try:
            self.entry_doc.delete(0, tk.END)
            self.lbl_image.config(image="")
            self._tkimg = None
            self._found = False
        except: pass

    def find_records(self):
        # Para la versión con imagen fija, si existe ecg/ecg.png consideramos que hay registro
        doc = self.entry_doc.get().strip()
        if not doc:
            messagebox.showwarning("Aviso", "Escribe un número de documento")
            return
        path = ECG_DIR / "ecg.png"
        if path.exists():
            self._found = True
            messagebox.showinfo("Listo", "Registro encontrado (imagen fija). Pulsa 'Mostrar ECG'.")
        else:
            self._found = False
            messagebox.showinfo("No hay registros", "No se encontró la imagen ecg/ecg.png en la carpeta ecg/")

    def show_ecg(self):
        if not self._found:
            messagebox.showwarning("Aviso", "Primero pulsa 'Buscar registros' o coloca ecg/ecg.png")
            return
        path = ECG_DIR / "ecg.png"
        if not path.exists():
            messagebox.showerror("Error", "No se encontró ecg/ecg.png")
            return
        try:
            img = Image.open(path).resize((350, 250), Image.LANCZOS)
            self._tkimg = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=self._tkimg)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

# -----------------------
# DoctorPanelFrame (buscar paciente, IMC campo, ver ECG, generar registro)
# -----------------------
class DoctorPanelFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.current_doc = None
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_ui()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, relief="flat",
                        cursor="hand2", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_ui(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=10, fill="both", expand=True)

        tk.Label(frame, text="Buscar paciente por documento", bg="white").pack(pady=(6,0))
        self.entry_doc = tk.Entry(frame, width=30)
        self.entry_doc.pack(pady=6)

        tk.Label(frame, text="IMC / Observación (doctor escribe aquí)", bg="white").pack(pady=(8,0))
        self.entry_imc = tk.Entry(frame, width=30)
        self.entry_imc.pack(pady=6)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Buscar paciente", bg="#3366CC", fg="white",
                  command=self.find_patient).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Ver historial ECG", bg="#1e73b8", fg="white",
                  command=self.open_ecg_viewer).pack(side="left", padx=6)
        tk.Button(frame, text="Generar / Guardar descripción", bg="#1e73b8", fg="white",
                  command=self.generate_description).pack(pady=8)

        self.info_lbl = tk.Label(frame, text="", bg="white", justify="left")
        self.info_lbl.pack(pady=6)

    def clear_fields(self):
        try:
            self.entry_doc.delete(0, tk.END)
            self.entry_imc.delete(0, tk.END)
            self.info_lbl.config(text="")
        except: pass

    def find_patient(self):
        doc = self.entry_doc.get().strip()
        if not doc:
            messagebox.showwarning("Aviso", "Escribe un número de documento")
            return
        users = load_json(USUARIOS_FILE) or []
        patient = next((u for u in users if str(u.get("documento")) == doc), None)
        if not patient:
            messagebox.showinfo("No encontrado", "No existe un paciente con ese documento.")
            return
        nombre = patient.get("nombre", "")
        edad = patient.get("edad", "")
        peso = patient.get("peso", "")
        altura = patient.get("altura", "")
        info = f"Nombre: {nombre}\nDocumento: {doc}\nEdad: {edad}\nPeso: {peso}\nAltura: {altura}\n"
        # IMC no se calcula automáticamente: el doctor escribirá en entry_imc
        self.info_lbl.config(text=info)
        # almacenar doc para acciones siguientes
        self.current_doc = doc

    def open_ecg_viewer(self):
        doc = self.entry_doc.get().strip()
        if not doc:
            messagebox.showwarning("Aviso", "Ingresa documento")
            return
        viewer = self.controller.frames["ECGViewerFrame"]
        try:
            viewer.entry_doc.delete(0, tk.END)
            viewer.entry_doc.insert(0, doc)
            viewer.clear_fields()
        except: pass
        self.controller.show_frame("ECGViewerFrame")

    def generate_description(self):
        doc = self.entry_doc.get().strip()
        if not doc:
            messagebox.showwarning("Aviso", "Ingresa documento")
            return
        # el doctor elige el ecg (aquí usamos imagen fija 'ecg')
        desc_text = simpledialog.askstring("Descripción", "Escribe la interpretación (observaciones) del ECG:")
        if desc_text is None:
            return
        descs = load_json(DESCRIP_FILE) or {}
        # usamos la clave 'ecg' por tratarse de imagen fija
        descs.setdefault(doc, {})["ecg"] = {"descripcion": desc_text, "imc_observacion": self.entry_imc.get().strip()}
        save_json(DESCRIP_FILE, descs)
        messagebox.showinfo("OK", "Descripción guardada en descripcion_ecg.json")

# -----------------------
# DoctorRecordFrame (si quieres un frame dedicado para registrar — opcional)
# -----------------------
class DoctorRecordFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_ui()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, relief="flat",
                        cursor="hand2", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_ui(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20)
        tk.Label(frame, text="Generar registro (Doctor)", bg="white").pack(pady=6)
        tk.Label(frame, text="Documento", bg="white").pack()
        self.entry_doc = tk.Entry(frame, width=30)
        self.entry_doc.pack(pady=6)
        tk.Label(frame, text="Observación", bg="white").pack()
        self.text_obs = tk.Text(frame, width=40, height=8)
        self.text_obs.pack(pady=6)
        tk.Button(frame, text="Guardar", bg="#1e73b8", fg="white", command=self.save).pack(pady=6)

    def save(self):
        doc = self.entry_doc.get().strip()
        obs = self.text_obs.get("1.0", tk.END).strip()
        if not doc or not obs:
            messagebox.showerror("Error", "Datos incompletos")
            return
        descs = load_json(DESCRIP_FILE) or {}
        descs.setdefault(doc, {})["ecg"] = {"descripcion": obs}
        save_json(DESCRIP_FILE, descs)
        messagebox.showinfo("OK", "Guardado")
        self.controller.go_back()

# -----------------------
# PatientPanelFrame (ver ultimo ECG y descripciones)
# -----------------------
class PatientPanelFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.current_doc = None
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_ui()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, relief="flat",
                        cursor="hand2", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_ui(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20, fill="both", expand=True)

        tk.Label(frame, text="Documento del paciente", bg="white").pack(pady=(6,0))
        self.entry_doc = tk.Entry(frame, width=30)
        self.entry_doc.pack(pady=6)

        btns = tk.Frame(frame, bg="white")
        btns.pack(pady=6)
        tk.Button(btns, text="Ver examen ECG (más reciente)", bg="#1e73b8", fg="white", command=self.view_latest_ecg).pack(side="left", padx=6)
        tk.Button(btns, text="Ver descripción ECG", bg="#3366CC", fg="white", command=self.view_description).pack(side="left", padx=6)

    def clear_fields(self):
        try:
            self.entry_doc.delete(0, tk.END)
        except: pass

    def view_latest_ecg(self):
        doc = self.entry_doc.get().strip()
        if not doc:
            messagebox.showwarning("Aviso", "Escribe un número de documento")
            return
        # Como usamos imagen fija, si existe ecg/ecg.png la mostramos
        path = ECG_DIR / "ecg.png"
        if not path.exists():
            messagebox.showinfo("No hay ECG", "No se encontró la imagen ecg/ecg.png")
            return
        viewer = self.controller.frames["ECGViewerFrame"]
        try:
            viewer.entry_doc.delete(0, tk.END)
            viewer.entry_doc.insert(0, doc)
            viewer.clear_fields()
            viewer._found = True
            viewer.show_ecg()
            self.controller.show_frame("ECGViewerFrame")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el ECG: {e}")

    def view_description(self):
        doc = self.entry_doc.get().strip()
        if not doc:
            messagebox.showwarning("Aviso", "Escribe un número de documento")
            return
        descs = load_json(DESCRIP_FILE) or {}
        if doc not in descs or "ecg" not in descs[doc]:
            messagebox.showinfo("No hay descripción", "No hay descripciones guardadas para este paciente.")
            return
        text = descs[doc]["ecg"].get("descripcion", "")
        imc_obs = descs[doc]["ecg"].get("imc_observacion", "")
        info = f"Descripción:\n{text}\n\nIMC/Observación doctor: {imc_obs}"
        # mostrar en una ventana simple
        messagebox.showinfo("Descripción ECG", info)

# -----------------------
# PatientECGFrame (si quieres vista dedicada para paciente)
# -----------------------
class PatientECGFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._tkimg = None
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_ui()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, relief="flat",
                        cursor="hand2", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_ui(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20)
        tk.Label(frame, text="Mi ECG", bg="white", font=("Arial", 16, "bold")).pack(pady=6)
        tk.Button(frame, text="Mostrar ECG", bg="#1e73b8", fg="white", command=self.show_my_ecg).pack(pady=6)
        self.lbl_image = tk.Label(self, bg="white")
        self.lbl_image.pack(pady=12)

    def show_my_ecg(self):
        # intentar obtener documento del usuario logueado
        doc = self.controller.current_user_doc or ""
        if not doc:
            # pedirlo
            doc = simpledialog.askstring("Documento", "Introduce tu número de documento:")
            if not doc:
                return
        path = ECG_DIR / "ecg.png"
        if not path.exists():
            messagebox.showerror("Error", "No existe ecg/ecg.png")
            return
        try:
            img = Image.open(path).resize((350, 250), Image.LANCZOS)
            self._tkimg = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=self._tkimg)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

# -----------------------
# PatientDescriptionFrame (vista dedicada para descripciones)
# -----------------------
class PatientDescriptionFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header_image_or_bar()
        self.create_back_button()
        self.create_ui()

    def create_back_button(self):
        btn = tk.Button(self, text="←", font=("Arial", 18, "bold"),
                        bg="#0047AB", fg="white", bd=0, relief="flat",
                        cursor="hand2", command=self.controller.go_back)
        btn.place(x=380, y=10, width=40, height=40)

    def create_ui(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20)
        tk.Label(frame, text="Descripción ECG", font=("Arial", 16, "bold"), bg="white").pack(pady=6)
        self.text = tk.Text(frame, width=45, height=15)
        self.text.pack(pady=6)
        tk.Button(frame, text="Cargar descripción", bg="#3366CC", fg="white", command=self.load_description).pack(pady=6)

    def load_description(self):
        doc = simpledialog.askstring("Documento", "Introduce tu número de documento:")
        if not doc:
            return
        descs = load_json(DESCRIP_FILE) or {}
        if doc not in descs or "ecg" not in descs[doc]:
            messagebox.showinfo("No hay", "No hay descripciones guardadas para este documento.")
            return
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, descs[doc]["ecg"].get("descripcion", ""))

# -----------------------
# RUN
# -----------------------
def run():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    run()
