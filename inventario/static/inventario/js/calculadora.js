// C A L C U L A D O R A   D E   P R E C I O S  //
function toggleCalculationMode() {
    var mode = document.getElementById('calculationMode').value;
    var unitsLabel = document.getElementById('unitsGroup').getElementsByTagName('label')[0];
    var unitsInput = document.getElementById('units');

    if (mode === 'unit') {
        unitsLabel.textContent = 'Número de Unidades:';
        unitsInput.placeholder = 'Número de unidades en la caja';
    } else if (mode === 'weight') {
        unitsLabel.textContent = 'Peso en Gramos:';
        unitsInput.placeholder = 'Peso total en gramos';
    }
}

function calculatePrice() {
    var mode = document.getElementById('calculationMode').value;
    var purchasePrice = parseFloat(document.getElementById('purchasePrice').value);
    var units = parseFloat(document.getElementById('units').value);
    var margin = parseFloat(document.getElementById('margin').value);
    var subtotal = parseFloat(document.getElementById('subtotal').value); // Asegurarse de recuperar el valor del subtotal
    var totalFinal = parseFloat(document.getElementById('totalFinal').value); // Asegurarse de recuperar el valor del total final

    if (!purchasePrice || !units || !margin || isNaN(subtotal) || isNaN(totalFinal)) {
        alert('Por favor, completa todos los campos con valores numéricos válidos.');
        return;
    }

    // Calcular el porcentaje de impuesto y mostrarlo en el campo correspondiente
    var taxPercentage = ((totalFinal - subtotal) / subtotal) * 100;
    document.getElementById('taxPercentage').value = taxPercentage.toFixed(2) + '%';

    var costPerUnitBeforeTax;
    var sellingPrice;
    var resultText;

    if (mode === 'unit') {
        costPerUnitBeforeTax = purchasePrice / units;
    } else if (mode === 'weight') {
        var weightInKg = units / 1000; // Convertir gramos a kilogramos
        costPerUnitBeforeTax = purchasePrice / weightInKg;
    }

    var costPerUnitIncludingTax = costPerUnitBeforeTax * (1 + (taxPercentage / 100));
    sellingPrice = costPerUnitIncludingTax * (1 + (margin / 100));

    if (mode === 'unit') {
        resultText = "El precio de venta por unidad es de $" + sellingPrice.toFixed(2);
    } else if (mode === 'weight') {
        resultText = "El precio de venta del producto por kg es de $" + sellingPrice.toFixed(2);
    }

    document.getElementById('calculatedPrice').value = resultText;
}

function resetForm() {
    document.getElementById('priceCalcForm').reset();
    document.getElementById('calculatedPrice').value = "";
    document.getElementById('taxPercentage').value = ""; // Restablecer también el campo de porcentaje de impuesto
}

function addPrice() {
    var priceInput = document.getElementById('calculatedPrice').value;
    if (priceInput) {
        document.getElementById('precio').value = priceInput.split('$')[1]; // Extraer solo el valor numérico para agregarlo al campo principal
    }
    $('#priceCalcModal').modal('hide');
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
}

document.addEventListener('DOMContentLoaded', function() {
    toggleCalculationMode(); // Set initial state of form fields based on default selection
});
