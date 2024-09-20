import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import customtkinter
import os
customtkinter.set_appearance_mode("Light")  # O "Light" o "Dark" según prefieras
customtkinter.set_default_color_theme("green")  # Puedes cambiar "blue" por otros colores disponibles

file_patch = os.path.dirname(os.path.realpath(__file__))
image_1 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/acep.png"),size=(30,30))
image_2 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/reg.png"),size=(30,30))
# Configuración de la base de datos
def crear_base_datos():
    conn = sqlite3.connect('cafeteria.db')
    cursor = conn.cursor()

    # Crear tabla de usuarios si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

class VentanaInicio:
    def __init__(self, root, abrir_menu_principal):
        self.root = root
        self.root.title("Cafetería - Inicio de Sesión")
        self.root.geometry("650x350")
        self.abrir_menu_principal = abrir_menu_principal
        
        self.login_frame = customtkinter.CTkFrame(self.root, corner_radius=10)
        self.login_frame.pack(pady=20,padx=20,fill="both",expand=True)

        # Cargar la imagen con fondo transparente
        self.imagen = Image.open("./fondos/i_fondo.png")
        self.imagen = self.imagen.resize((150, 150), Image.LANCZOS)
        self.imagen_tk = ImageTk.PhotoImage(self.imagen)

        # Configurar el Label para que muestre la imagen
        self.label_imagen = tk.Label(self.login_frame, image=self.imagen_tk, bg='white')
        self.label_imagen.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")

        # Resto de los widgets

        tk.Label(self.login_frame, text="Usuario:", font=('Arial', 12,"bold")).grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.username_entry = customtkinter.CTkEntry(self.login_frame, font=('Courier New', 14,"bold"))
        self.username_entry.grid(row=0, column=2, padx=10, pady=10)

        #botones

        tk.Label(self.login_frame, text="Contraseña:", font=('Arial', 12,"bold")).grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = customtkinter.CTkEntry(self.login_frame,show="*" ,font=('Courier New', 14,"bold"))
        self.password_entry.grid(row=1, column=2, padx=10, pady=10)


        iniciar_sesion_btn = customtkinter.CTkButton(master=self.login_frame,
            image=image_1,
            #self.login_frame,
            text="Iniciar Sesión",
            command=self.login,
            corner_radius=20, 
            width=200, 
            height=30, 
            font=("Arial", 16,"bold"),
            border_spacing=10,
            fg_color="red",
            hover_color="orange",text_color="black"
        )
        iniciar_sesion_btn.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        registrarse_btn = customtkinter.CTkButton(master=self.login_frame, 
            image=image_2, text="Registrarse", command=self.show_register,
            corner_radius=20, width=200, height=40, font=("Arial", 16,"bold"),border_spacing=10,fg_color="blue",hover_color="green",text_color="black"
        )
        registrarse_btn.grid(row=2, column=2, padx=10, pady=20, sticky="ew")

        # Configurar el grid para que cambie de tamaño
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(2, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=0)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_columnconfigure(2, weight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.login_frame.pack_forget()
            self.abrir_menu_principal(self.root)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def show_register(self):
        from ventana_registrar import VentanaRegistrar
        self.login_frame.pack_forget()
        self.register_frame = VentanaRegistrar(self.root, self)

    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(pady=20)

# Crear la base de datos al iniciar el programa
crear_base_datos()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")  # Establecer modo de apariencia
    customtkinter.set_default_color_theme("blue")  # Establecer tema de color

    root = customtkinter.CTk()
    app = VentanaInicio(root, lambda x: None)
    root.mainloop()
