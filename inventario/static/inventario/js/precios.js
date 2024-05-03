function calculatePrice() {
    var mode = document.getElementById('calculationMode').value;
    var purchasePrice = parseFloat(document.getElementById('purchasePrice').value);
    var units = parseFloat(document.getElementById('units').value);
    var margin = parseFloat(document.getElementById('margin').value);
    var subtotal = parseFloat(document.getElementById('subtotal').value);
    var totalFinal = parseFloat(document.getElementById('totalFinal').value);

    if (!purchasePrice || !units || !margin || !subtotal || !totalFinal) {
        alert('Por favor, completa todos los campos');
        return;
    }

    var taxPercentage = ((totalFinal - subtotal) / subtotal) * 100;
    var costPerUnitBeforeTax;
    var sellingPrice;
    var resultText;

    if (mode === 'unit') {
        costPerUnitBeforeTax = purchasePrice / units;
    } else if (mode === 'weight') {
        // Convertir gramos a kilogramos si el modo de peso está seleccionado
        var weightInKg = units / 1000;
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