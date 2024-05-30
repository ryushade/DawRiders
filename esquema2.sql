-- Creación de la tabla MOTO
CREATE TABLE MOTO (
    idMoto INT AUTO_INCREMENT PRIMARY KEY,
    codmoto varchar(10) NOT NULL,
    tipo VARCHAR(255)  NOT NULL,
    posicionManejo VARCHAR(255)  NOT NULL,
    numAsientos INT  NOT NULL, 
    numPasajeros INT  NOT NULL,
    largo DECIMAL(9,2)  NOT NULL,
    ancho DECIMAL(9,2)  NOT NULL,
    alto DECIMAL(9,2)  NOT NULL,
    tipoMotor VARCHAR(255)  NOT NULL,
    combustible VARCHAR(255)  NOT NULL,
    numCilindros INT  NOT NULL,
    capacidadTanque DECIMAL(9,2)  NOT NULL,
    rendimiento VARCHAR(255) NOT NULL
);

-- Creación de la tabla ACCESORIO
CREATE TABLE ACCESORIO (
    idAccesorio INT AUTO_INCREMENT PRIMARY KEY,
    codaccesorio varchar(10) not null,
    tipo VARCHAR(255)  NOT NULL,
    material VARCHAR(255)  NOT NULL
);

-- Creación de la tabla PRODUCTO
    CREATE TABLE PRODUCTO (
        idProducto INT AUTO_INCREMENT PRIMARY KEY,
        descripcion VARCHAR(255)  NOT NULL,
        precio DECIMAL(9,2)  NOT NULL,
        stock INT  NOT NULL, 
        marca VARCHAR(255)  NOT NULL,
        modelo VARCHAR(255)  NOT NULL,
        color VARCHAR(255)  NOT NULL,
        imagen VARCHAR(255)  NOT NULL,
        idMoto INT null,
        idAccesorio INT null,
        FOREIGN KEY (idMoto) REFERENCES MOTO(idMoto)  MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, 
        FOREIGN KEY (idAccesorio) REFERENCES ACCESORIO(idAccesorio)  MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
    );

-- Creación de la tabla CARRITO
CREATE TABLE CARRITO (
    idCarrito INT AUTO_INCREMENT PRIMARY KEY,
    idCliente INT,
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idCliente) REFERENCES CLIENTE(idCliente) ON DELETE CASCADE
);

-- Creación de la tabla ITEM_CARRITO
CREATE TABLE ITEM_CARRITO (
    idItemCarrito INT AUTO_INCREMENT PRIMARY KEY,
    idCarrito INT NOT NULL,
    idProducto INT NOT NULL,
    cantidad INT NOT NULL,
    precioPorUnidad DECIMAL(9,2) NOT NULL,
    subtotal DECIMAL(9,2) AS (precioPorUnidad * cantidad) STORED,
    FOREIGN KEY (idCarrito) REFERENCES CARRITO(idCarrito) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) ON DELETE CASCADE
);

-- Creación de la tabla CLIENTE
CREATE TABLE CLIENTE (
    idCliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(20) NOT NULL,
    telefono VARCHAR(15) NOT NULL
);

-- Creación de la tabla VENTA
CREATE TABLE VENTA (
    idVenta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    idProducto INT NOT NULL,
    idCliente INT NOT NULL,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (idCliente) REFERENCES CLIENTE(idCliente) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Creación de la tabla TIPO_COMPROBANTE
CREATE TABLE TIPO_COMPROBANTE (
    idTipoComprobante INT AUTO_INCREMENT PRIMARY KEY,
    tipoComprobante VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);

-- Creación de la tabla COMPROBANTE_PAGO
CREATE TABLE COMPROBANTE_PAGO (
    idComprobante INT AUTO_INCREMENT PRIMARY KEY,
    montoTotal DECIMAL(9,2) NOT NULL,
    tipoPago VARCHAR(255) NOT NULL,
    fechaPago DATE NOT NULL,
    horaPago TIME NOT NULL,
    idVenta INT NOT NULL,
    idTipoComprobante INT,
    FOREIGN KEY (idVenta) REFERENCES VENTA(idVenta) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (idTipoComprobante) REFERENCES TIPO_COMPROBANTE(idTipoComprobante) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE Administrador (
    idAdmin INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(idCliente)
);

CREATE TABLE VENTA1 (
    idVenta1 INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    pais VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    localidad VARCHAR(255) NOT NULL,
    telefono VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    mes VARCHAR(255) NOT NULL,
    año INT NOT NULL,
    cvv VARCHAR(3) NOT NULL,
    numtarjeta INT NOT NULL,
    idProducto INT,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);