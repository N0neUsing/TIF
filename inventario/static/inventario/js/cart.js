
console.log("cart.js cargado.");
const BASE_URL = 'https://sistema-delvalle-noneuser.loca.lt';
//const BASE_URL = 'http://localhost:8000';
const MEDIA_URL = '/media/';


document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM completamente cargado y analizado.");
    fetchCartAndUpdateUI();
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            let productId = button.dataset.productId;
            addToCart(productId);
        });
    });

document.querySelectorAll('.btn-update-cart').forEach(button => {
    button.addEventListener('click', event => {
        const productId = button.getAttribute('data-product-id');
        const quantityInput = document.querySelector(`#product-row-${productId} input[name='quantity']`);
        const desiredPriceInput = document.querySelector(`#product-row-${productId} input[name='desired-price']`);

        let quantity;
        if (desiredPriceInput && desiredPriceInput.value) {
            const pricePerGram = parseFloat(desiredPriceInput.dataset.pricePerGram); // Asegúrate de que este dato está disponible
            const desiredPrice = parseFloat(desiredPriceInput.value);
            quantity = desiredPrice / pricePerGram; // Calcular la cantidad basada en el precio deseado
            quantityInput.value = quantity.toFixed(2); // Actualizar visualmente el campo de cantidad
        } else if (quantityInput) {
            quantity = parseFloat(quantityInput.value);
        }

        if (quantity && !isNaN(quantity)) {
            actualizarCarrito(productId, quantity);
        } else {
            console.error("La cantidad no es un número válido", quantity);
        }
    });
});
    

document.addEventListener('click', function(event) {
    if (event.target.matches('.btn-update-cart')) {
        updateCartEventListener(event);
    } else if (event.target.matches('.remove-from-cart')) {
        removeFromCartEventListener(event);
    }
});

document.querySelectorAll('.expand-on-hover').forEach(img => {
    img.addEventListener('mouseover', () => {
        // Implementación simplificada sin necesidad de manejar el timer externamente
        img.classList.add('hovered');
    });

    img.addEventListener('mouseout', () => {
        img.classList.remove('hovered');
    });
});
});

function actualizarTotalCarrito() {
    let total = 0;
    document.querySelectorAll('.subtotal-cell').forEach(cell => {
        const subtotal = parseFloat(cell.textContent.replace('$', ''));
        if (!isNaN(subtotal)) {
            total += subtotal;
        }
    });
    console.log("Total calculado:", total);
    const totalCarritoEl = document.querySelector('.total-carrito');
    if(totalCarritoEl) {
        totalCarritoEl.textContent = `$${total.toFixed(2)}`;
    } else {
        console.log('Elemento total-carrito no encontrado');
    }

    // Asegúrate de que el botón de finalizar compra siempre esté habilitado
    const finalizePurchaseButton = document.getElementById('finalize-purchase-button');
    if (finalizePurchaseButton) {
        finalizePurchaseButton.removeAttribute('disabled');
    } else {
        console.log('Elemento finalize-purchase-button no encontrado');
    }
}



function addToCart(productId) {
    fetch(`/inventario/agregar-a-carrito/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            if (data.errorCode === 'NOT_FOUND') {
                showAlert(`Producto no encontrado (ID: ${productId})`, 'error');
            } else if (data.errorCode === 'NO_PRICE') {
                showAlert(`Producto sin precio (ID: ${productId})`, 'error');
            } else {
                showAlert(data.message, 'error');
            }
        } else {
            showAlert(data.message, 'success');
            fetchCartAndUpdateUI();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error al agregar al carrito', 'error');
    });
}

function actualizarCarrito(productId, quantityInputValue, desiredPriceInputValue) {
    const { unitId, pricePerUnit } = getUnitAndPrice(productId);

    let quantityToSend = parseFloat(quantityInputValue);
    const desiredPrice = parseFloat(desiredPriceInputValue);

    if (!unitId || isNaN(pricePerUnit)) {
        console.error("Información de unidad o precio por unidad inválida");
        showAlert('Error: Información de unidad o precio por unidad inválida', 'error');
        return;
    }

    switch (unitId) {
        case '3': // Kilogramos
            if (desiredPriceInputValue !== undefined && desiredPrice > 0) {
                quantityToSend = desiredPrice / (pricePerUnit * 1000);
            }
            break;
        case '2': // Gramos
            if (desiredPriceInputValue !== undefined && desiredPrice > 0) {
                quantityToSend = desiredPrice / pricePerUnit;
            }
            break;
        default:
            break;
    }

    console.log(`Actualizando carrito para el producto ID ${productId} con cantidad ${quantityToSend} (ID de unidad: ${unitId})`);

    fetch(`${BASE_URL}/inventario/actualizar-item-carrito/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: quantityToSend, unit_id: unitId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector(`#product-row-${productId} .subtotal-cell`).textContent = `$${data.new_subtotal.toFixed(2)}`;
            actualizarTotalCarritoConImpuestos();  // Esta función debería solicitar el total actualizado con impuestos del servidor
            showAlert('Cantidad actualizada correctamente', 'success');
        } else {
            showAlert(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error al actualizar la cantidad en el carrito:', error);
        showAlert('Error al actualizar la cantidad en el carrito', 'error');
    });
}

