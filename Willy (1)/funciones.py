"""
#funcion para saludar

def saludar(nombre):
  #Función que saluda a una persona por su nombre.
  print(f"¡Hola, {nombre}!")

# Ejemplo de uso
saludar(input("¿Cuál es tu nombre? "))  # Imprime: ¡Hola, Juan!"""

"""#funcion para sumar

def sumar(num1, num2):
  #Función que suma dos números.
 
  return float(num1) + float(num2)

# Ejemplo de uso
a = input("Ingrese el primer número: ")
b = input("Ingrese el segundo número: ")

resultado = sumar(a, b)
print(f"La suma de {a} y {b} es: {resultado}")  # Imprime: La suma de 5 y 3 es: 8"""


"""#funcion para restar

def restar(num1, num2):
  #Función que suma dos números.
  
  return  float(num1) - float(num2)

# Ejemplo de uso
a = input("Ingrese el primer número: ")
b = input("Ingrese el segundo número: ")

resultado = restar(a, b)
print(f"La resta de {a} y {b} es: {resultado}")  # Imprime: La resta de 5 y 3 es: 2"""





"""class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    def saludar(self):
        print(f"{self.nombre} tiene {self.edad} años.")

# Crear instancias de la clase Persona
persona1 = Persona("Juan", 30)
persona2 = Persona("María", 25)
persona3 = Persona("Anna", 47)
persona4 = Persona("José", 78)
persona5 = Persona("Neyley", 18)

persona1.saludar()       
persona2.saludar()






class Carro:
    def __init__(self, marca, placa):
        self.marca = marca
        self.placa = placa
    
    def carro(self):
        print(f"Carro Marca: {self.marca} Carro Placa: {self.placa}")

# Crear instancias de la clase Persona
carro1 = Carro("Uno", "243")
carro2 = Carro("Xiaomi", "258")

carro1.carro()       
carro2.carro()





class Televisor:
    def __init__(self, marca, pulgadas):
        self.marca = marca
        self.pulgadas = pulgadas
    
    def televisor(self):
        print(f"Televisor Marca: {self.marca} Televisor Pulgadas: {self.pulgadas}")

# Crear instancias de la clase Persona
televisor1 = Televisor("Samsung", "56")
televisor2 = Televisor("Hawei", "23")

# Acceder a los atributos y métodos de las instancias
televisor1.televisor()       
televisor2.televisor()       






class Moto:
    def __init__(self, marca, placa):
        self.marca = marca
        self.placa = placa
    
    def moto(self):
        print(f"Moto Marca: {self.marca} Moto Placa: {self.placa}")

# Crear instancias de la clase Persona
moto1 = Moto("Pulsar", "56")
moto2 = Moto("Hawei", "23")

# Acceder a los atributos y métodos de las instancias
moto1.moto()       
moto2.moto()"""




"""""class Vehiculo:
  def __init__(self, marca, modelo, año, color, kilometraje):
    self.marca = marca
    self.modelo = modelo
    self.año = año
    self.color = color
    self.kilometraje = kilometraje

class Carro(Vehiculo):
  def __init__(self, marca, modelo, año, color, kilometraje, tipo_carroceria):
    super().__init__(marca, modelo, año, color, kilometraje)
    self.tipo_carroceria = tipo_carroceria

class Tractomula(Vehiculo):
  def __init__(self, marca, modelo, año, color, kilometraje, capacidad_carga):
    super().__init__(marca, modelo, año, color, kilometraje)
    self.capacidad_carga = capacidad_carga

class Tractor(Vehiculo):
  def __init__(self, marca, modelo, año, color, kilometraje, potencia):
    super().__init__(marca, modelo, año, color, kilometraje)
    self.potencia = potencia

class Terraneitor(Vehiculo):
  def __init__(self, marca, modelo, año, color, kilometraje, altura_libre):
    super().__init__(marca, modelo, año, color, kilometraje)
    self.altura_libre = altura_libre


carro1 = Carro("Toyota", "Corolla", 2020, "Rojo", 50000, "Sedan")
tracto1 = Tractomula("Kenworth", "T680", 2022, "Azul", 100000, 50000)
tractor1 = Tractor("John Deere", "9R", 2023, "Verde", 20000, 400)
terraneitor1 = Terraneitor("Hummer", "De Otro Mundo", 2021, "Negro", 350, "10cm")


print(f"Carro: Marca: {carro1.marca} Modelo: {carro1.modelo} Año: {carro1.año} Color: {carro1.color} Kilometraje: {carro1.kilometraje} Tipo de Carrocería: {carro1.tipo_carroceria}")
print(f"Tractomula: Marca: {tracto1.marca} Modelo: {tracto1.modelo} Año: {tracto1.año} Color: {tracto1.color} Kilometraje: {tracto1.kilometraje} Capacidad de Carga: {tracto1.capacidad_carga}")
print(f"Tractor: Marca: {tractor1.marca} Modelo: {tractor1.modelo} Año: {tractor1.año} Color: {tractor1.color} Kilometraje: {tractor1.kilometraje} Potencia: {tractor1.potencia}")
print(f"Terraneitor: Marca: {terraneitor1.marca} Modelo: {terraneitor1.modelo} Año: {terraneitor1.año} Color: {terraneitor1.color} Kilometraje: {terraneitor1.kilometraje} Altura Libre: {terraneitor1.altura_libre}")"""""





class latam:
  def __init__(self, region, español, petroleo):
    self.region = region
    self.español = español
    self.petroleo = petroleo


class Venezuela(latam):
  def __init__(self, region, español, petroleo, biodiversidad):
    super().__init__(region, español, petroleo)
    self.biodiversidad = biodiversidad