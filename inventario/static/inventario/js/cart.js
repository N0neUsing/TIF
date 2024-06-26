console.log("cart.js cargado.");
//const BASE_URL = 'https://sistema-delvalle-noneuser.loca.lt';
const BASE_URL = 'http://localhost:8000';
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
                const pricePerGram = parseFloat(desiredPriceInput.dataset.pricePerGram);
                const desiredPrice = parseFloat(desiredPriceInput.value);
                quantity = desiredPrice / pricePerGram;
                quantityInput.value = quantity.toFixed(2);
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

    document.querySelectorAll('input[name="quantity"]').forEach(input => {
        input.addEventListener('input', event => {
            const productId = event.target.closest('tr').id.split('-')[2];
            const quantity = parseFloat(event.target.value);
            updateSubtotal(productId, quantity);
            actualizarTotalCarrito();
        });
    });

    document.addEventListener('click', function(event) {
        if (event.target.matches('.btn-update-cart')) {
            updateCartEventListener(event);
        } else if (event.target.matches('.remove-from-cart')) {
            removeFromCartEventListener(event);
        }
    });

    document.querySelector('#impuesto-select').addEventListener('change', actualizarTotalCarritoConImpuestos);

    document.querySelectorAll('.expand-on-hover').forEach(img => {
        img.addEventListener('mouseover', () => {
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
    if (totalCarritoEl) {
        totalCarritoEl.textContent = `$${total.toFixed(2)}`;
    } else {
        console.log('Elemento total-carrito no encontrado');
    }

    const finalizePurchaseButton = document.getElementById('finalize-purchase-button');
    if (finalizePurchaseButton) {
        finalizePurchaseButton.removeAttribute('disabled');
    } else {
        console.log('Elemento finalize-purchase-button no encontrado');
    }
}

function updateSubtotal(productId, quantity) {
    const productRow = document.getElementById(`product-row-${productId}`);
    const priceCell = productRow.querySelector('.product-price');
    const subtotalCell = productRow.querySelector('.subtotal-cell');

    const price = parseFloat(priceCell.textContent.trim().replace('$', ''));
    const subtotal = price * quantity;

    subtotalCell.textContent = `$${subtotal.toFixed(2)}`;
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
        case '3':
            if (desiredPriceInputValue !== undefined && desiredPrice > 0) {
                quantityToSend = desiredPrice / (pricePerUnit * 1000);
            }
            break;
        case '2':
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            document.querySelector(`#product-row-${productId} .subtotal-cell`).textContent = `$${parseFloat(data.new_subtotal).toFixed(2)}`;
            actualizarTotalCarritoConImpuestos();
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
    const impuestoId = document.querySelector('#impuesto-select').value;
    fetch(`${BASE_URL}/inventario/api/total-con-impuestos/?impuesto_id=${impuestoId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Datos recibidos de la API:', data);
        const totalCarritoEl = document.querySelector('.total-carrito');
        if (totalCarritoEl) {
            const totalConImpuestos = parseFloat(data.total_con_impuestos);
            if (!isNaN(totalConImpuestos)) {
                totalCarritoEl.textContent = `$${totalConImpuestos.toFixed(2)}`;
            } else {
                console.error('Total con impuestos no es un número válido:', data.total_con_impuestos);
            }
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

        if (!cartItemsContainer) {
            console.error("El contenedor de ítems del carrito no se encontró.");
            return;
        }

        if (!data || data.length === 0 || !data[0].items || data[0].items.length === 0) {
            console.error('No se encontraron elementos en la respuesta de la API:', data);
            cartItemsContainer.innerHTML = '<tr><td colspan="6">No hay productos en el carrito.</td></tr>';
        } else {
            console.log("Se encontraron elementos en el carrito:", data[0].items);
            cartItemsContainer.innerHTML = '';
            data[0].items.forEach(item => {
                renderCartItem(item);
            });
            attachEventListenersToButtons();
        }

        actualizarTotalCarritoConImpuestos();
    })
    .catch(error => {
        console.error('Error al actualizar el carrito:', error);
    });
}

function getUnitAndPrice(productId) {
    const productUnitPriceMap = {
        '1': { unitId: '1', pricePerUnit: 6500 },
        '2': { unitId: '3', pricePerUnit: 6500 / 1000 },
    };

    const productInfo = productUnitPriceMap[productId];

    if (!productInfo) {
        console.error(`Información no encontrada para el producto con ID ${productId}`);
        return { unitId: '1', pricePerUnit: 0 };
    }

    return productInfo;
}

function renderCartItem(item) {
    const cartItemsContainer = document.querySelector('#cart-items-container');
    const imagePath = item.product.imagen_producto_url ? item.product.imagen_producto_url : `${BASE_URL}/path/to/default/image.png`;

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

    if (item.product.precio === null) {
        cartItemsContainer.querySelector(`.btn-add-price[data-product-id="${item.product.id}"]`).addEventListener('click', () => {
            const saveButton = document.getElementById('save-price-button');
            saveButton.dataset.productId = item.product.id;
            document.getElementById('modal-product-price').value = '';
            $('#priceModal').modal('show');
        });
    }
}

document.addEventListener('input', function(event) {
    if (event.target.matches('.desired-price-input')) {
        const productId = event.target.dataset.productId;
        const grams = parseFloat(event.target.value);
        const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.slice(1)) / 1000;
        const newSubtotal = grams * pricePerGram;
        document.querySelector(`#product-row-${productId} .subtotal-cell`).textContent = `$${newSubtotal.toFixed(2)}`;
    }
});

function updatePriceBasedOnGrams(inputElement) {
    const grams = parseFloat(inputElement.value);
    const productId = inputElement.dataset.productId;
    const pricePerGram = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent.slice(1)) / 1000;
    const newPrice = grams * pricePerGram;
    document.querySelector(`#product-row-${productId} .desired-price-input`).value = newPrice.toFixed(2);
}

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
            document.getElementById('save-price-button').dataset.productId = productId;
            $('#priceModal').modal('show');
        });
    });
}

