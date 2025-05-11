# Imagen base con Python y pip
FROM python:3.9-slim

# Instalar dependencias del sistema (para matplotlib, PIL, etc.)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements si los tienes (opcional)
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Instalar dependencias necesarias
RUN pip install --no-cache-dir \
    tensorflow==2.12 \
    scikit-learn \
    matplotlib \
    seaborn \
    boto3 \
    pandas \
    numpy \
    opencv-python \
    pillow

# Copia tu código dentro de la imagen (opcional si quieres pruebas locales)
# COPY . .

# Comando por defecto
CMD ["python"]
