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
        agregarProductoAlCarrito(decodedText,true);
    } else if (contextoEscaner === 'buscarProducto') {
        fetchProductoPorCodigo(decodedText);
        var table = $('#example2').DataTable();
        table.search(decodedText).draw(); // Filtra la tabla por el código de barras escaneado
    }


    cerrarModalYDetenerEscaner();
}

function mostrarDetallesProducto(producto) {
    const detalles = `
        <h5>${producto.descripcion}</h5>
        <p>Precio: ${producto.precio}</p>
        <p>Tipo: ${producto.tipo}</p>
        <p>Cantidad Disponible: ${producto.disponible}</p>
        <p>Fecha de Vencimiento: ${producto.fecha_vencimiento}</p>
        <img src="${producto.imagen}" alt="Imagen del producto" height="100">
    `;
    document.getElementById('escaner-qr-detalles-listar').innerHTML = detalles;
    const btnEditarProducto = document.getElementById('btnEditarProducto');
    document.getElementById('btnAgregarAlCarrito').setAttribute('data-product-id', producto.id);
    if (producto.id) {
        btnEditarProducto.setAttribute('data-id', producto.id);
        btnEditarProducto.style.display = 'block';
    } else {
        btnEditarProducto.style.display = 'none';
        console.error('ID del producto no definido');
    }
}

function mostrarDetallesProductoCarrito(producto) {
    console.log("Intentando mostrar los detalles del producto:", producto);

    const detallesProducto = document.getElementById('escaner-qr-detalles');
    if (!detallesProducto) {
        console.error("No se encontró el elemento para mostrar los detalles del producto.");
        return;
    }

    console.log("Actualizando el innerHTML del elemento de detalles del producto");
    detallesProducto.innerHTML = `
        <div>
            <h5>${producto.descripcion}</h5>
            <p>Precio: ${producto.precio}</p>
            <img src="${producto.imagen}" alt="${producto.descripcion}" class="img-fluid">
        </div>
    `;

    console.log("El contenido del modal debe estar actualizado ahora");
    $('#scanModalCarrito').modal('show');
}


function mostrarModalProductoNoEncontrado(codigoBarra) {
    const contenido = `
        <p>Producto con código ${codigoBarra} no encontrado.</p>
        // Asegúrate de que los botones de acción llamen a las funciones correspondientes
    `;
    document.getElementById('escaner-qr-detalles-listar').innerHTML = contenido;
    // Restablece el estado de los botones si es necesario
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
    fetch(`/inventario/api/producto/${codigoBarra}`, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        console.log("Datos recibidos del servidor para el código de barra", codigoBarra, ":", data);
        if (data.success && data.producto) {
            // Decisiones basadas en el contexto del escáner
            switch (contextoEscaner) {
                case 'agregarCarrito':
                    mostrarDetallesProductoCarrito(data.producto);
                    $('#scanModalCarrito').modal('show'); // Asegurarse de mostrar el modal correcto para el carrito
                    break;
                case 'buscarProducto':
                    mostrarDetallesProducto(data.producto);
                    $('#scanModalListar').modal('show'); // Mostrar otro tipo de modal si el contexto es búsqueda
                    break;
                default:
                    mostrarDetallesProducto(data.producto); // Mostrar detalles del producto por defecto
                    $('#scanModal').modal('show'); // Asegurarse de mostrar el modal general
                    break;
            }
        } else {
            mostrarModalProductoNoEncontrado(codigoBarra);
            // Configuración de visibilidad de botones dependiendo del contexto
            document.getElementById('btnAgregarAlCarrito').style.display = (contextoEscaner === 'agregarCarrito') ? 'none' : 'block';
            document.getElementById('btnEditarProducto').style.display = 'none';
            document.getElementById('btnAgregarProducto').style.display = 'block';
            $('#scanModalListar').modal('show'); // Mostrar el modal de producto no encontrado
        }
    })
    .catch(error => {
        console.error('Error al obtener datos del producto:', error);
        mostrarModalProductoNoEncontrado(codigoBarra);
    });
}