function actualizarTotalCarritoConImpuestos() {
    fetch(`${BASE_URL}/inventario/api/total-con-impuestos/`) // Asegúrate de tener esta ruta implementada en Django
    .then(response => response.json())
    .then(data => {
        const totalCarritoEl = document.querySelector('.total-carrito');
        if (totalCarritoEl) {
            totalCarritoEl.textContent = `$${data.total_con_impuestos.toFixed(2)}`;
        } else {
            console.log('Elemento total-carrito no encontrado');
        }
    })
    .catch(error => {
        console.error('Error al obtener el total del carrito con impuestos:', error);
    });
}


function fetchCartAndUpdateUI() {
    console.log("Actualizando el carrito UI...");
    fetch('/inventario/api/cart/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Respuesta de la API:", data);
        const cartItemsContainer = document.querySelector('#cart-items-container');

        // Verifica si el contenedor del carrito existe
        if (!cartItemsContainer) {
            console.error("El contenedor de ítems del carrito no se encontró.");
            return; // Detén la ejecución si el contenedor no existe
        }

        // Verifica si se recibieron productos en la respuesta
        if (!data || data.length === 0 || !data[0].items || data[0].items.length === 0) {
            console.error('No se encontraron elementos en la respuesta de la API:', data);
            cartItemsContainer.innerHTML = '<tr><td colspan="6">No hay productos en el carrito.</td></tr>';
        } else {
            console.log("Se encontraron elementos en el carrito:", data[0].items);
            // Limpia el contenedor antes de añadir nuevos productos
            cartItemsContainer.innerHTML = '';
            data[0].items.forEach(item => {
                renderCartItem(item); // Asegúrate de que esta función añade correctamente cada producto al DOM
            });
            attachEventListenersToButtons(); // Re-attach event listeners to newly added buttons
        }

        // Llama a actualizarTotalCarrito() después de manejar la visibilidad del pie del carrito
        actualizarTotalCarrito();
    })
    .catch(error => {
        console.error('Error al actualizar el carrito:', error);
    });
}

function updateCartItemsUI(data, container) {
    container.innerHTML = data.length === 0 ? '<tr><td colspan="6">No hay productos en el carrito.</td></tr>' : '';
    data.forEach(item => container.insertAdjacentHTML('beforeend', renderCartItem(item)));
}


function getUnitAndPrice(productId) {
    // Simulación de un mapa de unidades y precios por producto
    const productUnitPriceMap = {
        '1': { unitId: '1', pricePerUnit: 6500 }, // Ejemplo: '1' para piezas
        '2': { unitId: '3', pricePerUnit: 6500 / 1000 }, // Ejemplo: '3' para kilogramos, precio por gramo
        // ... otros productos
    };

    // Obtener la información de la unidad y el precio por unidad para el productId dado
    const productInfo = productUnitPriceMap[productId];

    // Si no se encuentra la información del producto, devolver valores por defecto o manejar el error adecuadamente
    if (!productInfo) {
        console.error(`Información no encontrada para el producto con ID ${productId}`);
        return { unitId: '1', pricePerUnit: 0 }; // Valores por defecto o lanzar un error
    }

    return productInfo;
}


