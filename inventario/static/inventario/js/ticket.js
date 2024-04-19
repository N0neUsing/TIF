<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Compra Completa</title>
    <script>
    document.addEventListener('DOMContentLoaded', function () {
        const printButton = document.getElementById('printButton');
        printButton.addEventListener('click', function () {
            navigator.bluetooth.requestDevice({ filters: [{ services: ['000018f0-0000-1000-8000-00805f9b34fb'] }] })
            .then(device => device.gatt.connect())
            .then(server => server.getPrimaryService('000018f0-0000-1000-8000-00805f9b34fb'))
            .then(service => service.getCharacteristic('00002af1-0000-1000-8000-00805f9b34fb'))
            .then(characteristic => {
                let encoder = new TextEncoder('utf-8');
                let data = encoder.encode("Texto para imprimir\n");
                return characteristic.writeValue(data);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Falló la impresión: ' + error);
            });
        });
    });
    </script>
</head>
<body>
    <h1>Compra completada con éxito</h1>
    <button id="printButton">Imprimir Ticket</button>
</body>
</html>
