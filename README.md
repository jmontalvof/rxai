# RxAI - Clasificación de Imágenes Médicas con Kubeflow 🚀

Este proyecto utiliza TensorFlow y Kubeflow Pipelines para entrenar modelos CNN sobre imágenes de rayos X, con una arquitectura modular y reproducible.

---

## 📦 Estructura del proyecto

```
rxai/
├── pipelines/
│   ├── train_pipeline_parametrizado.py
│   └── yamls/
│       ├── rxai_pipeline_parametrizable.yaml
│       └── clone_and_train.yaml  ← ← Este permite clonar el repo y ejecutar main.py
├── docker/
│   └── Dockerfile
├── data/
│   └── README.md
├── docs/
│   └── resultados.md
├── scripts/
│   └── compilar_pipeline.sh
├── main.py
└── README.md
```

---

## 🧪 ¿Cómo lanzar el pipeline desde Kubeflow?

1. Ve a **Kubeflow Dashboard → Pipelines → Upload pipeline**
2. Sube el archivo:  
   `pipelines/yamls/clone_and_train.yaml`

3. Dale nombre al pipeline, por ejemplo:
   ```
   RxAI Clone and Run
   ```

4. Al crear un **run**, podrás establecer:
   - `repo-url`: `https://github.com/jmontalvof/rxai.git`
   - `script`: `main.py`

5. Ejecuta y observa los logs desde la pestaña **Logs** del paso `main`

---

## ☁️ Dataset

El dataset (`dataset.zip`) se encuentra almacenado en MinIO y no está incluido en el repo por límites de GitHub.

---

## 🐳 Imagen Docker recomendada

Utiliza tu propia imagen con dependencias preinstaladas:

```
jmontalvof/rxai-pipeline:latest
```

Puedes modificar el pipeline para usar esta imagen en lugar de `python:3.9`.

---

## 🧠 Resultados

Puedes registrar tus ejecuciones y métricas en:  
`docs/resultados.md`

---

## ✨ Autor

Jorge Montalvo (@jmontalvof)