function renderCartItem(item) {
    const cartItemsContainer = document.querySelector('#cart-items-container');
    const imagePath = item.product.imagen_producto_url ? item.product.imagen_producto_url : `${BASE_URL}/path/to/default/image.png`;
    
    // Maneja el caso cuando el producto no tiene precio asignado
    let priceContent, pricePerGram, pricePerKilogram;
    if (item.product.precio) {
        pricePerGram = parseFloat(item.product.precio);
        pricePerKilogram = pricePerGram * 1000;
        priceContent = `$${pricePerGram.toFixed(2)}`;
        if (['Gramos', 'Kilo', 'Litro', 'Otro'].includes(item.product.tipo_nombre)) {
            priceContent = `$${pricePerGram.toFixed(2)} por g // $${pricePerKilogram.toFixed(2)} por kg`;
        }
    } else {
        priceContent = 'Precio no disponible';
    }

    let subtotalContent = item.product.precio ? `$${(item.quantity * pricePerGram).toFixed(2)}` : 'N/A';
    let quantityInput = `<input type="number" name="quantity" value="${item.quantity}" min="1" class="quantity-input" data-product-id="${item.product.id}">`;
    let desiredPriceInput = '';
    let addPriceButton = '';

    if (item.product.tipo_nombre !== 'Unidad') {
        desiredPriceInput = `
            <input type="number" name="desired-price" class="desired-price-input" data-product-id="${item.product.id}" placeholder="Precio deseado" min="0.01" step="0.01" onchange="updateQuantityAndSubtotalBasedOnDesiredPrice(this)">
            <input type="number" name="desired-grams" class="desired-grams-input" data-product-id="${item.product.id}" placeholder="Gramos deseados" min="1" step="1" onchange="updatePriceAndSubtotalBasedOnDesiredGrams(this)">
        `;
    }

    if (!item.product.precio) {
        addPriceButton = `<button type="button" class="btn btn-warning btn-add-price" data-product-id="${item.product.id}">Agregar Precio</button>`;
    }

    const itemHTML = `
        <tr id="product-row-${item.product.id}">
            <td><img src="${imagePath}" alt="${item.product.descripcion}" height="50"></td>
            <td>${item.product.descripcion}</td>
            <td>
                ${quantityInput}
                ${desiredPriceInput}
                ${addPriceButton}
                <button type="button" class="btn btn-primary btn-update-cart" data-product-id="${item.product.id}">Actualizar</button>
            </td>
            <td class="product-price">${priceContent}</td>
            <td class="subtotal-cell">${subtotalContent}</td>
            <td>
                <button type="button" class="btn btn-danger remove-from-cart" data-product-id="${item.product.id}">Eliminar</button>
            </td>
        </tr>
    `;

    cartItemsContainer.insertAdjacentHTML('beforeend', itemHTML);
    
    // Evento para el botón de agregar precio, si es necesario
    if(item.product.precio === null) {
        // Añadir evento para mostrar el modal con el ID priceModal
        cartItemsContainer.querySelector(`.btn-add-price[data-product-id="${item.product.id}"]`).addEventListener('click', () => {
            const saveButton = document.getElementById('save-price-button');
            // Establecer el ID del producto en el botón del modal para saber qué producto se está actualizando
            saveButton.dataset.productId = item.product.id;
            // Limpiar valor anterior y mostrar el modal
            document.getElementById('modal-product-price').value = '';
            $('#priceModal').modal('show');
        });
    }
}

document.addEventListener('input', function(event) {
    if (event.target.matches('.desired-price-input')) {
        const productId = event.target.dataset.productId;
        const grams = parseFloat(event.target.value);
        const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.slice(1)) / 1000; // Suponiendo que el precio es por kilogramo
        const newSubtotal = grams * pricePerGram;
        document.querySelector(`#product-row-${productId} .subtotal-cell`).textContent = `$${newSubtotal.toFixed(2)}`;
    }
});

// Función para actualizar el precio basado en la cantidad de gramos ingresada
function updatePriceBasedOnGrams(inputElement) {
    const grams = parseFloat(inputElement.value);
    const productId = inputElement.dataset.productId;
    const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.slice(1)) / 1000;
    const newPrice = grams * pricePerGram;
    document.querySelector(`#product-row-${productId} .desired-price-input`).value = newPrice.toFixed(2);
}

// Función para actualizar el subtotal y la cantidad basado en el precio deseado ingresado
function updateQuantityAndSubtotalBasedOnDesiredPrice(inputElement) {
    const productId = inputElement.dataset.productId;
    const desiredPrice = parseFloat(inputElement.value);
    const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.split(' ')[0].slice(1));
    const grams = desiredPrice / pricePerGram;
    const quantityInput = document.querySelector(`#product-row-${productId} .quantity-input`);
    const subtotalCell = document.querySelector(`#product-row-${productId} .subtotal-cell`);

    quantityInput.value = grams.toFixed(2);
    subtotalCell.textContent = `$${desiredPrice.toFixed(2)}`;
}

