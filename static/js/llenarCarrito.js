document.addEventListener('DOMContentLoaded', function () {
    var datosGuardados = localStorage.getItem("elementos_carrito");
    var contenedor = document.getElementById('detalle');

    if (datosGuardados) {
        var datosComoObjetos = JSON.parse(datosGuardados);
        actualizarHTML(datosComoObjetos);
    }

    contenedor.addEventListener('click', function(e) {
        if (e.target.classList.contains('increment') || e.target.classList.contains('decrement')) {
            var index = parseInt(e.target.getAttribute('data-index'), 10);
            var isIncrement = e.target.classList.contains('increment');
            changeQuantity(index, isIncrement);
        }
    });
});

function changeQuantity(index, isIncrement) {
    console.log('Index:', index, 'Is Increment:', isIncrement);  // Debugging
    var datosGuardados = localStorage.getItem("elementos_carrito");
    if (datosGuardados) {
        var datosComoObjetos = JSON.parse(datosGuardados);
        var cantidadActual = datosComoObjetos[index].cantidad;
        console.log('Cantidad Actual antes de cambiar:', cantidadActual);  // Debugging

        if (isIncrement) {
            datosComoObjetos[index].cantidad = cantidadActual + 1;
        } else {
            if (cantidadActual > 1) {
                datosComoObjetos[index].cantidad = cantidadActual - 1;
            }
        }

        console.log('Nueva Cantidad:', datosComoObjetos[index].cantidad);  // Debugging
        localStorage.setItem("elementos_carrito", JSON.stringify(datosComoObjetos));
        actualizarHTML(datosComoObjetos);
    }
}


function actualizarHTML(datosComoObjetos) {
    var contenedor = document.getElementById('detalle');
    var nuevoHTML = '';
    var total = 0;

    datosComoObjetos.forEach(function(item, i) {
        var precio = parseFloat(item.precio);
        var cantidad = item.cantidad;
        var subtotal = precio * cantidad;

        nuevoHTML += '<tr>' +
            '<td class="w-50">' +
            '<img src="' + item.imagen + '" alt="" class="img-fluid w-25 img_prod">' +
            '<span class="nombre_prod">' + item.nombre + '</span>' +
            '</td>' +
            '<td>' +
            'S/.<span class="precio_prod">' + precio + '</span>' +
            '</td>' +
            '<td>' +
            '<button style="margin-right:10px;" data-index="' + i + '" class="decrement">-</button>' +
            '<span class="cant_prod">' + cantidad + '</span>' +
            '<button style="margin-left:10px;" data-index="' + i + '" class="increment">+</button>' +
            '</td>' +
            '<td>' +
            'S/.<span class="subtotal_prod">' + subtotal.toFixed(2) + '</span>' +
            '</td>' +
            '</tr>';

        total += subtotal;
    });

    contenedor.innerHTML = nuevoHTML;
    document.querySelector('.subtotal').textContent = total.toFixed(2);
}
