from bd import obtener_conexion

def insertar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO VENTA1(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final))
    conexion.commit()
    conexion.close()

def obtener_ventas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final FROM VENTA1")
        ventas = cursor.fetchall()
    conexion.close()
    return ventas

def eliminar_venta(idVenta1):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM VENTA1 WHERE idVenta1 = %s", (idVenta1,))
        conexion.commit()
    except Exception as e:
        print(f"No se pudo eliminar la moto con id {idVenta1} debido a: {e}")
    finally:
        conexion.close()

def actualizar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, idVenta1):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE VENTA1 SET nombre = %s, apellidos = %s, pais = %s, direccion = %s, region = %s, localidad = %s, telefono = %s, correo = %s, mes = %s, año = %s, cvv = %s, numtarjeta = %s, idProducto = %s, monto_final = %s WHERE idVenta1 = %s",
            (nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, idVenta1))
    conexion.commit()
    conexion.close()

def obtener_venta_por_id(idVenta1):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM VENTA1 WHERE idVenta1 = %s", (idVenta1,))
        venta = cursor.fetchone()
    conexion.close()
    return venta

def obtener_venta_por_id_api():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM VENTA1")
        venta = cursor.fetchone()
    conexion.close()
    return venta
