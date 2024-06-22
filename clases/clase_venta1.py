class clsVenta:
    def __init__(self, p_id, p_nombre, p_apellidos, p_pais, p_direccion, p_region, p_localidad, p_telefono, p_correo, p_mes, p_anio, p_cvv, p_numtarjeta, p_idProducto, p_monto_final, p_num_venta, p_idCliente, p_cantidad):
        self.id = p_id
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.pais = p_pais
        self.direccion = p_direccion
        self.region = p_region
        self.localidad = p_localidad
        self.telefono = p_telefono
        self.correo = p_correo
        self.mes = p_mes
        self.anio = p_anio  # Cambiado de 'año' a 'anio'
        self.cvv = p_cvv
        self.numtarjeta = p_numtarjeta
        self.idProducto = p_idProducto
        self.monto_final = p_monto_final
        self.num_venta = p_num_venta
        self.idCliente = p_idCliente
        self.cantidad = p_cantidad

        self.diccVenta = {
            "id": p_id,
            "nombre": p_nombre,
            "apellidos": p_apellidos,
            "pais": p_pais,
            "direccion": p_direccion,
            "region": p_region,
            "localidad": p_localidad,
            "telefono": p_telefono,
            "correo": p_correo,
            "mes": p_mes,
            "anio": p_anio,  # Cambiado de 'año' a 'anio'
            "cvv": p_cvv,
            "numtarjeta": p_numtarjeta,
            "idProducto": p_idProducto,
            "monto_final": p_monto_final,
            "num_venta": p_num_venta,
            "idCliente": p_idCliente,
            "cantidad": p_cantidad
        }
