
console.log("cart.js cargado.");
const BASE_URL = 'https://sistema-delvalle-noneuser.loca.lt';
//const BASE_URL = 'http://localhost:8000';
const MEDIA_URL = '/media/';


document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM completamente cargado y analizado.");
    
    // Inicia el polling aquí, justo después de que el DOM esté completamente cargado.
    // Esto asegura que solo se inicie una vez y no cada vez que se agrega un producto al carrito.
    fetchCartAndUpdateUI(); // Llama a la función inmediatamente para cargar los artículos
    // Remover el setInterval si decides actualizar el carrito solo después de las acciones del usuario

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
            if (quantityInput) {
                const quantity = parseInt(quantityInput.value, 10);
                console.log("Valor de cantidad obtenido:", quantityInput.value);
                if (!isNaN(quantity)) {
                    actualizarCarrito(productId, quantity);
                } else {
                    console.error("La cantidad no es un número", quantityInput.value);
                }
            } else {
                console.error(`No se encontró el input de cantidad para el producto ${productId}.`);
            }
        });
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

function actualizarCarrito(productId, quantity) {
    // Verificar si el valor de 'quantity' es válido
    if (quantity === undefined || quantity === null || isNaN(quantity)) {
        console.error("La cantidad es inválida: ", quantity);
        showAlert('Error: La cantidad es inválida', 'error');
        return; // Detener la ejecución si la cantidad no es válida
    }

    // Continuar si la cantidad es un número válido
    console.log("CSRF Token:", getCookie('csrftoken'));
    fetch(`${BASE_URL}/inventario/actualizar-item-carrito/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: quantity }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP status ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Actualizar el subtotal del ítem en el carrito
            document.querySelector(`#product-row-${productId} .subtotal-cell`).textContent = `$${data.new_subtotal.toFixed(2)}`;
            actualizarTotalCarrito();
            showAlert('Cantidad actualizada correctamente', 'success');
        } else {
            showAlert(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error al actualizar la cantidad en el carrito', 'error');
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



function renderCartItem(item) {
    console.log(item);
    const subtotal = (item.quantity * parseFloat(item.product.precio)).toFixed(2);
    const cartItemsContainer = document.querySelector('#cart-items-container');
    
    // Asegúrate de usar imagen_producto_url de la respuesta de la API.
    // Se cambió imagePath para usar directamente la propiedad imagen_producto_url
    const imagePath = item.product.imagen_producto_url ? item.product.imagen_producto_url : `${BASE_URL}/path/to/default/image.png`;

    const itemHTML = `
        <tr id="product-row-${item.product.id}">
            <td><img src="${imagePath}" alt="${item.product.descripcion}" height="50"></td>
            <td>${item.product.descripcion}</td>
            <td>
                <input type="number" name="quantity" value="${item.quantity}" min="1">
                <button type="button" class="btn btn-primary btn-update-cart" data-product-id="${item.product.id}">Actualizar</button>
            </td>
            <td class="product-price">$${item.product.precio}</td>
            <td class="subtotal-cell">$${subtotal}</td>
            <td>
                <button type="button" class="btn btn-danger remove-from-cart" data-product-id="${item.product.id}">Eliminar</button>
            </td>
        </tr>
    `;
    cartItemsContainer.insertAdjacentHTML('beforeend', itemHTML);
}

function attachEventListenersToButtons() {
    // Remueve los listeners existentes y añade los nuevos para evitar duplicados.
    document.querySelectorAll('.btn-update-cart').forEach(button => {
        button.removeEventListener('click', updateCartEventListener);
        button.addEventListener('click', updateCartEventListener);
    });

    document.querySelectorAll('.remove-from-cart').forEach(button => {
        button.removeEventListener('click', removeFromCartEventListener);
        button.addEventListener('click', removeFromCartEventListener);
    });
}

function updateCartEventListener(event) {
    const button = event.target;
    const productId = button.dataset.productId;
    const quantityInput = document.querySelector(`#product-row-${productId} input[name='quantity']`);

    if (quantityInput) {
        const quantity = parseInt(quantityInput.value, 10);
        if (!isNaN(quantity) && quantity > 0) {
            actualizarCarrito(productId, quantity);
        } else {
            console.error("La cantidad no es un número o es menor o igual a cero", quantityInput.value);
            showAlert('La cantidad debe ser un número mayor que cero.', 'error');
        }
    } else {
        console.error(`No se encontró el input de cantidad para el producto ${productId}.`);
    }
}

function removeFromCartEventListener(event) {
    event.preventDefault();
    const button = event.target;
    const productId = button.dataset.productId;
    fetch(`${BASE_URL}/inventario/eliminar-de-carrito/${productId}/`, { method: 'GET' })
        .then(response => {
            if (response.ok) {
                fetchCartAndUpdateUI(); // Actualiza el carrito después de eliminar un producto
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .catch(error => {
            console.error('Error al eliminar del carrito:', error);
            // Considera mostrar un mensaje al usuario aquí
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
