import kfp
from kfp import dsl

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["git"]
)
def clone_repo_op(repo_url: str):
    import subprocess
    subprocess.run(["git", "clone", repo_url], check=True)

@dsl.pipeline(
    name="RxAI Clone y Entrenamiento",
    description="Pipeline que clona el repo de GitHub y ejecuta el main.py"
)
def rxai_pipeline():
    clone_task = clone_repo_op("https://github.com/jmontalvof/rxai.git")

