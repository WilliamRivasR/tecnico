"""for i in range(2, 9, 3):"""
"""fruits = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]

for i in fruits:
  print(i)
  if i == "e":
    break"""

"""abc = ["a", "b", "c", "d", "e", "f"]
for ad in abc:
  if ad == "a" or ad == "b":
    pass
    print(ad)"""

"""cadena = 'Python'
for letra in cadena:
    if letra == 'P':
        continue
    print(letra)"""

"""suma_pares = 0
for i in range(1, 11):
    if i % 2 != 0:
        continue  # Saltar números impares
    suma_pares += i

print("La suma de los números pares es:", suma_pares)"""

"""Cuenta las vocales en una cadena de texto.

  Parámetros:
    texto (str): La cadena de texto a analizar.

  Retorno:
    Un diccionario con las vocales como claves y sus conteos como valores.
  """

"""Cuenta las vocales en una cadena de texto.

  Parámetros:
    texto (str): La cadena de texto a analizar.

  Retorno:
    Un diccionario con las vocales como claves y sus conteos como valores.
  """




#1
"""def contar_vocales(texto):
  return {vocal: texto.count(vocal) for vocal in "aeiouAEIOU"}

texto = input("Ingrese una palabra o frase: ")
conteo_vocales = contar_vocales(texto)

for vocal, conteo in conteo_vocales.items():
  print(f"{vocal}: {conteo}")"""


#2
"""nombres = ["Fabio", "Felipe", "William", "Neyley", "Mariana"]
nombres.sort()
for nombre in nombres:
  print(nombre)"""


#3
"""nombres = ["jose", "maria","sara", "jesus", "james", "valeria", "daniel"]
for palabras in nombres:
    if "j" in palabras:
       print(palabras)"""


#4
"""suma_pares = 0
for i in range(1, 11):
    if i % 2 != 0:
        continue  # Saltar números impares
    suma_pares += i

print("La suma de los números pares es:", suma_pares)"""


"""x = 5
while x > 0:
    x -=1
    print(x)"""





"""lista = ["A", "b", 1, True, 1.80]
lista.append("vent")
print (lista)"""#['A', 'b', 1, True, 1.8, 'vent']

"""lista = ["A", "b", 1, True, 1.80]
lista.insert(1, "goku")
print (lista)"""#['A', 'goku', 'b', 1, True, 1.8]

"""lista = ["A", "b", 1, True, 1.80]
lista.extend(["goku le gana", "holu", 7])
print (lista)"""#['A', 'b', 1, True, 1.8, 'goku le gana', 'holu', 7]

"""lista = ["A", "b", 1, True, 1.80]
lista.remove(1)
print (lista)"""#['A', 'b', True, 1.8]

"""lista = ["A", "b", 1, True, 1.80]
lista.pop()
print (lista)"""#['A', 'b', 1, True]

"""lista = ["A", "b", 1, True, 1.80]
lista.reverse()
print (lista)"""#[1.8, True, 1, 'b', 'A']

"""lista = [8, 5, 4, 2, 8, 1, 9]
lista.sort()
print (lista)"""#[1, 2, 4, 5, 8, 8, 9]

"""lista = [8, 5, 4, 2, 8, 1, 9]
lista.sort(reverse=True)
print (lista)"""#[9, 8, 8, 5, 4, 2, 1]

"""lista = ["A", "b", 1, True, 1.80]
lista.clear()
print (lista)"""#[]

"""cuadrados = [x**2 for x in range(1, 11)]
print (cuadrados)"""#[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

"""lista = ["A", "b", 1, True, 1.80, "i"]
del lista[1]
print (lista)"""#['A', 1, True, 1.8, 'i']

"""lista = ["A", 2, "b", 1, True, 1.80, "i", 2]
cantidad = lista.count(2)
print (cantidad)"""#[2]

"""lista = ["A", 2, "b", 1, True, 1.80, "i", 2]
indice = lista.index(2)
print (indice)"""#cuenta el numero de veces q está 2 en la lista (1)

"""lista = ["A", 2, "b", 1, True, 1.80, "i", 2]
indice = len(lista)
print (indice)"""#cueta la cantidad de objetos en ua lista (8)

"""lista = {"A", 2, "b", 1, True, 1.80, "i", 2}
print (lista)"""#siempre imprime en orden distinto (al estar entre llaves es un set [conjunto])

"""lista = {"A", 2, "b", 1, True, 1.80, "i", 2}
for x in lista: 
 print (x)"""#lo itera 

