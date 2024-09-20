import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import sqlite3
import customtkinter
import os
customtkinter.set_appearance_mode("Light")  # O "Light" o "Dark" según prefieras
customtkinter.set_default_color_theme("green")  # Puedes cambiar "blue" por otros colores disponibles

#iconos
file_patch = os.path.dirname(os.path.realpath(__file__))
image_1 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/guardar.png"),size=(30,30))
image_2 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/modificar.png"),size=(30,30))
image_3 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/eliminar.png"),size=(30,30))
image_4 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/salir.png"),size=(30,30))

class VentanaRegistrarProducto:
    def __init__(self, root):
        self.root = root
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.title("Registrar Producto")
        self.toplevel.geometry("800x600")

        # Estilos
        self.estilo = ttk.Style()
        self.estilo.configure('TButton', foreground='white', background='#4CAF50', font=('Arial', 12))
        self.estilo.configure('Treeview.Heading', font=('Arial', 10, 'bold'))

        # Marco para campos de entrada y botones
        self.marco_entrada = tk.Frame(self.toplevel)
        self.marco_entrada.pack(pady=20)

        # Títulos y campos de entrada
        tk.Label(self.marco_entrada, text="ID:", font=('Arial', 12,"bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.id_entry = customtkinter.CTkEntry(self.marco_entrada, font=('Courier New', 14,"bold"))
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)


        tk.Label(self.marco_entrada, text="Nombre del Producto:", font=('Arial', 12,"bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.nombre_entry = customtkinter.CTkEntry(self.marco_entrada, font=('Courier New', 14,"bold"))
        self.nombre_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.marco_entrada, text="Categoría:", font=('Arial', 12,'bold')).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.categoria_entry = customtkinter.CTkEntry(self.marco_entrada, font=('Courier New', 14,"bold"))
        self.categoria_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.marco_entrada, text="Cantidad:", font=('Arial', 12,"bold")).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.cantidad_entry = customtkinter.CTkEntry(self.marco_entrada, font=('Courier New', 14,"bold"))
        self.cantidad_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.marco_entrada, text="Precio:", font=('Arial', 12,"bold")).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.precio_entry = customtkinter.CTkEntry(self.marco_entrada, font=('Courier New', 14,"bold"))
        self.precio_entry.grid(row=4, column=1, padx=10, pady=10)

        # Botones
        self.marco_botones = tk.Frame(self.toplevel)
        self.marco_botones.pack(pady=10)
        
        registrar_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_1, text="Registrar", command=self.registrar_producto,
            corner_radius=20, width=10,font=("Arial", 16),border_spacing=10,fg_color="purple",hover_color="grey",text_color="black"
        )
        registrar_btn.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

        modificar_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_2, text="Modificar", command=self.modificar_producto,
            corner_radius=20, width=10,font=("Arial", 16),border_spacing=10,fg_color="orange",hover_color="grey",text_color="black"
        )
        modificar_btn.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

        eliminar_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_3, text="Eliminar", command=self.eliminar_producto,
            corner_radius=20, width=10,font=("Arial", 16),border_spacing=10,fg_color="blue",hover_color="grey",text_color="black"
        )
        eliminar_btn.grid(row=0, column=2, padx=10, pady=20, sticky="ew")

        salir_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_4, text="Salir", command=self.cerrar_ventana,
            corner_radius=20, width=10,font=("Arial", 16),border_spacing=10,fg_color="red",hover_color="grey",text_color="black"
        )
        salir_btn.grid(row=0, column=3, padx=10, pady=20, sticky="ew")

        # Tabla de productos
        self.productos_tree = ttk.Treeview(self.toplevel, columns=("ID", "Nombre", "Categoría", "Cantidad", "Precio"), show='headings', height=15)
        self.productos_tree.heading("ID", text="ID", anchor=tk.CENTER,)
        self.productos_tree.heading("Nombre", text="Nombre del Producto", anchor=tk.CENTER)
        self.productos_tree.heading("Categoría", text="Categoría", anchor=tk.CENTER)
        self.productos_tree.heading("Cantidad", text="Cantidad", anchor=tk.CENTER)
        self.productos_tree.heading("Precio", text="Precio", anchor=tk.CENTER)
        
        # Ajustar el ancho de las columnas
        self.productos_tree.column("ID", width=50, anchor=tk.CENTER)
        self.productos_tree.column("Nombre", width=200, anchor=tk.CENTER)
        self.productos_tree.column("Categoría", width=100, anchor=tk.CENTER)
        self.productos_tree.column("Cantidad", width=80, anchor=tk.CENTER)
        self.productos_tree.column("Precio", width=80, anchor=tk.CENTER)

        self.productos_tree.pack(fill=tk.BOTH, expand=True)

        self.cargar_productos()

        # Evento de selección en la tabla
        self.productos_tree.bind("<ButtonRelease-1>", self.mostrar_seleccion)

    def registrar_producto(self):
        id_producto = self.id_entry.get()
        nombre_producto = self.nombre_entry.get()
        categoria = self.categoria_entry.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()

        if not (id_producto and nombre_producto and categoria and cantidad and precio):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY,
                    nombre_producto TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL
                )
            ''')
            cursor.execute('''
                INSERT INTO productos (id, nombre_producto, categoria, cantidad, precio)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_producto, nombre_producto, categoria, cantidad, precio))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Producto registrado exitosamente")
            self.limpiar_campos()
            self.cargar_productos()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "ID de producto duplicado. Por favor, ingrese un ID único.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def modificar_producto(self):
        id_producto = self.id_entry.get()
        nombre_producto = self.nombre_entry.get()
        categoria = self.categoria_entry.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()

        if not id_producto:
            messagebox.showerror("Error", "Seleccione un producto de la tabla para modificar")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE productos SET nombre_producto=?, categoria=?, cantidad=?, precio=?
                WHERE id=?
            ''', (nombre_producto, categoria, cantidad, precio, id_producto))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Producto modificado exitosamente")
            self.limpiar_campos()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def eliminar_producto(self):
        id_producto = self.id_entry.get()

        if not id_producto:
            messagebox.showerror("Error", "Seleccione un producto de la tabla para eliminar")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM productos WHERE id=?', (id_producto,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
            self.limpiar_campos()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cargar_productos(self):
        for i in self.productos_tree.get_children():
            self.productos_tree.delete(i)

        conn = sqlite3.connect('cafeteria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        conn.close()

        for producto in productos:
            self.productos_tree.insert('', 'end', values=producto)

    def mostrar_seleccion(self, event):
        item = self.productos_tree.selection()[0]
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

        values = self.productos_tree.item(item, 'values')
        self.id_entry.insert(tk.END, values[0])
        self.nombre_entry.insert(tk.END, values[1])
        self.categoria_entry.insert(tk.END, values[2])
        self.cantidad_entry.insert(tk.END, values[3])
        self.precio_entry.insert(tk.END, values[4])

    def limpiar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

    def cerrar_ventana(self):
        self.toplevel.destroy()
