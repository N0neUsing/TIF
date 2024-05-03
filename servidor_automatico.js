const localtunnel = require('localtunnel');

const allowedSubdomain = 'sistema-delvalle-noneuser';  // Subdominio permitido

async function startTunnel() {
    while (true) {  // Ciclo infinito para mantener el intento continuo
        try {
            const tunnel = await localtunnel({ port: 8000, subdomain: allowedSubdomain });

            console.log('LocalTunnel está funcionando correctamente en:', tunnel.url);

            tunnel.on('close', () => {
                console.error('Túnel cerrado. Intentando reconectar...');
                // No necesitamos comprobar reintentos ya que debe seguir intentando indefinidamente
                restartTunnel();
            });

            tunnel.on('error', (error) => {
                console.error('Error en LocalTunnel:', error.message);
                tunnel.close();
                restartTunnel();  // Reiniciar el túnel en caso de error
            });

            return;  // Salir del ciclo si el túnel se establece correctamente
        } catch (error) {
            console.error('Error al iniciar LocalTunnel:', error.message);
            // Espera 10 segundos antes de reintentar en caso de error
            await new Promise(resolve => setTimeout(resolve, 10000));
        }
    }
}

function restartTunnel() {
    console.log('Reiniciando LocalTunnel...');
    startTunnel();  // Volver a iniciar el túnel
}

startTunnel();
