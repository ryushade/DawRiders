class clsMoto:
    id = 0
    codmoto = ""
    tipo = ""
    posicionManejo = ""
    numAsientos = 0
    numPasajeros = 0
    largo = 0.0
    ancho = 0.0
    alto = 0.0
    tipoMotor = ""
    combustible = ""
    numCilindros = 0
    capacidadTanque = 0.0
    rendimiento = ""

    diccmoto = dict()

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
        self.diccmoto["id"] = p_id
        self.diccmoto["codmoto"] = p_codmoto
        self.diccmoto["tipo"] = p_tipo
        self.diccmoto["posicionManejo"] = p_posicionManejo
        self.diccmoto["numAsientos"] = p_numAsientos
        self.diccmoto["numPasajeros"] = p_numPasajeros
        self.diccmoto["largo"] = p_largo
        self.diccmoto["ancho"] = p_ancho
        self.diccmoto["alto"] = p_alto
        self.diccmoto["tipoMotor"] = p_tipoMotor
        self.diccmoto["combustible"] = p_combustible
        self.diccmoto["numCilindros"] = p_numCilindros
        self.diccmoto["capacidadTanque"] = p_capacidadTanque
        self.diccmoto["rendimiento"] = p_rendimiento






