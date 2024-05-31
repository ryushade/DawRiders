class clsAdministrador:
    id = 0
    cliente_id = ""
    fecha_asignacion = ""

    diccadmin = dict()

    def __init__(self, p_id, p_cliente_id, p_fecha_asignacion):
        self.id = p_id
        self.cliente_id = p_cliente_id
        self.fecha_asignacion = p_fecha_asignacion

        self.diccadmin["id"] = p_id
        self.diccadmin["cliente_id"] = p_cliente_id
        self.diccadmin["fecha_asignacion"] = p_fecha_asignacion







