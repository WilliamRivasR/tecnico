import tkinter as tk

# Crear una instancia de la ventana
ventana = tk.Tk()

# Configurar el tamaño de la ventana
ventana.geometry("300x200")

#tamaño maximo
ventana.maxsize(600,400)

#tamaño minimo
ventana.minsize(150,100)

# Configurar el título de la ventana
ventana.title("Suma :D")


# Crear un botón y colocarlo en la fila 2, columna 1
button = tk.Button(ventana, text="Click me")
button.grid(row=1, column=1)

# Crear un botón y colocarlo en la fila 2, columna 1
button = tk.Button(ventana, text="Click me")
button.grid(row=1, column=2)

# Crear un botón y colocarlo en la fila 2, columna 1
entrada1 = tk.Entry(ventana)
entrada1.grid(row=0, column=1)

entrada1 = tk.Entry(ventana)
entrada1.grid(row=0, column=1)


ventana.mainloop()