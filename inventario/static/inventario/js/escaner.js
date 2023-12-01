function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let contextoEscaner = 'agregarProducto'; 
let html5QrcodeScanner;
let ultimoEscaneo = 0; 
const INTERVALO_ESCANEO = 3000; 

function onScanSuccess(decodedText, decodedResult) {
    const tiempoActual = new Date().getTime();
    if (tiempoActual - ultimoEscaneo < INTERVALO_ESCANEO) {
        console.log("Escaneo ignorado: Escaneo demasiado rápido");
        return;
    }
    ultimoEscaneo = tiempoActual;
    
    if (contextoEscaner === 'agregarProducto') {
        document.getElementById('codigoBarra').value = decodedText;
    } else if (contextoEscaner === 'agregarCarrito') {
        agregarProductoAlCarrito(decodedText);
    }

    cerrarModalYDetenerEscaner();
}

function cerrarModalYDetenerEscaner() {
    setTimeout(() => {
        $('#modalScanner').modal('hide');
        $('.modal-backdrop').remove();
        $('body').removeClass('modal-open');
        if (html5QrcodeScanner) {
            html5QrcodeScanner.clear(); 
        }
    }, 1000);
}

function cambiarContextoEscaner(nuevoContexto) {
    contextoEscaner = nuevoContexto;
}

function iniciarEscaner(contexto) {
    let qrReaderId = contexto === 'agregarProducto' ? 'qr-reader' : 'qr-reader-carrito';
    if (html5QrcodeScanner) {
        html5QrcodeScanner.clear(); 
    }
    html5QrcodeScanner = new Html5QrcodeScanner(qrReaderId, { fps: 10, qrbox: 250 });
    html5QrcodeScanner.render(onScanSuccess, onScanFailure);
}

function onScanFailure(error) {
    if (!error.includes("No MultiFormat Readers were able to detect the code")) {
        console.warn(`Error de escaneo = ${error}`);
    }
}

document.getElementById('btn-scan-qr')?.addEventListener('click', () => {
    cambiarContextoEscaner('agregarProducto');
    iniciarEscaner('agregarProducto');
});

document.getElementById('startScanButton')?.addEventListener('click', () => {
    console.log("Iniciando escáner en contexto 'agregarCarrito'");
    cambiarContextoEscaner('agregarCarrito');
    iniciarEscaner('agregarCarrito');
});

function agregarProductoAlCarrito(codigoBarra) {
    fetch('/inventario/agregar-producto-por-codigo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ codigoBarra: codigoBarra })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Producto agregado:', data);
            actualizarCarritoUI(data); // Asegúrate de pasar el objeto data completo
            // ...
        } else {
            console.error('Error al agregar producto:', data.message);
            mostrarErrorUI(data.message); // Mostrar el error en la interfaz
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        mostrarErrorUI(error); // Mostrar el error en la interfaz
    });
}

function actualizarCarritoUI(data) {
    // Verifica si se proporcionaron los datos del producto
    if (!data || !data.producto) {
        console.error("Datos del producto no proporcionados");
        return;
    }

    let producto = data.producto;
    // Encuentra el tbody donde se listan los productos
    let tbody = document.querySelector('.table tbody');

    // Crear una nueva fila para el producto
    let filaProducto = document.createElement('tr');
    filaProducto.innerHTML = `
        <td><img src="${producto.imagen}" alt="${producto.descripcion}" height="50"></td>
        <td>${producto.descripcion}</td>
        <td>
            <input type="number" name="quantity" value="1" min="1">
            <button type="button" class="btn btn-primary btn-update-cart" data-product-id="${producto.id}">Actualizar</button>
        </td>
        <td class="product-price">${producto.precio}</td>
        <td class="subtotal-cell">${producto.precio}</td>
        <td>
            <a href="#" class="btn btn-danger remove-from-cart">Eliminar</a>
        </td>
    `;

    // Añadir la fila al tbody
    tbody.appendChild(filaProducto);
}


function mostrarErrorUI(mensaje) {
    let mensajesDiv = document.querySelector('.messages');
    if (!mensajesDiv) {
        mensajesDiv = document.createElement('div');
        mensajesDiv.classList.add('messages');
        let contentSection = document.querySelector('.content');
        contentSection.prepend(mensajesDiv);
    }
    let errorMensaje = document.createElement('div');
    errorMensaje.className = 'error';
    errorMensaje.textContent = mensaje;
    mensajesDiv.appendChild(errorMensaje);
}