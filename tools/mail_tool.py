import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smolagents import tool


class MailTool:
    @staticmethod
    @tool
    def send_email(recipient: str, subject: str, content: str) -> str:
        """Send an email after user validate it.
        Args:
            recipient: recipient email adress
            subject: email subject
            content: email content
        Returns:
            error or succes message
        """

        print("\n--- 📨 Détails de l'e-mail ---")
        print(f"Destinataire: {recipient}")
        print(f"Sujet: {subject}")
        print(f"Contenu:\n{content}")

        confirmation = input("\n📨 Voulez-vous envoyer cet e-mail ? (oui/non): ").strip().lower()

        if confirmation != "oui":
            return "Envoi annulé par l'utilisateur."

        gmail_user = os.getenv("EMAIL_USER")
        gmail_password = os.getenv("EMAIL_PASSWORD")

        if not gmail_user or not gmail_password:
            return "Error: Gmail credentials not in .env"

        try:
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = gmail_user
            msg["To"] = recipient
            msg.attach(MIMEText(content, "html"))


            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_user, gmail_password)
                server.send_message(msg)
                return f"📨 Mail send successfully to {recipient}"
        except Exception as e:
            return f"Erreur lors de l'envoi : {e}"