// Función para actualizar el subtotal y el precio deseado basado en los gramos deseados ingresados
function updatePriceAndSubtotalBasedOnDesiredGrams(inputElement) {
    const productId = inputElement.dataset.productId;
    const desiredGrams = parseFloat(inputElement.value);
    const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.split(' ')[0].slice(1));
    const desiredPrice = desiredGrams * pricePerGram;
    const desiredPriceInput = document.querySelector(`#product-row-${productId} .desired-price-input`);
    const subtotalCell = document.querySelector(`#product-row-${productId} .subtotal-cell`);

    desiredPriceInput.value = desiredPrice.toFixed(2);
    subtotalCell.textContent = `$${(desiredGrams * pricePerGram).toFixed(2)}`;
}


// Función para actualizar la cantidad de gramos basada en el precio deseado
function updateQuantityBasedOnPrice(inputElement) {
    const desiredPrice = parseFloat(inputElement.value);
    const productId = inputElement.dataset.productId;
    const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.slice(1)) / 1000;
    const newGrams = desiredPrice / pricePerGram;
    document.querySelector(`#product-row-${productId} .desired-grams-input`).value = newGrams.toFixed(2);
}

document.getElementById('save-price-button').addEventListener('click', () => {
    const productId = document.getElementById('save-price-button').getAttribute('data-product-id');
    const newPrice = parseFloat(document.getElementById('modal-product-price').value);
    console.log(`Intentando actualizar el precio para el producto ID ${productId} con nuevo precio: ${newPrice}`);
    if (!isNaN(newPrice) && newPrice > 0) {
        actualizarPrecio(productId, newPrice);
        $('#priceModal').modal('hide');
    } else {
        console.error("Precio introducido no válido:", newPrice);
        alert("Por favor, introduce un precio válido.");
    }
});

function attachEventListenersToButtons() {
    document.querySelectorAll('.btn-update-cart').forEach(button => {
        button.removeEventListener('click', updateCartEventListener);
        button.addEventListener('click', updateCartEventListener);
    });

    document.querySelectorAll('.remove-from-cart').forEach(button => {
        button.removeEventListener('click', removeFromCartEventListener);
        button.addEventListener('click', removeFromCartEventListener);
    });

    document.querySelectorAll('.desired-price').forEach(input => {
        input.removeEventListener('input', handleDesiredPriceInput);
        input.addEventListener('input', handleDesiredPriceInput);
    });
    document.querySelectorAll('.btn-add-price').forEach(button => {
        button.addEventListener('click', event => {
            const productId = button.dataset.productId;
            document.getElementById('save-price-button').dataset.productId = productId; // Asegúrate de actualizar el productId aquí para que esté disponible cuando se envíe el formulario
            $('#priceModal').modal('show');
        });
    });
}

function handleDesiredPriceInput(event) {
    const input = event.target;
    const productId = input.dataset.productId;
    const unitId = input.dataset.unitId;  // Asegúrate de que esto se define en el backend y se pasa correctamente
    const pricePerUnit = parseFloat(input.dataset.pricePerUnit);  // Asumiendo que esto es el precio por gramo si es aplicable
    const desiredPrice = parseFloat(input.value);

    let quantity;
    if (unitId === '3') {  // Suponiendo '3' para kilogramos
        quantity = (desiredPrice / pricePerUnit) * 1000;  // Convierte el precio deseado en kilogramos a la cantidad en gramos
    } else if (unitId === '2') {  // '2' para gramos
        quantity = desiredPrice / pricePerUnit;  // Calcula la cantidad directamente en gramos
    } else {
        console.error("Unidad no manejada:", unitId);
        return;  // Detener si la unidad no es manejable
    }

    const quantityInput = document.querySelector(`#product-row-${productId} .quantity-input`);
    quantityInput.value = quantity.toFixed(2);  // Actualiza el input de cantidad

    actualizarCarrito(productId, quantity.toFixed(2), desiredPrice);  // Asegúrate de que esta función maneje los parámetros correctamente
}




