# RxAI - Radiografía Inteligente

RxAI es una aplicación de inteligencia artificial desarrollada para clasificar imágenes de rayos X en tres clases: **Covid**, **Normal** y **Neumonía Viral**. Este proyecto ha sido diseñado con una arquitectura modular y reproducible utilizando **Kubeflow Pipelines**, contenedores Docker y GitHub Actions para CI/CD.

## 🚀 Características Principales

- Clasificación de imágenes de rayos X con MobileNetV2
- Ajuste de pesos por clase y tasa de dropout parametrizable
- Pipeline de entrenamiento automatizado con Kubeflow
- Imagen Docker lista para despliegue en local o en clúster
- Validación automática del pipeline y Dockerfile con GitHub Actions

## 🧪 Estructura del Proyecto

```
rxai/
├── data/                        # Imágenes de entrenamiento y validación
├── docker/                      # Dockerfile y recursos de entorno
├── pipelines/                   # YAML de Kubeflow pipeline
├── scripts/                     # Código de entrenamiento y métricas
├── main.py                      # Entrenamiento CNN base
├── rxai_pipeline_parametrizable.yaml
├── rxai_pipeline_from_git_parametrizable.yaml
├── Dockerfile                   # Imagen con entorno completo
├── requirements.txt
└── .github/workflows/           # Acciones de GitHub para validación y despliegue
```

## 📦 Imagen Docker

Construida con:

- Python 3.9
- Tensorflow 2.12
- scikit-learn, matplotlib, seaborn, boto3, opencv-python

```bash
docker pull jmontalvof/rxai-pipeline:latest
docker run -p 8888:8888 jmontalvof/rxai-pipeline:latest
```

## 📋 Entrenamiento desde Kubeflow

1. Carga el pipeline `rxai_pipeline_from_git_parametrizable.yaml`
2. Crea un experimento en Kubeflow
3. Ajusta los parámetros del entrenamiento
4. Ejecuta el pipeline y visualiza los resultados

## ✅ Validación CI

Se ejecutan automáticamente las siguientes validaciones:

- Sintaxis del pipeline YAML (`dsl-compile`)
- Validación del Dockerfile (`docker build`)

## 📅 Fecha de despliegue inicial

11/05/2025
