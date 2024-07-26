// ESTA FUNCION NO PERMITE BLOQUEAR LA ENTRADA DE NUMEROS EN LOS INPUTS 

function eliminarNumeros(event) {
    var input = event.target;
    input.value = input.value.replace(/\d/g, ''); // Eliminar números
}

// Función para eliminar letras de la entrada en tiempo real
function eliminarLetras(event) {
    var input = event.target;
    input.value = input.value.replace(/[a-zA-Z]/g, ''); // Eliminar letras
}
