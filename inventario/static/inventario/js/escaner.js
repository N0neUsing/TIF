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
    
    cerrarModalYDetenerEscaner();
    if (contextoEscaner === 'agregarCarrito') {
        agregarProductoAlCarrito(decodedText, true);
    } else {
        mostrarModalConDatos(decodedText);
    }
}

function mostrarModalConDatos(codigoBarra) {
    fetchProductoPorCodigo(codigoBarra)
        .then(producto => {
            const detalles = `
                <h5>${producto.descripcion}</h5>
                <p>Precio: ${producto.precio}</p>
                <p>Tipo: ${producto.tipo}</p>
                <p>Cantidad Disponible: ${producto.disponible}</p>
                <p>Fecha de Vencimiento: ${producto.fecha_vencimiento}</p>
                <img src="${producto.imagen}" alt="Imagen del producto" height="100">
            `;
            document.getElementById('escaner-qr-detalles').innerHTML = detalles;
            $('#scanModalCarrito').modal('show');
        })
        .catch(error => {
            console.error('Error al obtener datos del producto:', error);
            mostrarModalProductoNoEncontrado(codigoBarra);
        });
}

function mostrarModalProductoNoEncontrado(codigoBarra) {
    const contenido = `
        <p>Producto con código ${codigoBarra} no encontrado.</p>
        <button onclick="reiniciarEscaneo()" class="btn btn-secondary">Intentar de nuevo</button>
        <button onclick="window.location.href='/inventario/agregarProducto'" class="btn btn-success">Agregar Producto</button>
    `;
    document.getElementById('escaner-qr-detalles').innerHTML = contenido;
    $('#scanModalCarrito').modal('show');
}

function mostrarErrorCarrito(mensaje, codigoBarra) {
    const contenido = `
        <div class="alert alert-danger" role="alert">${mensaje}</div>
        <p>Código del producto: ${codigoBarra}</p>
        <button onclick="$('#scanModalCarrito').modal('hide');" class="btn btn-secondary">Cerrar</button>
        <button onclick="reiniciarEscaneo();" class="btn btn-primary">Intentar de nuevo</button>
    `;
    document.getElementById('escaner-qr-detalles').innerHTML = contenido;
    $('#scanModalCarrito').modal('show');
}

function fetchProductoPorCodigo(codigoBarra) {
    return fetch(`/inventario/api/producto/${codigoBarra}`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.producto) {
                return data.producto;
            } else {
                throw new Error('Producto no encontrado');
            }
        });
}

function reiniciarEscaneo() {
    cerrarModalYDetenerEscaner();

    setTimeout(() => {
        iniciarEscaner(contextoEscaner);
        $('#scanModalCarrito').modal('show');
    }, 1500);
}

function cerrarModalYDetenerEscaner() {
    $('#scanModalCarrito').on('hidden.bs.modal', function () {
        if (html5QrcodeScanner) {
            html5QrcodeScanner.clear();
        }
    }).modal('hide');
}

function cambiarContextoEscaner(nuevoContexto) {
    contextoEscaner = nuevoContexto;
}

function iniciarEscaner(contexto) {
    let qrReaderId;
    if (contexto === 'agregarProducto') {
        qrReaderId = 'qr-reader';
    } else if (contexto === 'agregarCarrito') {
        qrReaderId = 'qr-reader-carrito';
    } else if (contexto === 'buscarProducto') {
        qrReaderId = 'qr-reader-listar';
    } else {
        console.error('Contexto del escáner no definido:', contexto);
        return;
    }

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

function agregarProductoAlCarrito(codigoBarra, actualizarUI) {
    fetch('/inventario/agregar-producto-por-codigo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ codigoBarra: codigoBarra })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Error desconocido al agregar al carrito.');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (actualizarUI) {
                fetchCartAndUpdateUI(); // Actualiza la interfaz de usuario del carrito
            }
            mostrarDetallesProductoCarrito(data.producto);
        } else {
            throw new Error(data.message || 'Error al procesar el producto.');
        }
    })
    .catch(error => {
        console.error('Error al agregar producto al carrito:', error.message);
        mostrarErrorCarrito(error.message, codigoBarra);
    });
}

