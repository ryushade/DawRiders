from bd import obtener_conexion
from datetime import datetime, timedelta


def insertar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            INSERT INTO VENTA1 (nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad))
            conexion.commit()
            print("Venta insertada correctamente")
    except Exception as e:
        print("Error al insertar venta:", e)
        conexion.rollback()
    finally:
        conexion.close()




def obtener_ventas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final FROM VENTA1")
        ventas = cursor.fetchall()
    conexion.close()
    return ventas

def obtener_ventas_dashboard():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idVenta1, nombre, apellidos, pais,direccion, region, localidad,telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, num_venta, cantidad, fechaVenta FROM VENTA1")
        ventas = cursor.fetchall()
    conexion.close()
    return ventas


def obtener_ventas_excel():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT p.imagen, p.marca, p.modelo, v.cantidad, p.precio, SUM(v.monto_final) AS total_pagado, v.fechaVenta, v.num_venta, cl.nombre, cl.apellidos, cl.email, cl.telefono
                FROM VENTA1 v
                INNER JOIN PRODUCTO p ON v.idProducto = p.idProducto
                INNER JOIN CLIENTE cl on v.idCliente = cl.idCliente
                GROUP BY v.num_venta, p.imagen, p.marca, p.modelo, v.cantidad, p.precio
                ORDER BY v.fechaVenta DESC
            """)
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

def eliminar_venta_pr(idProducto):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM VENTA1 WHERE idProducto = %s", (idProducto,))
        conexion.commit()
    except Exception as e:
        print(f"No se pudo eliminar la venta con id de producto {idVenta1} debido a: {e}")
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


def obtener_ventas_por_cliente(id_cliente):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT p.imagen, p.marca, p.modelo, v.cantidad, p.precio, SUM(v.monto_final) AS total_pagado, v.fechaVenta, v.num_venta, cl.nombre, cl.apellidos, cl.email, cl.telefono
                FROM VENTA1 v
                INNER JOIN PRODUCTO p ON v.idProducto = p.idProducto
                INNER JOIN CLIENTE cl on v.idCliente = cl.idCliente
                WHERE v.idCliente = %s
                GROUP BY v.num_venta, p.imagen, p.marca, p.modelo, v.cantidad, p.precio
                ORDER BY v.fechaVenta DESC
            """, (id_cliente,))
            ventas = cursor.fetchall()
    except Exception as e:
        print("Error al obtener el historial de ventas:", e)
        ventas = []
    finally:
        conexion.close()
    return ventas

def obtener_todas_las_ventas():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT p.imagen, p.marca, p.modelo, v.cantidad, p.precio, SUM(v.monto_final) AS total_pagado, v.fechaVenta, v.num_venta, cl.nombre, cl.apellidos, cl.email, cl.telefono
                FROM VENTA1 v
                INNER JOIN PRODUCTO p ON v.idProducto = p.idProducto
                INNER JOIN CLIENTE cl on v.idCliente = cl.idCliente
                GROUP BY v.num_venta, p.imagen, p.marca, p.modelo, v.cantidad, p.precio
                ORDER BY v.fechaVenta DESC
            """)
            ventas = cursor.fetchall()
    except Exception as e:
        print("Error al obtener el historial de ventas:", e)
        ventas = []
    finally:
        conexion.close()
    return ventas

###### APIS

def api_insertar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, anio, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad, fechaVenta=None):
    conexion = obtener_conexion()
    id_generado = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO VENTA1(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad, fechaVenta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, anio, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad, fechaVenta if fechaVenta else datetime.now()))
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_generado = cursor.fetchone()[0]
        conexion.commit()
    finally:
        conexion.close()
    return id_generado



def api_editar_venta(id, nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, anio, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad, fechaVenta):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE VENTA1 SET nombre = %s, apellidos = %s, pais = %s, direccion = %s, region = %s, localidad = %s, telefono = %s, correo = %s, mes = %s, año = %s, cvv = %s, numtarjeta = %s, idProducto = %s, monto_final = %s, num_venta = %s, idCliente = %s, cantidad = %s, fechaVenta = %s WHERE idVenta1 = %s",
            (nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, anio, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad, fechaVenta, id))
    conexion.commit()
    conexion.close()


def api_eliminar_venta(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM VENTA1 WHERE idVenta1 = %s", (id,))
    conexion.commit()
    conexion.close()

def api_obtener_ventas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM VENTA1")
        ventas = cursor.fetchall()
    conexion.close()
    return ventas

def api_obtener_venta_por_id(id):
    conexion = obtener_conexion()
    venta = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM VENTA1 WHERE idVenta1 = %s", (id,))
        venta = cursor.fetchone()
    conexion.close()
    return venta

