class clsAccesorio:
    def __init__(self, p_id, p_codaccesorio, p_tipo, p_material):
        self.id = p_id
        self.codaccesorio = p_codaccesorio
        self.tipo = p_tipo
        self.material = p_material

        self.diccaccesorio = {
            "id": p_id,
            "codaccesorio": p_codaccesorio,
            "tipo": p_tipo,
            "material": p_material
        }
