import os
from modal import Image, Secret, Stub, wsgi_app

image = (
    Image.debian_slim(python_version="3.11")
        .apt_install("ffmpeg")
        .pip_install_from_requirements("requirements.txt")
        .copy_local_dir('staticfiles', '/root/staticfiles')
        .copy_local_dir('todoApp', '/root/todoApp')
        .copy_local_dir('todos', '/root/todos')
        .copy_local_file('manage.py', '/root/manage.py')
        .run_commands(
            "python /root/manage.py migrate",
            secrets=[Secret.from_name("surukoto-secret")],
        )
)

with image.imports():
    import whisper
    whisper.load_model("medium.en")

stub = Stub(name="surukoto", image=image)

@stub.function(
        secret=Secret.from_name("surukoto-secret"), 
        gpu="T4", 
        concurrency_limit=1, 
        container_idle_timeout=300,
    )
@wsgi_app()
def run():
    from todoApp.wsgi import application
    return application

