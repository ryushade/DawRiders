from bd import obtener_conexion

def insertar_moto(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO MOTO(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento))
    conexion.commit()
    conexion.close()

def obtener_motos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento FROM MOTO")
        motos = cursor.fetchall()
    conexion.close()
    return motos

def obtener_motos_api():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMoto, codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento FROM MOTO")
        motos = cursor.fetchall()
    conexion.close()
    return motos

def eliminar_moto(id_moto):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM MOTO WHERE idMoto = %s", (id_moto,))
        conexion.commit()
    except Exception as e:
        print(f"No se pudo eliminar la moto con id {id_moto} debido a: {e}")
    finally:
        conexion.close()

def actualizar_moto(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento, id_moto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE MOTO SET codmoto = %s, tipo = %s, posicionManejo = %s, numAsientos = %s, numPasajeros = %s, largo = %s, ancho = %s, alto = %s, tipoMotor = %s, combustible = %s, numCilindros = %s, capacidadTanque = %s, rendimiento = %s WHERE idMoto = %s",
            (codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento, id_moto))
    conexion.commit()
    conexion.close()

def obtener_moto_por_id(id_moto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM MOTO WHERE idMoto = %s", (id_moto,))
        moto = cursor.fetchone()
    conexion.close()
    return moto

def obtener_cod_moto(codMoto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idMoto FROM MOTO where codMoto = %s", (codMoto))
        motos = cursor.fetchall()
    conexion.close()
    return motos

def eliminar_moto(codmoto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM MOTO WHERE codmoto = %s", (codmoto,))
    conexion.commit()
    conexion.close()