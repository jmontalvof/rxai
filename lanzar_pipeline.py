# Lanzar pipeline de RxAI desde un notebook en Kubeflow
import kfp
from kfp import Client

# Conexión al servidor local de Kubeflow Pipelines
client = Client(host="http://localhost:8080")  # Cambia esta URL si usas otro puerto o IP

# Ejecutar el pipeline cargado previamente en YAML
run = client.create_run_from_pipeline_package(
    pipeline_file="rxai_pipeline_from_git_parametrizable.yaml",
    arguments={
        "repo-url": "https://github.com/jmontalvof/rxai.git",
        "script": "main.py"
    },
    experiment_name="RxAI-Kubeflow-Notebook"
)

print(f"Run iniciado: {run.run_id}")
