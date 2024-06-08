import tkinter as tk


def obtener_texto():
  numero1 = entrada1.get()
  numero2 = entrada2.get()
  suma = float(numero1) + float(numero2)
  etiqueta_resultado.config(text=f"El resultado es: {suma}")

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

#Crea una etiqueta
saludo = tk.Label(ventana, text="Ingresa solo numeros")
saludo.grid(row=0, column=1)

spacer = tk.Label(ventana, width=20)  # Create a spacer widget
spacer.grid(row=1, column=0)



# Crear una entrada de texto
entrada1 = tk.Entry(ventana)
entrada1.grid(row=1, column=1)

spacer = tk.Label(ventana, width=20)  # Create a spacer widget
spacer.grid(row=2, column=1)

entrada2 = tk.Entry(ventana)
entrada2.grid(row=3, column=1)

# Crear un botón que obtiene el texto ingresado
boton_obtener = tk.Button(ventana, text="Suma", command=obtener_texto)
boton_obtener.grid(row=4, column=1)
# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.grid(row=5, column=1, columnspan=2)

ventana.rowconfigure(8, weight=1)

ventana.iconbitmap("favicon (2).ico")

ventana.mainloop()