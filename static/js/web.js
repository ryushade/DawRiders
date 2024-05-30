$(document).on('click', '.edit', function() {
    var motoId = $(this).data('moto-id'); // Asegúrate de que el enlace tiene un atributo `data-moto-id`
    // Luego, carga los datos usando AJAX o tomando los valores de algún lugar de tu página
    $.ajax({
        url: '/get-moto-details', // La URL donde tu backend puede devolver los datos de la moto
        method: 'GET',
        data: {id: motoId},
        success: function(response) {
            // Suponiendo que la respuesta es un objeto con los datos de la moto
            $('#editEmployeeModal' + motoId).find('#codmoto').val(response.codmoto);
            $('#editEmployeeModal' + motoId).find('#tipo').val(response.tipo);
            // Completa para otros campos...
        }
    });
});

$('.edit').click(function() {
    var motoId = $(this).data('moto-id');  // Obtiene el ID desde el atributo data-moto-id
    $('#editMotoModal' + motoId).modal('show');  // Usa el ID para abrir el modal específico
});
