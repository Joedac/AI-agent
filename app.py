import gradio as gr
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool
from models.llm import MistralLLM
from tools.file_tool import FileTool
from tools.mail_tool import MailTool

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("Clé API Mistral non trouvée dans .env")

mistral_model = MistralLLM(api_key=api_key)
agent = CodeAgent(
    tools=[
        FileTool.write_to_file,
        FileTool.read_from_file,
        MailTool.send_email,
        DuckDuckGoSearchTool()
    ],
    model=mistral_model,
)

def run_agent(prompt):
    result = agent.run(prompt)
    return result

with gr.Blocks() as app:
    gr.Markdown("# 🤖 AI Agent")

    with gr.Row():
        prompt_input = gr.Textbox(label="🚀 prompt", placeholder="Tapez votre requête ici...")
        execute_button = gr.Button("Exécuter")

    output_text = gr.Textbox(label="Réponse", interactive=False)

    execute_button.click(run_agent, inputs=prompt_input, outputs=output_text)

app.launch(server_name="0.0.0.0", server_port=8501, share=True, debug=True)