function mostrarModalProductoEncontrado(producto, detallesID) {
    const detalles = `
        <h5>${producto.nombre}</h5>
        <p>${producto.descripcion}</p>
        <p>Precio: ${producto.precio}</p>
        <img src="${producto.imagen}" alt="Imagen del producto" height="100">
    `;
    document.getElementById('detallesID').innerHTML = detalles;
    $('#btnAgregarAlCarrito').show();
    $('#btnEditarProducto').show();
    $('#btnBuscarPrecio').show();
    $('#btnAgregarProducto').hide(); // Esconder el botón de agregar si el producto existe
    $('#scanModal').modal('show');
}

function mostrarModalProductoNoEncontrado(codigoBarra) {
    const contenido = `
        <p>Producto con código ${codigoBarra} no encontrado.</p>
        <button onclick="reiniciarEscaneo()" class="btn btn-secondary">Intentar de nuevo</button>
        <button onclick="window.location.href='/inventario/agregarProducto'" class="btn btn-success">Agregar Producto</button>
    `;
    document.getElementById('escaner-qr-detalles-listar').innerHTML = contenido;
    $('#btnAgregarAlCarrito').hide();
    $('#btnEditarProducto').hide();
    $('#btnAgregarProducto').hide(); // Esconder todos los botones, ya que no son relevantes en este contexto
}

function reiniciarEscaneo() {
    // Cierra el modal actualmente abierto y detiene el escáner de QR
    cerrarModalYDetenerEscaner();

    // Espera un corto tiempo antes de reiniciar el escáner para asegurar que se ha limpiado correctamente
    setTimeout(() => {
        iniciarEscaner(contextoEscaner); // Asegúrate de que 'contextoEscaner' es accesible globalmente o pasa como argumento
    }, 1500); // Ajusta este tiempo según sea necesario
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
    // Asegúrate de tener un 'qr-reader-listar' en tu HTML para listarProductos.html
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

    // Asigna el nuevo escáner al elemento con el ID correspondiente
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
    // Evento para el botón de escanear otro producto
    $('#scanNextButton').click(function() {
        $('#scanModalCarrito').modal('hide');
        cambiarContextoEscaner('agregarProducto');
        iniciarEscaner('agregarProducto');
    });

    // Evento para el botón de cerrar
    $('.close').click(function() {
        $('#scanModalCarrito').modal('hide');
    });
});

// Configuración inicial del escáner
document.getElementById('btn-scan-product-list').addEventListener('click', function() {
    console.log("Iniciando escáner en contexto 'buscarProducto'");
    cambiarContextoEscaner('buscarProducto');
    iniciarEscaner('buscarProducto');
});

// Botón para escanear otro producto
document.getElementById('scanNextButton').addEventListener('click', function() {
    $('#scanModalCarrito').modal('hide');  // Cierra el modal actual
    cambiarContextoEscaner('agregarProducto');  // Cambia el contexto de escaneo a agregar producto
    iniciarEscaner('agregarProducto');  // Reinicia el escáner
});

// Configuración del botón para agregar al carrito desde el modal de escaneo
document.getElementById('btnAgregarAlCarrito').addEventListener('click', function() {
    const productId = this.getAttribute('data-product-id');
    if (productId) {
        addToCart(productId);
    } else {
        console.error("No se pudo obtener el ID del producto para agregar al carrito.");
    }
});

document.getElementById('btnRetryScan').addEventListener('click', function() {
    reiniciarEscaneo();
});

$('.close').click(function() {
    $('#scanModalCarrito').modal('hide');  // Cierra el modal
    // Aquí puedes añadir cualquier otra lógica de limpieza si es necesario
});

$('#scanModalListar').on('hidden.bs.modal', function () {
    // Limpia los detalles del producto escaneado
    document.getElementById('escaner-qr-detalles-listar').innerHTML = '';
    // Restablece los botones a su estado original si es necesario
    document.getElementById('btnAgregarAlCarrito').style.display = 'none';
    document.getElementById('btnEditarProducto').style.display = 'none';
    document.getElementById('btnAgregarProducto').style.display = 'block';
    // Si tienes un elemento de input para el código de barras, también deberías limpiarlo
    const codigoBarraInput = document.getElementById('codigoBarra');
    if (codigoBarraInput) {
        codigoBarraInput.value = '';
    }
    // Reiniciar cualquier otra información relacionada o estados de interfaz aquí si es necesario
});