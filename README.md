# AI Agent

A proof of concept application using the smolagents library with Mistral AI for executing actions based on natural language instructions.

## Overview

This project demonstrates the capabilities of smolagents to create a conversational agent that can perform various tasks like file operations and sending emails based on natural language instructions.

## Requirements

- Python 3.10+
- Mistral AI API key
- Gmail account (for email functionality)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/joedac-netvigie/Ai-agent.git
   cd smolagents-poc
   ```

2. Create a Python virtual environment:
   ```
   if you don't install it :
   sudo apt install python3.10 python3.10-venv python3.10-dev
   then :
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your credentials:
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   EMAIL_USER=your_gmail_address
   EMAIL_PASSWORD=your_gmail_app_password
   ```

   Note: For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833) rather than your account password.

## Usage

Run the application:
```
python main.py
```

The agent will prompt you to enter instructions. Examples:
- "Write 'Hello world!' to a file named test.txt and then read that file"
- "Send an email to someone@example.com with the subject 'Hello' and content 'How are you?'"
- "Find the latest news on Donald Trump and resume it in 10 lines"

Type 'quit' to exit the application.


## Security Notes

- Never commit your `.env` file to the repository
- The email tool will ask for confirmation before sending any email
  Acknowledgements

## Acknowledgements
  Special thanks to [Hugging Face](https://huggingface.co/) for their [smolagents](https://github.com/huggingface/smolagents) framework that makes this project possible. SmolaAgents provides an efficient way to build lightweight agent-based applications with AI models.
## License

[MIT License](LICENSE)
