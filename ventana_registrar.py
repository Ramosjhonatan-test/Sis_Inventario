import tkinter as tk
from tkinter import messagebox
import sqlite3
import customtkinter

customtkinter.set_appearance_mode("Ligth")  # O "Light" o "Dark" según prefieras
customtkinter.set_default_color_theme("green")  # Puedes cambiar "blue" por otros colores disponibles

class VentanaRegistrar:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack(pady=20)

        customtkinter.CTkLabel(self.register_frame, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
        self.reg_username_entry = customtkinter.CTkEntry(self.register_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(self.register_frame, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
        self.reg_password_entry = customtkinter.CTkEntry(self.register_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.register_frame, text="Registrarse", command=self.register,width=10,bg='orange',fg='black',font=("Arial", 14)).grid(row=7, column=1, columnspan=1, pady=20)
        tk.Button(self.register_frame, text="Salir", command=self.show_login,width=10,bg='red',fg='black',font=("Black", 14)).grid(row=8, column=1, columnspan=1, pady=20)
        

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Registro exitoso")
        self.show_login()

    def show_login(self):
        self.register_frame.pack_forget()
        self.parent.login_frame.pack(pady=20)