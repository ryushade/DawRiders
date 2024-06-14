class clsAccesorio:
    id = 0
    codaccesorio = ""
    tipo = ""
    material = ""

    diccaccesorio = dict()

    def __init__(self, p_id, p_codaccesorio, p_tipo, p_material):
        self.id = p_id
        self.codaccesorio = p_codaccesorio
        self.tipo = p_tipo
        self.material = p_material

        self.diccaccesorio["id"] = p_id
        self.diccaccesorio["codaccesorio"] = p_codaccesorio
        self.diccaccesorio["tipo"] = p_tipo
        self.diccaccesorio["material"] = p_material