function mostrarDetallesProductoCarrito(producto) {
    const detalles = `
        <h5>${producto.descripcion}</h5>
        <p>Precio: ${producto.precio}</p>
        <p>Tipo: ${producto.tipo}</p>
        <p>Cantidad Disponible: ${producto.disponible}</p>
        <p>Fecha de Vencimiento: ${producto.fecha_vencimiento}</p>
        <img src="${producto.imagen}" alt="Imagen del producto" height="100">
    `;
    document.getElementById('escaner-qr-detalles').innerHTML = detalles;
    $('#scanModalCarrito').modal('show');
}

function actualizarCarritoUI(producto, detallesID) {
    if (!producto) {
        console.error("Datos del producto no proporcionados");
        mostrarErrorUI("Datos del producto no proporcionados", detallesID);
        return;
    }

    const detalles = `
        <h5>${producto.descripcion}</h5>
        <p>Precio: ${producto.precio}</p>
        <p>Tipo: ${producto.tipo}</p>
        <p>Cantidad Disponible: ${producto.disponible}</p>
        <p>Fecha de Vencimiento: ${producto.fecha_vencimiento}</p>
        <img src="${producto.imagen}" alt="Imagen del producto" height="100">
    `;
    document.getElementById(detallesID).innerHTML = detalles;
    $('#btnAgregarAlCarrito').show();
    $('#btnEditarProducto').show();
    $('#btnBuscarPrecio').show();
    $('#btnAgregarProducto').hide();  // Esconder el botón de agregar si el producto existe
    $('#modalScanner').modal('show');
}

function attachModalButtonEvents() {
    const btnAgregarAlCarrito = document.getElementById('btnAgregarAlCarrito');
    if (btnAgregarAlCarrito) {
        btnAgregarAlCarrito.onclick = function() {
            const codigoBarra = document.getElementById('codigoBarra').value;
            agregarProductoAlCarrito(codigoBarra);
        };
    }

    const btnEditarProducto = document.getElementById('btnEditarProducto');
    btnEditarProducto.onclick = function() {
        const productId = this.getAttribute('data-id');
        if (productId) {
            window.location.href = `/inventario/editarProducto/${productId}/`;
        } else {
            console.error("ID del producto no definido en el botón editar.");
        }
    };

    const btnAgregarProducto = document.getElementById('btnAgregarProducto');
    if (btnAgregarProducto) {
        btnAgregarProducto.onclick = function() {
            window.location.href = '/inventario/agregarProducto';
        };
    }
}

function mostrarErrorUI(mensaje, detallesID) {
    const contenido = `<div class="alert alert-danger">${mensaje}</div>`;
    document.getElementById(detallesID).innerHTML = contenido;
    $('#btnAgregarAlCarrito').hide();
    $('#btnEditarProducto').hide();
    $('#btnBuscarPrecio').hide();
    $('#btnAgregarProducto').show(); // Mostrar solo el botón de agregar si el producto no existe
    $(`#modalScanner`).modal('show');
}

$('#scanModalListar').on('shown.bs.modal', function () {
    attachModalButtonEvents();
});

$(document).ready(function() {
    $('#scanNextButton').click(function() {
        reiniciarEscaneo();
    });

    $('.close').click(function() {
        $('#scanModalCarrito').modal('hide');
    });
});

document.getElementById('btn-scan-product-list').addEventListener('click', function() {
    console.log("Iniciando escáner en contexto 'buscarProducto'");
    cambiarContextoEscaner('buscarProducto');
    iniciarEscaner('buscarProducto');
});

document.getElementById('scanNextButton').addEventListener('click', function() {
    reiniciarEscaneo();
});

document.getElementById('btnRetryScan').addEventListener('click', function() {
    reiniciarEscaneo();
});

$('.close').click(function() {
    $('#scanModalCarrito').modal('hide');
});

$('#scanModalListar').on('hidden.bs.modal', function () {
    document.getElementById('escaner-qr-detalles-listar').innerHTML = '';
    document.getElementById('btnAgregarAlCarrito').style.display = 'none';
    document.getElementById('btnEditarProducto').style.display = 'none';
    document.getElementById('btnAgregarProducto').style.display = 'block';
    const codigoBarraInput = document.getElementById('codigoBarra');
    if (codigoBarraInput) {
        codigoBarraInput.value = '';
    }
});
