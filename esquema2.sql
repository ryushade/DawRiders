CREATE TABLE ACCESORIO (
    idAccesorio INT AUTO_INCREMENT PRIMARY KEY,
    codaccesorio VARCHAR(10) NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    material VARCHAR(255) NOT NULL
);

CREATE TABLE ADMINISTRADOR (
    idAdmin INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CARRITO (
    idCarrito INT AUTO_INCREMENT PRIMARY KEY,
    idCliente INT,
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CLIENTE (
    idCliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    token VARCHAR(255)
);

CREATE TABLE ITEM_CARRITO (
    idItemCarrito INT AUTO_INCREMENT PRIMARY KEY,
    idCarrito INT NOT NULL,
    idProducto INT NOT NULL,
    cantidad INT NOT NULL,
    precioPorUnidad DECIMAL(9,2) NOT NULL,
    subtotal DECIMAL(9,2)
);

CREATE TABLE MOTO (
    idMoto INT AUTO_INCREMENT PRIMARY KEY,
    codmoto VARCHAR(10) NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    posicionManejo VARCHAR(255) NOT NULL,
    numAsientos INT NOT NULL,
    numPasajeros INT NOT NULL,
    largo DECIMAL(9,2) NOT NULL,
    ancho DECIMAL(9,2) NOT NULL,
    alto DECIMAL(9,2) NOT NULL,
    tipoMotor VARCHAR(255) NOT NULL,
    combustible VARCHAR(255) NOT NULL,
    numCilindros INT NOT NULL,
    capacidadTanque DECIMAL(9,2) NOT NULL,
    rendimiento VARCHAR(255) NOT NULL
);

CREATE TABLE PRODUCTO (
    idProducto INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
    stock INT NOT NULL,
    marca VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    color VARCHAR(255) NOT NULL,
    imagen VARCHAR(255),
    idMoto INT,
    idAccesorio INT
);

CREATE TABLE VENTA1 (
    idVenta INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    pais VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    localidad VARCHAR(255) NOT NULL,
    telefono VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    mes VARCHAR(3) NOT NULL,
    año INT NOT NULL,
    cvv VARCHAR(3) NOT NULL,
    numTarjeta INT NOT NULL,
    idProducto INT,
    monto_final DECIMAL(9,2),
    num_venta int not null,
	idCliente int not null,
	cantidad int not null,

);


------POSTGRES

CREATE TABLE ACCESORIO (
    idAccesorio SERIAL PRIMARY KEY,
    codaccesorio VARCHAR(10) NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    material VARCHAR(255) NOT NULL
);

CREATE TABLE ADMINISTRADOR (
    idAdmin SERIAL PRIMARY KEY,
    cliente_id INT,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CARRITO (
    idCarrito SERIAL PRIMARY KEY,
    idCliente INT,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE CLIENTE (
    idCliente SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    token VARCHAR(255)
);

CREATE TABLE ITEM_CARRITO (
    idItemCarrito SERIAL PRIMARY KEY,
    idCarrito INT NOT NULL,
    idProducto INT NOT NULL,
    cantidad INT NOT NULL,
    precioPorUnidad DECIMAL(9,2) NOT NULL,
    subtotal DECIMAL(9,2)
);

CREATE TABLE MOTO (
    idMoto SERIAL PRIMARY KEY,
    codmoto VARCHAR(10) NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    posicionManejo VARCHAR(255) NOT NULL,
    numAsientos INT NOT NULL,
    numPasajeros INT NOT NULL,
    largo DECIMAL(9,2) NOT NULL,
    ancho DECIMAL(9,2) NOT NULL,
    alto DECIMAL(9,2) NOT NULL,
    tipoMotor VARCHAR(255) NOT NULL,
    combustible VARCHAR(255) NOT NULL,
    numCilindros INT NOT NULL,
    capacidadTanque DECIMAL(9,2) NOT NULL,
    rendimiento VARCHAR(255) NOT NULL
);

CREATE TABLE PRODUCTO (
    idProducto SERIAL PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
    stock INT NOT NULL,
    marca VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    color VARCHAR(255) NOT NULL,
    imagen VARCHAR(255),
    idMoto INT,
    idAccesorio INT
);

CREATE TABLE VENTA1 (
    idVenta SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    pais VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    localidad VARCHAR(255) NOT NULL,
    telefono VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    mes VARCHAR(3) NOT NULL,
    año INT NOT NULL,
    cvv VARCHAR(3) NOT NULL,
    numTarjeta BIGINT NOT NULL,
    idProducto INT,
    monto_final DECIMAL(9,2),
    num_venta INT NOT NULL,
	idCliente int not null,
	cantidad int not null
);