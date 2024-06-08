import mysql.connector
user = 'root'
password = ''
host = 'localhost'
database = 'northwind'
try:
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        passwd="1234",
        database=database,
    )

    cursor = conexion.cursor()

    # Ejecutar una consulta de eliminación
    cursor.execute("DELETE FROM employees WHERE EmployeeID = %s", (14,))

    # Confirmar los cambios
    conexion.commit()

    # Cerrar cursor y conexión
    cursor.close()

    print("Conexión exitosa")
except mysql.connector.Error as error:
    print("Error de conexión:", error)
finally:
    # Si la conexión se estableció, la cerramos
    if 'conexion' in locals() or 'conexion' in globals():
        conexion.close()