function handleDesiredPriceInput(event) {
    const input = event.target;
    const productId = input.dataset.productId;
    const unitId = input.dataset.unitId;
    const pricePerUnit = parseFloat(input.dataset.pricePerUnit);
    const desiredPrice = parseFloat(input.value);

    let quantity;
    if (unitId === '3') {
        quantity = (desiredPrice / pricePerUnit) * 1000;
    } else if (unitId === '2') {
        quantity = desiredPrice / pricePerUnit;
    } else {
        console.error("Unidad no manejada:", unitId);
        return;
    }

    const quantityInput = document.querySelector(`#product-row-${productId} .quantity-input`);
    quantityInput.value = quantity.toFixed(2);

    actualizarCarrito(productId, quantity.toFixed(2), desiredPrice);
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
                fetchCartAndUpdateUI();
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
                    fetchCartAndUpdateUI();
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
            const productId = document.getElementById('save-price-button').dataset.productId;
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

document.addEventListener('input', function(event) {
    if (event.target.matches('.desired-price')) {
        var productId = event.target.dataset.productId;
        var unitId = event.target.dataset.unitId;
        var priceInput = parseFloat(event.target.value);
        var pricePerUnit = parseFloat(event.target.dataset.pricePerUnit);

        var quantity = priceInput / pricePerUnit;

        var quantityInput = document.querySelector(`#product-row-${productId} .quantity-input`);
        quantityInput.value = quantity.toFixed(2);
        actualizarCarrito(productId, quantity, unitId);
    }
}, false);

function loadClients() {
    fetch(`${BASE_URL}/inventario/api/clientes/`)
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('client-table-body');
        tbody.innerHTML = '';
        data.forEach(client => {
            const row = tbody.insertRow();
            row.insertCell().textContent = client.id;
            row.insertCell().textContent = client.nombre;
            row.insertCell().textContent = client.apellido;
            const actionCell = row.insertCell();
            const actionButton = document.createElement('button');
            actionButton.textContent = 'Seleccionar';
            actionButton.className = 'btn btn-primary btn-sm';
            actionButton.onclick = () => assignCartToClient(client.id);
            actionCell.appendChild(actionButton);
        });
    })
    .catch(error => console.error('Error al cargar los clientes:', error));
}

