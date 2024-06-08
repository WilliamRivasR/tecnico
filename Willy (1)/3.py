import tkinter as tk

# Función para crear la ventana

ventana = tk.Tk()  # Crear una instancia de la ventana principal
ventana.geometry("300x200")  # Tamaño de la ventana
    
    # Crear un widget de etiqueta para mostrar texto
etiqueta = tk.Label(ventana, text="¡Hola, mundo!")
etiqueta.pack()  # Agregar la etiqueta a la ventana
    
ventana.mainloop()  # Mantener la ventana abierta

ventana.mainloop()