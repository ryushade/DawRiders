class clsVenta1:
    idVenta1 = 0
    nombre = ""
    apellidos = ""
    pais = ""
    direccion = ""
    region = ""
    localidad = ""
    telefono = ""
    correo = ""
    mes = ""
    año = 0
    cvv = ""
    numtarjeta = 0
    idProducto = 0
    monto_final = 0.0

    diccVenta1 = dict()

    def __init__(self, p_id_venta1, p_nombre, p_apellidos, p_pais, p_direccion, p_region, p_localidad, p_telefono, p_correo, p_mes, p_año, p_cvv, p_numtarjeta, p_id_Producto, p_monto_final):
        self.idVenta1 = p_id_venta1
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.pais = p_pais
        self.direccion = p_direccion
        self.region = p_region
        self.localidad = p_localidad
        self.telefono = p_telefono
        self.correo = p_correo
        self.mes = p_mes
        self.año = p_año
        self.cvv = p_cvv
        self.numtarjeta = p_numtarjeta
        self.idProducto = p_id_Producto
        self.monto_final = p_monto_final

        self.diccVenta1["idVenta1"] = p_id_venta1
        self.diccVenta1["nombre"] = p_nombre
        self.diccVenta1["apellidos"] = p_apellidos
        self.diccVenta1["pais"] = p_pais
        self.diccVenta1["direccion"] = p_direccion
        self.diccVenta1["region"] = p_region
        self.diccVenta1["localidad"] = p_localidad
        self.diccVenta1["telefono"] = p_telefono
        self.diccVenta1["correo"] = p_correo
        self.diccVenta1["mes"] = p_mes
        self.diccVenta1["año"] = p_año
        self.diccVenta1["cvv"] = p_cvv
        self.diccVenta1["numtarjeta"] = p_numtarjeta
        self.diccVenta1["idProducto"] = p_id_Producto
        self.diccVenta1["monto_final"] = p_monto_final