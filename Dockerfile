# Utiliza una imagen oficial de Python como base
FROM python:3.11.4

# Instala dependencias necesarias para la compilación de ciertas librerías Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt en el contenedor y lo instala
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Instala Gunicorn y verifica su instalación
RUN pip install gunicorn
RUN gunicorn --version  # Verifica que Gunicorn está instalado correctamente
RUN which gunicorn      # Verifica la ubicación de Gunicorn

# Copia el resto del código de tu aplicación en el contenedor
COPY . /app/

# Crea el directorio para los archivos estáticos recolectados
RUN mkdir -p /app/staticfiles

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8001

# Comando para ejecutar la aplicación utilizando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "sistema.wsgi:application"]

