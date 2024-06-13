class clsProducto:
    id = 0
    descripcion = ""
    precio = 0.0
    stock = 0
    marca = ""
    modelo = ""
    color = ""
    imagen = ""
    idMoto = 0
    idAccesorio = 0

    dicctemp = dict()

    def __init__(self, p_id, p_descripcion, p_precio, p_stock, p_marca, p_modelo, p_color, p_imagen, p_idMoto, p_idAccesorio):
        self.id = p_id
        self.descripcion = p_descripcion
        self.precio = p_precio
        self.stock = p_stock
        self.marca = p_marca
        self.modelo = p_modelo
        self.color = p_color
        self.imagen = p_imagen
        self.idMoto = p_idMoto
        self.idAccesorio = p_idAccesorio

        self.dicctemp["id"] = p_id
        self.dicctemp["descripcion"] = p_descripcion
        self.dicctemp["precio"] = p_precio
        self.dicctemp["stock"] = p_stock
        self.dicctemp["marca"] = p_marca
        self.dicctemp["modelo"] = p_modelo
        self.dicctemp["color"] = p_color
        self.dicctemp["imagen"] = p_imagen
        self.dicctemp["idMoto"] = p_idMoto
        self.dicctemp["idAccesorio"] = p_idAccesorio
