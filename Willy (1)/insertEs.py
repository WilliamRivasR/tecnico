import mysql.connector
user = 'root'
password = ''
host = 'localhost'
database = 'biblioteca_escolar'

Tipo_usuario = "1"
Apellidos = 'Mosquera'
Nombre = 'Jmes'
Fecha_nacimiento = '1990-01-01'
Tipo_documento = '1'
Numero_documento = '5783321'
Fecha_nacimiento = '19900124'
Correo_electronico ='jamesmosq@gmail.com'
Contraseña = 'JM1234'
Telefono = '76348912'

try:
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        passwd="",
        database=database
    )
    cursor = conexion.cursor()

    #  SQL
    insert_query = """INSERT INTO usuarios (Tipo_usuario, Nombre, Apellidos, Tipo_documento, Numero_documento, Fecha_nacimiento, Correo_electronico, Contraseña, Telefono)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    empleado_data = (Tipo_usuario, Nombre, Apellidos, Tipo_documento, Numero_documento, Fecha_nacimiento, Correo_electronico, Contraseña, Telefono)

    # Ejecutar la consulta
    cursor.execute(insert_query, empleado_data)

    # Confirmar la transacción
    conexion.commit()

    print("Nuevo empleado insertado correctamente.")

except mysql.connector.Error as error:
    print("Error al insertar el nuevo empleado:", error)

finally:
    if 'conexion' in locals() or 'conexion' in globals():
        conexion.close()