
    // Obtener el elemento donde se mostrarán las notificaciones
    const contenedorNotificaciones = document.getElementById('contenedor-notificaciones');

    // Función para mostrar las notificaciones
    function mostrarNotificaciones(notificaciones) {
        // Limpiar el contenedor de notificaciones
        contenedorNotificaciones.innerHTML = '';

        // Crear y agregar elementos de notificación al contenedor
        notificaciones.forEach(notificacion => {
            const item = document.createElement('div');
            item.textContent = notificacion.contenido;
            contenedorNotificaciones.appendChild(item);
        });
    }

    // Función para obtener y mostrar las notificaciones
    function obtenerNotificaciones() {
        fetch('/notificaciones')
            .then(response => response.json())
            .then(data => {
                mostrarNotificaciones(data.notificaciones);
            })
            .catch(error => {
                console.error('Error al obtener las notificaciones:', error);
            });
    }

    // Llamar a la función para obtener y mostrar las notificaciones
    obtenerNotificaciones();

