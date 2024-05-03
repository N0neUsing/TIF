document.addEventListener('DOMContentLoaded', function() {
    const manageTaxesButton = document.getElementById('manageTaxesButton');
    const taxModal = document.getElementById('manageTaxesModal');
    const taxForm = document.getElementById('taxForm');
    const taxTableBody = document.getElementById('taxTableBody');


    manageTaxesButton.addEventListener('click', function() {
        console.log('Botón de gestión de impuestos clickeado');
        fetchImpuestos(); // Cargar los impuestos antes de que el modal se abra
    });

    taxModal.addEventListener('shown.bs.modal', function () {
        console.log(document.getElementById('taxName'));
    });

    taxForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const taxName = document.getElementById('taxName');
        const taxRate = document.getElementById('taxRate');
        if (taxName && taxRate) {
            const name = taxName.value;
            const rate = taxRate.value;
            const taxId = taxForm.getAttribute('data-tax-id');

            if (taxId) {
                updateImpuesto(taxId, name, rate);
            } else {
                addImpuesto(name, rate);
            }
        } else {
            console.error('Error: Form elements not found!');
        }
    });
});

function fetchImpuestos() {
    console.log('Fetching impuestos...');
    fetch('/inventario/impuestos/')
    .then(response => {
        console.log('Respuesta recibida para impuestos:', response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Asegura que la respuesta sea JSON antes de procesarla
    })
    .then(data => {
        taxTableBody.innerHTML = ''; // Limpiar la tabla antes de agregar nuevos datos
        data.forEach(tax => {
            const row = taxTableBody.insertRow();
            row.innerHTML = `
                <td>${tax.nombre}</td>
                <td>${tax.tasa}</td>
                <td>
                    <button class="btn btn-success" onclick="editImpuesto('${tax.id}', '${tax.nombre}', '${tax.tasa}')">Editar</button>
                    <button class="btn btn-danger" onclick="deleteImpuesto('${tax.id}')">Eliminar</button>
                </td>
            `;
        });
    })
    .catch(error => console.error('Error al cargar impuestos:', error));
}


    function addImpuesto(nombre, tasa) {
        fetch('/inventario/impuestos/crear/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ nombre, tasa })
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            fetchImpuestos();  // Recargar lista de impuestos
            taxForm.reset();   // Limpiar formulario
            taxForm.removeAttribute('data-tax-id');
        })
        .catch(error => console.error('Error al agregar impuesto:', error));
    }
    

    function updateImpuesto(id, nombre, tasa) {
    fetch(`/inventario/impuestos/editar/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()  // Asegúrate de obtener el token CSRF correctamente
        },
        body: JSON.stringify({ nombre, tasa })
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        fetchImpuestos();  // Recargar lista de impuestos
        taxForm.reset();   // Limpiar formulario
        taxForm.removeAttribute('data-tax-id');
    })
    .catch(error => console.error('Error al actualizar impuesto:', error));
}


    window.editImpuesto = function(id, nombre, tasa) {
        document.getElementById('taxName').value = nombre;
        document.getElementById('taxRate').value = tasa;
        taxForm.setAttribute('data-tax-id', id);  // Guardar id para uso en la actualización
    };

    window.deleteImpuesto = function(id) {
        fetch(`/inventario/impuestos/eliminar/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()  // Asegúrate de obtener el token CSRF correctamente
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            fetchImpuestos();  // Recargar lista de impuestos
        })
        .catch(error => console.error('Error al eliminar impuesto:', error));
    };
    

    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
