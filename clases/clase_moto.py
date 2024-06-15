class clsMoto:
    def __init__(self, p_id, p_codmoto, p_tipo, p_posicionManejo, p_numAsientos, p_numPasajeros, p_largo, p_ancho, p_alto, p_tipoMotor, p_combustible, p_numCilindros, p_capacidadTanque, p_rendimiento):
        self.id = p_id
        self.codmoto = p_codmoto
        self.tipo = p_tipo
        self.posicionManejo = p_posicionManejo
        self.numAsientos = p_numAsientos
        self.numPasajeros = p_numPasajeros
        self.largo = p_largo
        self.ancho = p_ancho
        self.alto = p_alto
        self.tipoMotor = p_tipoMotor
        self.combustible = p_combustible
        self.numCilindros = p_numCilindros
        self.capacidadTanque = p_capacidadTanque
        self.rendimiento = p_rendimiento

        self.diccmoto = {
            "id": p_id,
            "codmoto": p_codmoto,
            "tipo": p_tipo,
            "posicionManejo": p_posicionManejo,
            "numAsientos": p_numAsientos,
            "numPasajeros": p_numPasajeros,
            "largo": p_largo,
            "ancho": p_ancho,
            "alto": p_alto,
            "tipoMotor": p_tipoMotor,
            "combustible": p_combustible,
            "numCilindros": p_numCilindros,
            "capacidadTanque": p_capacidadTanque,
            "rendimiento": p_rendimiento
        }