function selectClient(clientId) {
    console.log('Cliente seleccionado:', clientId);
    document.getElementById('client-select').value = clientId;
}

function assignCartToClient(clientId) {
    console.log("Cliente ID enviado:", clientId);

    const url = `${BASE_URL}/inventario/asignar-carrito-a-cliente/`;
    console.log("URL completa:", url);
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cliente_id: clientId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP status ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Carrito asignado exitosamente al cliente.');
            location.reload();
        } else {
            alert('Error al asignar el carrito al cliente: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error técnico al asignar el carrito al cliente.');
    });
}

function finalizePurchase() {
    console.log("Finalizando la compra...");
    fetch(`${BASE_URL}/inventario/finalizar-compra/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Compra finalizada correctamente', 'success');
        } else {
            showAlert('Error al finalizar la compra', 'error');
        }
    })
    .catch(error => {
        console.error('Error al finalizar la compra:', error);
        showAlert('Error al finalizar la compra', 'error');
    });
}

$('#clientModal').on('show.bs.modal', function() {
    if (!this.dataLoaded) {
        loadClients();
        this.dataLoaded = true;
    }
});

function mostrarProductosCliente(clienteId) {
    const url = `${BASE_URL}/inventario/api/cliente/${clienteId}/productos/`;
    const pagarBtn = document.getElementById('pagarBtn');
    
    if (pagarBtn) {
        pagarBtn.setAttribute('data-cliente-id', clienteId);

        fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("Datos recibidos:", data);
            const tbody = document.getElementById('productosClienteTable').getElementsByTagName('tbody')[0];
            tbody.innerHTML = '';
            let totalSinImpuestos = 0;

            data.forEach(producto => {
                let precio = parseFloat(producto.precio);
                let subtotal = producto.cantidad * precio;
                totalSinImpuestos += subtotal;
                let row = tbody.insertRow();
                row.insertCell(0).textContent = producto.descripcion;
                row.insertCell(1).textContent = producto.cantidad;
                row.insertCell(2).textContent = `$${precio.toFixed(2)}`;
                row.insertCell(3).textContent = `$${subtotal.toFixed(2)}`;
            });

            document.getElementById('totalConRecargo').textContent = `$${(totalSinImpuestos * 1.10).toFixed(2)}`;
            $('#productosClienteModal').modal('show');
        })
        .catch(error => {
            console.error('Error al cargar los productos del cliente:', error);
        });
    } else {
        console.error("pagarBtn no encontrado");
    }
}


function pagarCuentaCliente(clienteId) {
    const url = `${BASE_URL}/inventario/pagar-cuenta-cliente/${clienteId}/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP status ${response.status}`);
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `recibo_${clienteId}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error técnico al procesar el pago del cliente.');
    });
}

document.getElementById('search-button').addEventListener('click', function() {
    var query = document.getElementById('product-search').value.toLowerCase();
    query = query.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    if (query.length > 0) {
        $.ajax({
            url: '/inventario/api/buscar-productos/',
            data: { q: query },
            success: function(data) {
                var tbody = document.getElementById('search-results-body');
                tbody.innerHTML = '';
                data.results.forEach(function(product) {
                    var row = `<tr>
                        <td><img src="${product.imagen_url}" alt="${product.text}" height="50"></td>
                        <td>${product.text}</td>
                        <td>${product.precio ? `$${product.precio.toFixed(2)}` : 'N/A'}</td>
                        <td>${product.cantidad}</td>
                        <td><button class="btn btn-primary" onclick="addToCart(${product.id})">Agregar</button></td>
                    </tr>`;
                    tbody.insertAdjacentHTML('beforeend', row);
                });
                $('#searchResultsModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error("Error en la solicitud AJAX:", status, error);
            }
        });
    }
});
