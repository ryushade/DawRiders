from bd import obtener_conexion

def insertar_administrador(cliente_id, fecha_asignacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ADMINISTRADOR(cliente_id, fecha_asignacion) VALUES (%s, %s)",
            (cliente_id, fecha_asignacion))
    conexion.commit()
    conexion.close()


def actualizar_administrador(cliente_id, fecha_asignacion, idAdmin):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE CLIENTE SET cliente_id = %s, fecha_asignacion = %s WHERE idAdmin = %s",
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