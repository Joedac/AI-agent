import os
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from models.llm import MistralLLM
from tools.file_tool import FileTool
from tools.mail_tool import MailTool
from tools.ascii_art import display_ascii_art

def main():

    display_ascii_art()

    load_dotenv()

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Erreur: Mistral API key not found in .env")
        return

    mistral_model = MistralLLM(api_key=api_key)

    agent = CodeAgent(
        tools=[
            FileTool.write_to_file,
            FileTool.read_from_file,
            MailTool.send_email,
            DuckDuckGoSearchTool()
        ],
        model=mistral_model,
        additional_authorized_imports=[
            "os",
            "smtplib",
            "email.mime.text",
            "email.mime.multipart",
            "requests",
            "bs4"
        ],
    )

    print("🤖 Salam ! Que puis je faire pour toi ? (ou 'quit' pour quitter):")
    while True:
        user_prompt = input("🚀 prompt > ")

        if user_prompt.lower() == 'quit':
            print("👋 See you later khouya !")
            break

        if user_prompt.strip():
            result = agent.run(user_prompt)
            print("\nRésultat :")
            print(result)
            print("\n-------------------\n")
        else:
            print("Prompt must not be empty.")


if __name__ == "__main__":
    main()
