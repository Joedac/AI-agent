import os
import time
from threading import Thread

import gradio as gr
from PIL import Image
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, VisitWebpageTool
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from models.llm import MistralLLM
from tools.file_tool import FileTool
from tools.mail_tool import MailTool
from tools.system_tool import SystemMonitorTool

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("Mistral API key not found in .env")

files_dir = "files"
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

latest_file = {"name": "", "content": "", "timestamp": 0}


class FileWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        self.update_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self.update_file(event.src_path)

    def update_file(self, path):
        global latest_file
        if files_dir in path:
            file_name = os.path.basename(path)
            try:
                latest_file = {
                    "name": file_name,
                    "content": "",
                    "timestamp": time.time(),
                    "path": path,
                }

                if not is_image_file(file_name):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            latest_file["content"] = f.read()
                    except Exception as e:
                        print(f"Error reading file as text: {e}")

            except Exception as e:
                print(f"Error processing file: {e}")


def is_image_file(filename):
    """Vérifie si un fichier est une image basée sur son extension."""
    return filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))


def load_image(image_path):
    """Charge une image en mémoire et la retourne si elle existe."""
    if not image_path or not os.path.exists(image_path):
        print(f"Image path doesn't exist: {image_path}")
        return None

    try:
        img = Image.open(image_path)
        if img.mode == "RGBA":
            img = img.convert("RGB")

        return img
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def start_monitoring():
    handler = FileWatcher()
    observer = Observer()
    observer.schedule(handler, files_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def list_files():
    return [
        f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))
    ]


def display_latest_file():
    global latest_file
    file_list = list_files()

    if latest_file["name"] and latest_file["name"] in file_list:
        is_image = is_image_file(latest_file["name"])
        file_path = os.path.join(files_dir, latest_file["name"])

        img = None
        if is_image:
            img = load_image(file_path)

        return latest_file["name"], latest_file["content"], file_list, is_image, img
    elif file_list:
        first_file = file_list[0]
        is_image = is_image_file(first_file)
        file_path = os.path.join(files_dir, first_file)

        content = ""
        img = None

        if is_image:
            img = load_image(file_path)
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                content = "Erreur de lecture du fichier"

        return first_file, content, file_list, is_image, img

    return "", "", file_list, False, None


def display_selected_file(file_name):
    if not file_name:
        return "", False, None

    file_path = os.path.join(files_dir, file_name)

    if os.path.exists(file_path):
        is_image = is_image_file(file_name)

        content = ""
        img = None

        if is_image:
            img = load_image(file_path)
            content = f""
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"Erreur lors de la lecture du fichier: {str(e)}"

        return content, is_image, img
    else:
        return "File does not exist.", False, None


def run_agent(prompt):
    result = agent.run(prompt)
    time.sleep(0.5)
    name, content, file_list, is_image, img = display_latest_file()
    return result, name, content, file_list, is_image, img


mistral_model = MistralLLM(api_key=api_key)
agent = CodeAgent(
    tools=[
        FileTool.write_to_file,
        FileTool.read_from_file,
        MailTool.send_email,
        DuckDuckGoSearchTool(),
        VisitWebpageTool(),
        SystemMonitorTool.get_system_info,
    ],
    model=mistral_model,
    additional_authorized_imports=[
        "io",
        "os",
        "smtplib",
        "email.mime.text",
        "email.mime.multipart",
        "requests",
        "bs4",
        "matplotlib",
        "matplotlib.pyplot",
        "reportlab",
        "fpdf",
        "PyPDF2",
        "pdfrw",
    ],
)

monitoring_thread = Thread(target=start_monitoring, daemon=True)
monitoring_thread.start()

AGENT_DESCRIPTION = """
#
## Qu'est-ce que c'est?
Cet agent IA est un assistant intelligent capable de réaliser des tâches que les modèles de langage traditionnels ne peuvent pas faire. Contrairement à ChatGPT qui peut uniquement générer du texte, cet agent peut **agir dans le monde réel** grâce à ses outils.

## Que peut faire cet agent?
* 📝 **Créer et manipuler des fichiers** - L'agent peut écrire et lire des fichiers sur le système
* 📊 **Analyser le système** - Il peut surveiller l'utilisation CPU, mémoire et disque et générer des graphiques
* 🔍 **Rechercher des informations** - Il peut chercher des informations sur internet
* 📧 **Envoyer des emails** - Il peut rédiger et envoyer des emails

## Comment l'utiliser?
1. Tapez votre demande dans le champ "Prompt"
2. Cliquez sur "Execute" pour que l'agent réponde et agisse

## Exemples de prompts:
* "Crée un fichier texte contenant une liste de 10 idées de projets IA"
* "Génère un rapport sur l'état actuel du système avec des graphiques"
* "Recherche des informations sur les dernières avancées en IA et résume-les dans un fichier"
* "Écris un script Python qui calcule la suite de Fibonacci"

Ce projet démontre comment les agents IA vont au-delà de la simple génération de texte en intégrant capacités d'action et d'interaction avec l'environnement.
"""

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# 🤖 AI Agent")

    with gr.Accordion(
        "📚 À propos de cet agent (Cliquez pour en savoir plus)", open=False
    ):
        gr.Markdown(AGENT_DESCRIPTION)

    with gr.Row():
        prompt_input = gr.Textbox(
            label="🚀 Prompt", placeholder="Type your request here..."
        )
        execute_button = gr.Button("Execute")

    with gr.Row():
        with gr.Column():
            agent_output = gr.Textbox(label="Agent Response", interactive=False)

        with gr.Column():
            with gr.Row():
                file_label = gr.Textbox(
                    label="Currently displayed file", interactive=False
                )
                files_dropdown = gr.Dropdown(
                    choices=list_files(),
                    label="All files",
                    interactive=True,
                    allow_custom_value=True,
                )
                refresh_button = gr.Button("🔄")

            # Afficher le contenu texte et l'image côte à côte
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Contenu texte")
                    file_content = gr.Textbox(
                        label="File content", lines=15, interactive=False
                    )

                with gr.Column(scale=1):
                    gr.Markdown("### Contenu image")
                    file_image = gr.Image(label="Image content", type="pil")

    def run_and_update(prompt):
        agent_response, file_name, content, file_list, is_image, img = run_agent(prompt)

        new_dropdown = gr.Dropdown(
            choices=file_list,
            value=file_name,
            label="All files",
            interactive=True,
            allow_custom_value=True,
        )

        if is_image:
            content = f""

        return agent_response, file_name, content, new_dropdown, img

    execute_button.click(
        run_and_update,
        inputs=[prompt_input],
        outputs=[agent_output, file_label, file_content, files_dropdown, file_image],
    )

    def display_and_update_file(file_name):
        content, is_image, img = display_selected_file(file_name)
        return file_name, content, img

    files_dropdown.change(
        display_and_update_file,
        inputs=[files_dropdown],
        outputs=[file_label, file_content, file_image],
    )

    def refresh_all():
        name, content, file_list, is_image, img = display_latest_file()

        new_dropdown = gr.Dropdown(
            choices=file_list,
            value=name,
            label="All files",
            interactive=True,
            allow_custom_value=True,
        )

        if is_image:
            content = f""

        return name, content, new_dropdown, img

    refresh_button.click(
        refresh_all, outputs=[file_label, file_content, files_dropdown, file_image]
    )

app.launch(server_name="0.0.0.0", server_port=8501, share=True, debug=True)
