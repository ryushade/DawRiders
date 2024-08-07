from bd import obtener_conexion

def insertar_accesorio(codaccesorio, tipo, material):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ACCESORIO(codaccesorio, tipo, material) VALUES (%s, %s, %s)",
            (codaccesorio, tipo, material))
    conexion.commit()
    conexion.close()

def insertar_accesorio_api(codaccesorio, tipo, material):
    conexion = obtener_conexion()
    id_generado = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ACCESORIO(codaccesorio, tipo, material) VALUES (%s, %s, %s)",
                (codaccesorio, tipo, material))
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_generado = cursor.fetchone()[0]

        conexion.commit()
    finally:
        conexion.close()
    return id_generado


def obtener_accesorios():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT codaccesorio, tipo, material FROM ACCESORIO")
        accesorios = cursor.fetchall()
    conexion.close()
    return accesorios

def obtener_accesorios_api():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idAccesorio, codaccesorio, tipo, material FROM ACCESORIO")
        accesorios = cursor.fetchall()
    conexion.close()
    return accesorios

def eliminar_accesorio(codaccesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM ACCESORIO WHERE codaccesorio = %s", (codaccesorio,))
    conexion.commit()
    conexion.close()

def eliminar_accesorio_api(id_accesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM ACCESORIO WHERE idAccesorio = %s", (id_accesorio,))
    conexion.commit()
    conexion.close()

def actualizar_accesorio(codaccesorio, tipo, material, id_accesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE ACCESORIO SET codaccesorio = %s, tipo = %s, material = %s WHERE idAccesorio = %s",
            (codaccesorio, tipo, material, id_accesorio))
    conexion.commit()
    conexion.close()

def obtener_accesorio_por_id(id_accesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM ACCESORIO WHERE idAccesorio = %s", (id_accesorio,))
        accesorio = cursor.fetchone()
    conexion.close()
    return accesorio

def obtener_cod_accesorio(codAccesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idAccesorio FROM ACCESORIO where codAccesorio = %s", (codAccesorio))
        accesorios = cursor.fetchall()
    conexion.close()
    return accesorios

def eliminar_accesorio_por_cod(codAccesorio):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM ACCESORIO WHERE codaccesorio = %s", (codAccesorio,))
        conexion.commit()
    except Exception as e:
        print(f"No se pudo eliminar el accesorio con cod {codAccesorio} debido a: {e}")
    finally:
        conexion.close()