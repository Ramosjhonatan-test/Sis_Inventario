import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import customtkinter
import os
customtkinter.set_appearance_mode("Light")  # O "Light" o "Dark" según prefieras
customtkinter.set_default_color_theme("green")  # Puedes cambiar "blue" por otros colores disponibles
file_patch = os.path.dirname(os.path.realpath(__file__))
image_1 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/guardar.png"),size=(30,30))
image_2 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/modificar.png"),size=(30,30))
image_3 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/eliminar.png"),size=(30,30))
image_4 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/salir.png"),size=(30,30))

# Función para crear la tabla 'clientes' si no existe
def crear_tabla_clientes():
    conn = sqlite3.connect('cafeteria.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            correo TEXT NOT NULL,
            celular TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Clase para la ventana de registrar clientes
class VentanaRegistrarCliente:
    def __init__(self, root):
        # Crear la tabla si no existe al inicializar la ventana
        crear_tabla_clientes()

        self.root = root
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.title("Registrar Cliente")
        self.toplevel.geometry("800x600")

        self.id_cliente = None

        # Marco para la parte superior (campos de entrada y botones)
        self.marco_superior = tk.Frame(self.toplevel, bd=4, relief=tk.SOLID)
        self.marco_superior.pack(fill=tk.BOTH, padx=10, pady=10)

        # Títulos y campos de entrada
        tk.Label(self.marco_superior, text="Nombre:", font=('Courier New', 12,"bold")).grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.nombre_entry = customtkinter.CTkEntry(self.marco_superior, font=('Arial Blac', 14,"bold"))
        self.nombre_entry.grid(row=0, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Apellidos:", font=('Courier New', 12,"bold")).grid(row=1, column=4, padx=10, pady=10, sticky="e")
        self.apellidos_entry = customtkinter.CTkEntry(self.marco_superior, font=('Arial', 14,"bold"))
        self.apellidos_entry.grid(row=1, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Correo:", font=('Courier New', 12,"bold")).grid(row=2, column=4, padx=10, pady=10, sticky="e")
        self.correo_entry = customtkinter.CTkEntry(self.marco_superior, font=('Arial', 14,"bold"))
        self.correo_entry.grid(row=2, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Celular:", font=('Courier New', 12,"bold")).grid(row=3, column=4, padx=10, pady=10, sticky="e")
        self.celular_entry = customtkinter.CTkEntry(self.marco_superior, font=('Arial', 14,"bold"))
        self.celular_entry.grid(row=3, column=5, padx=10, pady=10)

        # Botones
        self.marco_botones = tk.Frame(self.toplevel)
        self.marco_botones.pack(pady=10)

        registrarse_btn = customtkinter.CTkButton(master=self.marco_botones,
                                                  image=image_1, text="Registrar", command=self.registrar_cliente,
                                                  corner_radius=20, width=10, font=("Arial", 16,"bold"), border_spacing=10,
                                                  fg_color="indigo", hover_color="grey",text_color="black")
        registrarse_btn.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        modificar_btn = customtkinter.CTkButton(master=self.marco_botones,
                                                image=image_2, text="Modificar", command=self.modificar_cliente,
                                                corner_radius=20, width=10, font=("Arial", 16,"bold"), border_spacing=10,
                                                fg_color="orange", hover_color="grey",text_color="black")
        modificar_btn.grid(row=2, column=2, padx=10, pady=20, sticky="ew")

        eliminar_btn = customtkinter.CTkButton(master=self.marco_botones,
                                               image=image_3, text="Eliminar", command=self.eliminar_cliente,
                                               corner_radius=20, width=10, font=("Arial", 16,"bold"), border_spacing=10,
                                               fg_color="blue", hover_color="grey",text_color="black")
        eliminar_btn.grid(row=2, column=3, padx=10, pady=20, sticky="ew")

        salir_btn = customtkinter.CTkButton(master=self.marco_botones,
                                            image=image_4, text="Salir", command=self.cerrar_ventana,
                                            corner_radius=20, width=10, font=("Arial", 16,"bold"), border_spacing=10,
                                            fg_color="red", hover_color="grey",text_color="black")
        salir_btn.grid(row=2, column=4, padx=10, pady=20, sticky="ew")

        # Marco para la parte inferior (tabla)
        self.marco_inferior = tk.Frame(self.toplevel, bd=4, relief=tk.SOLID)
        self.marco_inferior.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear tabla para mostrar clientes
        self.clientes_tree = ttk.Treeview(self.marco_inferior, columns=("ID", "Nombre", "Apellidos", "Correo", "Celular"), show='headings', height=15)
        self.clientes_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.clientes_tree.heading("Nombre", text="Nombre", anchor=tk.CENTER)
        self.clientes_tree.heading("Apellidos", text="Apellidos", anchor=tk.CENTER)
        self.clientes_tree.heading("Correo", text="Correo", anchor=tk.CENTER)
        self.clientes_tree.heading("Celular", text="Celular", anchor=tk.CENTER)

        # Ajustar el ancho de las columnas
        self.clientes_tree.column("ID", width=50, anchor=tk.CENTER)
        self.clientes_tree.column("Nombre", width=150, anchor=tk.CENTER)
        self.clientes_tree.column("Apellidos", width=150, anchor=tk.CENTER)
        self.clientes_tree.column("Correo", width=200, anchor=tk.CENTER)
        self.clientes_tree.column("Celular", width=100, anchor=tk.CENTER)

        # Alinear contenido al centro en todas las columnas
        for col in ("ID", "Nombre", "Apellidos", "Correo", "Celular"):
            self.clientes_tree.column(col, anchor=tk.CENTER)


        self.clientes_tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Configurar evento de selección en la tabla
        self.clientes_tree.bind("<ButtonRelease-1>", self.cargar_datos_seleccionados)

        # Obtener y mostrar clientes al iniciar
        self.cargar_clientes()

    def cargar_clientes(self):
        # Limpiar la tabla antes de cargar nuevos datos
        registros = self.clientes_tree.get_children()
        for registro in registros:
            self.clientes_tree.delete(registro)

        # Conectar a la base de datos y obtener clientes
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            conn.close()

            # Insertar clientes en la tabla
            for cliente in clientes:
                self.clientes_tree.insert("", "end", values=cliente)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {e}")

    def cargar_datos_seleccionados(self, event):
        # Limpiar campos de entrada
        self.limpiar_campos()

        # Obtener el item seleccionado en la tabla
        item_seleccionado = self.clientes_tree.selection()
        if not item_seleccionado:
            return

        # Obtener datos del cliente seleccionado y cargar en campos de entrada
        datos_cliente = self.clientes_tree.item(item_seleccionado, "values")
        if datos_cliente:
            self.id_cliente = datos_cliente[0]
            self.nombre_entry.insert(0, datos_cliente[1])
            self.apellidos_entry.insert(0, datos_cliente[2])
            self.correo_entry.insert(0, datos_cliente[3])
            self.celular_entry.insert(0, datos_cliente[4])

    def registrar_cliente(self):
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        correo = self.correo_entry.get()
        celular = self.celular_entry.get()

        if not (nombre and apellidos and correo and celular):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, apellidos, correo, celular)
                VALUES (?, ?, ?, ?)
            ''', (nombre, apellidos, correo, celular))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cliente registrado exitosamente")
            self.limpiar_campos()
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {e}")

    def modificar_cliente(self):
        if not self.id_cliente:
            messagebox.showerror("Error", "Seleccione un cliente para modificar")
            return

        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        correo = self.correo_entry.get()
        celular = self.celular_entry.get()

        if not (nombre and apellidos and correo and celular):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE clientes
                SET nombre = ?, apellidos = ?, correo = ?, celular = ?
                WHERE id = ?
            ''', (nombre, apellidos, correo, celular, self.id_cliente))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cliente modificado exitosamente")
            self.limpiar_campos()
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar cliente: {e}")

    def eliminar_cliente(self):
        if not self.id_cliente:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clientes WHERE id = ?', (self.id_cliente,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cliente eliminado exitosamente")
            self.limpiar_campos()
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {e}")

    def limpiar_campos(self):
        self.id_cliente = None
        self.nombre_entry.delete(0, tk.END)
        self.apellidos_entry.delete(0, tk.END)
        self.correo_entry.delete(0, tk.END)
        self.celular_entry.delete(0, tk.END)

    def cerrar_ventana(self):
        self.toplevel.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarCliente(root)
    root.mainloop()
