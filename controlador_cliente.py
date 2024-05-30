from bd import obtener_conexion

def insertar_cliente(nombre, apellidos, email, contraseña, telefono):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO cliente(nombre, apellidos, email, contraseña, telefono) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellidos, email, contraseña, telefono))
    conexion.commit()
    conexion.close()

def obtener_clientes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idCliente, nombre, apellidos, email, contraseña, telefono FROM cliente")
        clientes = cursor.fetchall()
    conexion.close()
    return clientes

def eliminar_cliente(id_cliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (id_cliente,))
    conexion.commit()
    conexion.close()

def actualizar_cliente(nombre, apellidos, email, contraseña, telefono, id_cliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE cliente SET nombre = %s, apellidos = %s, email = %s, contraseña = %s, telefono = %s WHERE idCliente = %s",
            (nombre, apellidos, email, contraseña, telefono, id_cliente))
    conexion.commit()
    conexion.close()

def obtener_cliente_por_id(id_cliente):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idCliente, nombre, apellidos, email, contraseña, telefono FROM cliente WHERE idCliente = %s", (id_cliente,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def obtener_cliente_por_email(email):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idCliente, nombre, apellidos, email, contraseña, telefono FROM cliente WHERE email = %s", (email,))
        cliente = cursor.fetchone()
    conexion.close()
    return cliente


def obtener_usuario_por_email(email):
    # Open database connection
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Assuming 'users' table has columns 'id', 'email', 'contraseña' etc.
        cursor.execute("""
            SELECT u.idCliente, u.email, u.contraseña, 
                   CASE WHEN a.cliente_id IS NOT NULL THEN TRUE ELSE FALSE END as is_admin
            FROM cliente u
            LEFT JOIN administrador a ON u.idCliente = a.cliente_id
            WHERE u.email = %s
        """, (email,))
        result = cursor.fetchone()
        if result:
            return {'id': result[0], 'email': result[1], 'contraseña': result[2], 'is_admin': result[3]}
        else:
            return None



def obtener_contrasena_por_email(email):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT contraseña FROM cliente WHERE email = %s", (email,))
        cliente = cursor.fetchone()
    conexion.close()
    if cliente:
        return cliente[0]
    else:
        return None