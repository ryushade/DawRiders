class clsCarrito:
    id = 0
    idCliente = 0
    fechaCreacion = ""


    dicccarrito = dict()

    def __init__(self, p_id, p_idCliente, p_fechaCreacion):
        self.id = p_id
        self.idCliente = p_idCliente
        self.fechaCreacion = p_fechaCreacion

        self.dicccarrito["id"] = p_id
        self.dicccarrito["idCliente"] = p_idCliente
        self.dicccarrito["fechaCreacion"] = p_fechaCreacion