"""frutas = {"manzana", "pera","uva","cereza", "cebolla"}
verduras = {"lechuga", "zanahoria","cebolla","verengena"}

solo_frutas = frutas - verduras
print (solo_frutas)"""#{'cereza', 'pera', 'manzana', 'uva'}

"""frutas = {"manzana", "pera","uva","cereza", "zanahoria"}
verduras = {"lechuga", "zanahoria","cebolla","verengena"}

solo_verduras = verduras - frutas
print (solo_verduras)"""#{'lechuga', 'verengena', 'cebolla'}

"""frutas = {"manzana", "pera","uva","cereza", "zanahoria"}
verduras = {"lechuga", "zanahoria","cebolla","verengena"}
print(frutas.difference(verduras))"""#lo mismo de arriba pero más corto

"""frutas = {"manzana", "pera","uva","cereza", "zanahoria"}
verduras = {"lechuga", "zanahoria","cebolla","verengena"}
print(frutas.union(verduras))"""#une los sets

"""frutas = {"manzana", "pera","uva","cereza", "zanahoria"}
verduras = {"lechuga", "zanahoria","cebolla","verengena"}
print(frutas.intersection(verduras))"""#los elementos q tienen en común





"""d1 = {
  "Nombre": "James",
  "Edad": 53,
  "Documento": 123456889
}

d2 = {
    "Nombre2": "Mariana",
    "Edad2": 23,
    "Documento2": 1003883
}"""

#d1.clear() #limpiar
#print(d1)

#print(d1.get("Nombre")) #elimnar un elemento

#it = d1.items() #muestra todos los elementos
#print(it)

#print(list(d1.values())) #muestra losvalores solamente

#d1.pop("Edad") #elimina un elemento
#print(d1)

#d1.popitem() #elemina un elemento aleatorio
#print(d1)

#d1.update(d2) #agrega los elementos del diccionario d2 al d1
#print(d1)





"""print("escriba su nombre: ")
nombre = input()

print("escriba su edad: ")
edad = input()

print("escriba su dirección: ")
direccion = input()

print("escriba su número: ")
numero = input()

usuario = {
    "nombre": nombre,
    "edad": edad,
    "direccion": direccion,
    "numero": numero
}

print (usuario["nombre"], "tiene", usuario["edad"], "años", "vive en", usuario["direccion"], "y su número es", usuario["numero"])"""






import tkinter as tk

def saludar():
  saludo.config(text="HOLUUUUUU")

def qtal():
  saludo.config(text="BIENNNN, soy una ventana y vos? :D")

def humano():
  saludo.config(text="OMGGG me lo esperaba :D")

def tmbn():
  saludo.config(text="OMGGGG YO TMBN")

def obtener_texto():
   texto_ingresado = entrada.get()
   etiqueta_resultado.config(text=f"La ventana te respondió: {texto_ingresado}")

# Crear una instancia de la ventana
ventana = tk.Tk()

# Configurar el tamaño de la ventana
ventana.geometry("300x200")

#tamaño maximo
ventana.maxsize(600,400)

#tamaño minimo
ventana.minsize(150,100)

# Configurar el título de la ventana
ventana.title("Ventana :D")

#Crea una etiqueta
saludo = tk.Label(ventana, text="Hola, soy una ventana")
saludo.pack()

# Crear un botón
boton_saludar = tk.Button(ventana, text="Saludar a la ventana", command=saludar)
boton_saludar.pack()

boton_qtal = tk.Button(ventana, text="q tal, ventanita?", command=qtal)
boton_qtal.pack()

boton_soyhuman = tk.Button(ventana, text="Un ser humano", command=humano)
boton_soyhuman.pack()

boton_soyventana = tk.Button(ventana, text="Una ventana", command=tmbn)
boton_soyventana.pack()

# Crear una entrada de texto
entrada = tk.Entry(ventana)
entrada.pack()

# Crear un botón que obtiene el texto ingresado
boton_obtener = tk.Button(ventana, text="Diselo a la ventana", command=obtener_texto)
boton_obtener.pack()

# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()

ventana.iconbitmap("favicon (2).ico")

"""ventana.configure(bg="LightYellow")
boton_saludar.configure(bg="Yellow") #el color del boton
boton_qtal.configure(bg="Yellow")
boton_soyhuman.configure(bg="Blue")
boton_soyventana.configure(bg="Red")"""
#ventana.attributes("-alpha",0.6) #transparencia

# Mostrar la ventana
ventana.mainloop()