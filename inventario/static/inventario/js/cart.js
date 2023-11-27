// Actualización del carrito
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-update-cart').forEach(button => {
        button.addEventListener('click', () => {
            let productId = button.dataset.productId;
            actualizarCarrito(productId);
        });
    });
    

// Función para actualizar el carrito
function actualizarCarrito(productId) {
    let quantityInput = document.querySelector(`#product-row-${productId} input[name='quantity']`);
    let quantity = parseFloat(quantityInput.value);
    let price = parseFloat(document.querySelector(`#product-row-${productId} .product-price`).textContent);
    let newSubtotal = quantity * price;

    let formData = new FormData();
    formData.append('quantity', quantity);

    fetch(`/inventario/actualizar-item-carrito/${productId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let subtotalCell = document.querySelector(`#product-row-${productId} .subtotal-cell`);
            subtotalCell.textContent = `${newSubtotal.toFixed(2)}`;
            actualizarTotalCarrito();
            showAlert('Cantidad actualizada correctamente', 'success');
        } else {
            showAlert(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error al actualizar el carrito:', error);
        showAlert('Error al actualizar el carrito', 'error');
    });
}

// Función para actualizar el total del carrito
function actualizarTotalCarrito() {
    let total = 0;
    document.querySelectorAll('.subtotal-cell').forEach(cell => {
        total += parseFloat(cell.textContent);
    });
    document.querySelector('.total-carrito').textContent = `${total.toFixed(2)}`;
}

// Función para obtener el valor de una cookie
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

// Función para mostrar alertas
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
}})

document.querySelectorAll('.expand-on-hover').forEach(img => {
    let timer;
    img.addEventListener('mouseover', () => {
        timer = setTimeout(() => {
            img.classList.add('hovered');
        }, 2000); // 2000 milisegundos = 2 segundos
    });

    img.addEventListener('mouseout', () => {
        clearTimeout(timer);
        img.classList.remove('hovered');
    });
});