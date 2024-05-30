function aplicar_cupon() {
    // Obtén los elementos por sus ID
    var desc = document.getElementById('descuento');
    var codigo = document.getElementById('codigo_descuento');
    var valor = codigo.value;
    desc.innerHTML = valor;
}

document.addEventListener('DOMContentLoaded', function () {
    var elementosAgregarC = document.getElementsByClassName('agregar_C');

    for (var i = 0; i < elementosAgregarC.length; i++) {
        elementosAgregarC[i].addEventListener('click', agregar_carrtito);
    }

    // Actualiza el contador del carrito al cargar la página
    actualizarContadorCarrito();
});

function agregar_carrtito(event) {
    var elemnt = event.target.id;
    var button = document.getElementById(elemnt);
    var padreDelDiv = button.parentNode.parentNode.parentNode;

    // Obtén la imagen, nombre y precio del producto
    var imagen = padreDelDiv.querySelector('.img_prod').src;
    var nombre_prod = padreDelDiv.querySelector('.nombre_prod').textContent;
    var precio_prod = parseFloat(padreDelDiv.querySelector('.precio_prod').textContent); // Convierte el precio a float

    // Obtén los datos guardados en localStorage, si no hay datos, usa un array vacío
    var datosGuardados = localStorage.getItem("elementos_carrito") ? JSON.parse(localStorage.getItem("elementos_carrito")) : [];

    // Verifica si el producto ya existe en el carrito
    var elementoExistente = datosGuardados.find(function (elemento) {
        return elemento.nombre === nombre_prod;
    });

    if (elementoExistente) {
        // Si existe, incrementa la cantidad
        elementoExistente.cantidad += 1;
    } else {
        // Si no existe, crea un nuevo elemento y añádelo al carrito
        var nuevoDato = {
            imagen: imagen,
            nombre: nombre_prod,
            precio: precio_prod,
            cantidad: 1
        };
        datosGuardados.push(nuevoDato);
    }

    // Guarda los datos actualizados en localStorage
    localStorage.setItem("elementos_carrito", JSON.stringify(datosGuardados));

    // Actualiza el contador del carrito
    actualizarContadorCarrito();
}

function actualizarContadorCarrito() {
    // Recupera los datos del carrito desde localStorage
    var datosGuardados = localStorage.getItem("elementos_carrito") ? JSON.parse(localStorage.getItem("elementos_carrito")) : [];
    var totalQuantity = datosGuardados.reduce(function (total, elemento) {
        return total + elemento.cantidad;
    }, 0);

    // Encuentra el elemento span y actualiza su contenido con la cantidad total
    var spanElement = document.querySelector('.fa-cart-shopping span');
    spanElement.textContent = totalQuantity;
}
