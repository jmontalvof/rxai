# Esquema de Arquitectura - RxAI

1. **Entrenamiento local**
   - Entrenamiento del modelo CNN en main.py con parámetros ajustables.
   - Evaluación con métricas como Accuracy y F1-Score.
   - Visualización de resultados.

2. **Contenedor Docker**
   - Dockerfile con dependencias de IA.
   - Ejecutable en Jupyter Lab (`CMD`) o para pipelines.

3. **Kubeflow Pipeline**
   - Definición en YAML (`rxai_pipeline_parametrizable.yaml`).
   - Componentes parametrizables con class_weights, dropout, etc.
   - Entrenamiento automatizado desde interfaz de Kubeflow.

4. **GitHub Actions**
   - Validación automática de la pipeline y Dockerfile.
   - Archivo `.github/workflows/validate-rxai.yml`.

5. **Opcional**
   - Notebook JupyterLab lanzado desde Kubeflow para pruebas en GPU.