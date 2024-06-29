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

def eliminar_moto_por_cod(codMoto):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM MOTO WHERE codMoto = %s", (codMoto,))
        conexion.commit()
    except Exception as e:
        print(f"No se pudo eliminar la moto con cod {codMoto} debido a: {e}")
    finally:
        conexion.close()

def actualizar_moto(tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento, id_moto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE MOTO SET tipo = %s, posicionManejo = %s, numAsientos = %s, numPasajeros = %s, largo = %s, ancho = %s, alto = %s, tipoMotor = %s, combustible = %s, numCilindros = %s, capacidadTanque = %s, rendimiento = %s WHERE idMoto = %s",
            (tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento, id_moto))
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

###### APIS #########

def insertar_moto_api(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento):
    conexion = obtener_conexion()
    id_generado = None  # Inicializa la variable para el ID generado
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO MOTO(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento))
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_generado = cursor.fetchone()[0]  # Obtiene el ID generado de la fila resultante
        conexion.commit()
    finally:
        conexion.close()
    return id_generado
