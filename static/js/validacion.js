function validarCedula() {
    var cedula = document.getElementById('id').value;

    // Validar longitud de la cédula
    if (cedula.length !== 10) {
      alert('La cédula debe tener 10 dígitos.');
      return false;
    }

    // Validar que todos los caracteres sean dígitos
    if (!/^\d+$/.test(cedula)) {
      alert('La cédula solo debe contener dígitos.');
      return false;
    }

    // Validar el dígito verificador
    var provincia = parseInt(cedula.substring(0, 2));
    if (provincia < 1 || provincia > 24) {
      alert('El código de provincia no es válido.');
      return false;
    }

    var digitoVerificador = parseInt(cedula.substring(9, 10));
    var coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2];
    var suma = 0;

    for (var i = 0; i < coeficientes.length; i++) {
      var producto = parseInt(cedula.charAt(i)) * coeficientes[i];
      suma += producto >= 10 ? producto - 9 : producto;
    }

    var resultado = suma % 10 === 0 ? 0 : 10 - (suma % 10);

    if (digitoVerificador !== resultado) {
      alert('La cédula no es válida.');
      return false;
    }

    alert('La cédula es válida.');
    return true;
  }