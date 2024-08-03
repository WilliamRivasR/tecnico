"""import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo de Botón")

# Definir la función a ejecutar
def mi_funcion():
    print("¡El botón fue presionado!")

# Crear el botón y asociarlo a la función
boton = tk.Button(root, text="Presióname", command=mi_funcion)
boton.pack(pady=20)

# Ejecutar el bucle principal
root.mainloop()"""


#ventana modal
"""import tkinter as tk
from tkinter import simpledialog

def abrir_ventana_modal():
    # Crear una ventana Toplevel
    ventana_modal = tk.Toplevel(root)
    ventana_modal.title("Ventana Modal")

    # Configurar la ventana para que sea modal
    ventana_modal.transient(root)
    ventana_modal.grab_set()

    # Crear un Label y un Botón en la ventana modal
    label = tk.Label(ventana_modal, text="Esto es una ventana modal")
    label.pack(pady=20)

    boton_cerrar = tk.Button(ventana_modal, text="Cerrar", command=ventana_modal.destroy)
    boton_cerrar.pack(pady=20)

    # Esperar a que la ventana modal sea destruida antes de continuar
    root.wait_window(ventana_modal)

# Crear la ventana principal
root = tk.Tk()
root.title("Ventana Principal")

# Botón para abrir la ventana modal
boton_abrir_modal = tk.Button(root, text="Abrir Ventana Modal", command=abrir_ventana_modal)
boton_abrir_modal.pack(pady=20)

# Ejecutar el bucle principal
root.mainloop()"""


#detectar cuando hace clic
"""import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo de Detección de Clic en Botón")

# Definir la función que se ejecutará cuando el botón sea presionado
def on_button_click():
    print("¡El botón fue presionado!")

# Crear el botón y asociarlo a la función
boton = tk.Button(root, text="Presióname", command=on_button_click)
boton.pack(pady=20)

# Ejecutar el bucle principal
root.mainloop()"""


#menu desplegable
"""import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo de Menú Desplegable")

# Crear la barra de menú
barra_menu = tk.Menu(root)

# Crear un menú desplegable
menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=lambda: messagebox.showinfo("Nuevo", "Nuevo archivo creado"))
menu_archivo.add_command(label="Abrir", command=lambda: messagebox.showinfo("Abrir", "Archivo abierto"))
menu_archivo.add_command(label="Guardar", command=lambda: messagebox.showinfo("Guardar", "Archivo guardado"))
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)

# Añadir el menú desplegable a la barra de menú
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

# Crear otro menú desplegable
menu_editar = tk.Menu(barra_menu, tearoff=0)
menu_editar.add_command(label="Deshacer", command=lambda: messagebox.showinfo("Deshacer", "Acción deshecha"))
menu_editar.add_command(label="Rehacer", command=lambda: messagebox.showinfo("Rehacer", "Acción rehecha"))

# Añadir el menú desplegable a la barra de menú
barra_menu.add_cascade(label="Editar", menu=menu_editar)

# Configurar la ventana principal para utilizar la barra de menú
root.config(menu=barra_menu)

# Ejecutar el bucle principal
root.mainloop()"""


#PyQt
"""from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 300, 200)
        label = QLabel("¡Hola, PyQt5!", self)
        label.move(100, 100)

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec_()"""


#wxPython
"""from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 300, 200)
        label = QLabel("¡Hola, PyQt5!", self)
        label.move(100, 100)

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec_()"""



#Kivi
"""from kivy.app import App
from kivy.uix.label import Label

class MiAplicacion(App):
    def build(self):
        return Label(text="¡Hola, Kivy!")

if __name__ == "__main__":
    MiAplicacion().run()"""






