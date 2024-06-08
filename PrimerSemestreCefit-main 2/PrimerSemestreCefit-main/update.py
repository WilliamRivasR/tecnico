import mysql.connector
user = 'root'
password = ''
host = 'localhost'
database = 'Northwind'

last_name = 'Mosquera'
first_name = 'Jmes'
birth_date = '1990-01-01'
photo = 'jaes-MR.jpg'
notes = 'New employee'

try:
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        passwd="1234",
        database=database
    )
    # Crear un cursor
    cursor = conexion.cursor()

    # Ejecutar una consulta de actualización
    cursor.execute("UPDATE employees SET FirstName = 'Jamecito' WHERE EmployeeID = %s", (11,))

    # Confirmar los cambios
    conexion.commit()
    print("Modificación exitosa")

except mysql.connector.Error as error:
    print("Error al modificar el nuevo empleado:", error)

finally:
    if 'conexion' in locals() or 'conexion' in globals():
        conexion.close()