function updateCartEventListener(event) {
    const button = event.target;
    const productId = button.dataset.productId;
    const quantityInput = document.querySelector(`#product-row-${productId} input[name='quantity']`);
    const desiredPriceInput = document.querySelector(`#product-row-${productId} input[name='desired-price']`);

    let quantity = parseFloat(quantityInput.value);
    let desiredPrice = parseFloat(desiredPriceInput ? desiredPriceInput.value : 0);

    if (quantity && !isNaN(quantity)) {
        actualizarCarrito(productId, quantity, desiredPrice);
    } else {
        console.error("La cantidad no es un número válido", quantity);
        showAlert('La cantidad debe ser un número válido.', 'error');
    }
}


function removeFromCartEventListener(event) {
    const button = event.target;
    const productId = button.dataset.productId;
    fetch(`${BASE_URL}/inventario/eliminar-de-carrito/${productId}/`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Producto eliminado del carrito', 'success');
                fetchCartAndUpdateUI(); // Refresca los ítems del carrito y el total
            } else {
                showAlert('Error al eliminar del carrito', 'error');
            }
        })
        .catch(error => {
            console.error('Error al eliminar del carrito:', error);
            showAlert('Error al eliminar del carrito', 'error');
        });
}


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

function showAlert(message, type) {
    let alertBox = document.createElement('div');
    alertBox.textContent = message;
    alertBox.className = `alert ${type === 'success' ? 'alert-success' : 'alert-danger'}`;
    alertBox.style.position = 'fixed';
    alertBox.style.top = '20px';
    alertBox.style.right = '20px';
    alertBox.style.zIndex = '1000';
    document.body.appendChild(alertBox);
    setTimeout(() => {
        alertBox.remove();
    }, 3000);
}

document.querySelectorAll('.remove-from-cart').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        const productId = button.getAttribute('data-product-id');
        fetch(`${BASE_URL}/inventario/eliminar-de-carrito/${productId}/`, { method: 'GET' })
            .then(response => {
                if (response.ok) {
                    showAlert('Producto eliminado del carrito', 'success');
                    fetchCartAndUpdateUI(); // Refresca los ítems del carrito y el total
                } else {
                    throw new Error('La respuesta de la red no fue ok.');
                }
            })
            .catch(error => {
                console.error('Error al eliminar del carrito:', error);
                showAlert('Error al eliminar del carrito', 'error');
            });
    });
});

document.querySelectorAll('.btn-add-price').forEach(button => {
    button.addEventListener('click', event => {
        const productId = button.dataset.productId;
        $('#priceModal').modal('show');
        $('#updatePriceForm').on('submit', function(e) {
            e.preventDefault();
            const productId = document.getElementById('save-price-button').dataset.productId; // Asegúrate de que este ID se actualiza correctamente en otro lugar
            const newPrice = parseFloat(document.getElementById('product-price').value);
            if (!isNaN(newPrice) && newPrice > 0) {
                actualizarPrecio(productId, newPrice);
                $('#priceModal').modal('hide');
            } else {
                alert("Por favor, introduce un precio válido.");
            }
        });
    });
});

function actualizarPrecio(productId, precio) {
    const url = `${BASE_URL}/inventario/actualizar-precio/${productId}/`;
    console.log("URL a la que se está llamando:", url);
    const data = { precio: precio };
    console.log("Enviando datos al servidor:", data);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP status ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            document.querySelector(`#product-row-${productId} .product-price`).textContent = `$${precio.toFixed(2)}`;
            fetchCartAndUpdateUI();
            showAlert('Precio actualizado correctamente', 'success');
        } else {
            showAlert(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error al actualizar el precio:', error);
        showAlert('Error al actualizar el precio', 'error');
    });
}

document.addEventListener('input', function (event) {
    if (event.target.matches('.desired-price')) {
        var productId = event.target.dataset.productId;
        var unitId = event.target.dataset.unitId; // Suponiendo que tienes un data attribute para el ID de la unidad
        var priceInput = parseFloat(event.target.value);
        var pricePerUnit = parseFloat(event.target.dataset.pricePerUnit); // Este debe ser el precio por la unidad base

        // Calcula la cantidad necesaria en base a la unidad base
        var quantity = priceInput / pricePerUnit;

        // Actualiza el input de cantidad y llama a actualizarCarrito con la cantidad y el ID de la unidad
        var quantityInput = document.querySelector(`#product-row-${productId} .quantity-input`);
        quantityInput.value = quantity.toFixed(2); // Muestra la cantidad en la unidad base
        actualizarCarrito(productId, quantity, unitId);
    }
}, false);

document.addEventListener('DOMContentLoaded', function() {
    attachEventListenersToButtons();
});