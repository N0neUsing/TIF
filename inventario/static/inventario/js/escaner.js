let contextoEscaner = 'agregarProducto'; // Contexto predeterminado

function onScanSuccess(decodedText, decodedResult) {
    console.log(`Código escaneado = ${decodedText}`, decodedResult);

    if (contextoEscaner === 'agregarProducto') {
        // Actualiza el campo del formulario en agregarProducto.html
        document.getElementById('codigoBarra').value = decodedText;
    } else if (contextoEscaner === 'agregarCarrito') {
        // Agrega el producto al carrito en carrito.html
        agregarProductoAlCarrito(decodedText);
    }
    
    // Cerrar el modal y luego detener el escáner
    setTimeout(() => {
        $('#modalScanner').modal('hide');
        $('.modal-backdrop').remove();
        $('body').removeClass('modal-open');
        stopQRScanner();
    }, 1000);
}

function cambiarContextoEscaner(nuevoContexto) {
    contextoEscaner = nuevoContexto;
}

// Configura el lector de QR utilizando Html5QrcodeScanner
function startQRScanner() {
    html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: 250 });
    html5QrcodeScanner.render(onScanSuccess, onScanFailure);
}

// Función para manejar los errores de escaneo
function onScanFailure(error) {
    if (!error.includes("No MultiFormat Readers were able to detect the code")) {
        console.warn(`Error de escaneo = ${error}`);
    }
}

// Vincular el botón para iniciar el escaneo en agregarProducto.html
if (document.getElementById('btn-scan-qr')) {
    document.getElementById('btn-scan-qr').addEventListener('click', function() {
        cambiarContextoEscaner('agregarProducto');
        startQRScanner();
    });
}

// Vincular el botón para iniciar el escaneo en carrito.html
if (document.getElementById('startScanButton')) {
    document.getElementById('startScanButton').addEventListener('click', function() {
        cambiarContextoEscaner('agregarCarrito');
        startQRScanner();
    });
}

// Función para detener el escáner, si es necesario
function stopQRScanner() {
    if (html5QrcodeScanner) {
        html5QrcodeScanner.clear();
    }
}
