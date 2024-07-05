from bd import obtener_conexion

def insertar_administrador(cliente_id, fecha_asignacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ADMINISTRADOR(cliente_id, fecha_asignacion) VALUES (%s, %s)",
            (cliente_id, fecha_asignacion))
    conexion.commit()
    conexion.close()

def insertar_administrador_api(cliente_id, fecha_asignacion):
    conexion = obtener_conexion()
    id_generado = None  # Inicializa la variable para el ID generado
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ADMINISTRADOR(cliente_id, fecha_asignacion) VALUES (%s, %s)",
                (cliente_id, fecha_asignacion))
            cursor.execute("SELECT LAST_INSERT_ID()")  # Consulta para obtener el último ID insertado
            id_generado = cursor.fetchone()[0]  # Obtiene el ID generado de la fila resultante
        conexion.commit()
    finally:
        conexion.close()
    return id_generado


def actualizar_administrador(cliente_id, fecha_asignacion, idAdmin):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE ADMINISTRADOR SET cliente_id = %s, fecha_asignacion = %s WHERE idAdmin = %s",
            (cliente_id, fecha_asignacion, idAdmin))
    conexion.commit()
    conexion.close()



def eliminar_administrador(idAdmin):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM ADMINISTRADOR WHERE idAdmin = %s", (idAdmin,))
    conexion.commit()
    conexion.close()


def obtener_administradores():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idAdmin, cliente_id, fecha_asignacion FROM ADMINISTRADOR")
        administradores = cursor.fetchall()
    conexion.close()
    return administradores


def obtener_administrador_por_id(idAdmin):
    conexion = obtener_conexion()
    admin = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idAdmin, cliente_id, fecha_asignacion FROM ADMINISTRADOR WHERE idAdmin = %s", (idAdmin,))
        admin = cursor.fetchone()
    conexion.close()
    return admin


def obtener_administrador_por_cliente_id(cliente_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM ADMINISTRADOR WHERE cliente_id = %s", (cliente_id,))
            result = cursor.fetchone()
            return result
    finally:
        conexion.close()
