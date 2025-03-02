# AI Agent

A proof of concept application using the smolagents library with Mistral AI for executing actions based on natural language instructions.

## Overview

This project demonstrates the capabilities of smolagents to create a conversational agent that can perform various tasks like file operations and sending emails based on natural language instructions.

## Requirements

- Docker and Docker Compose
- Mistral AI API key
- Gmail account (for email functionality)

## Installation

### Option 1: Using Docker (Recommended)

1. Clone this repository:
   ```
   git clone https://github.com/joedac-netvigie/Ai-agent.git
   cd Ai-agent
   ```

2. Create a `.env` file in the root directory with your credentials:
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   EMAIL_USER=your_gmail_address
   EMAIL_PASSWORD=your_gmail_app_password
   ```

   Note: For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833) rather than your account password.

3. Create a directory for persistent data:
   ```
   mkdir -p data
   ```

4. Build and run the application:
   ```
   # Using the Makefile (simplest way)
   make build   # Build the Docker images
   make web     # Run the web interface
   
   # Or using Docker Compose directly
   docker-compose up ai-agent-web    # For web interface
   docker-compose run --rm ai-agent-cli  # For terminal interface
   ```

### Option 2: Local Installation

1. Clone this repository:
   ```
   git clone https://github.com/joedac-netvigie/Ai-agent.git
   cd Ai-agent
   ```

2. Create a Python virtual environment:
   ```
   # If Python 3.10 is not installed:
   sudo apt install python3.10 python3.10-venv python3.10-dev
   
   # Create and activate virtual environment
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your credentials as shown above.

## Usage

### Docker Mode

#### Using Makefile
```
make web     # Run the web interface
make cli     # Run the terminal interface
make build   # (Re)build Docker images
make clean   # Stop and remove containers, networks and volumes
```

#### Direct Docker Commands
```
# Web Interface
docker-compose up ai-agent-web

# Terminal Interface
docker-compose run --rm ai-agent-cli
```

Then open your browser at http://localhost:8501 to access the web interface.

### Local Mode

#### Web Interface
```
streamlit run app.py
```

#### Terminal Interface
```
python main.py
```

## Example Prompts

The agent understands natural language. Try these examples:
- "Write 'Hello world!' to a file named test.txt and then read that file"
- "Send an email to someone@example.com with the subject 'Hello' and content 'How are you?'"
- "Find the latest news on Donald Trump and resume it in 10 lines"
- "Create a Python script that downloads stock data for Apple and plots it"

Type 'quit' to exit the application in terminal mode.

## Features

- Natural language processing to understand and execute commands
- File operations (reading and writing files)
- Email sending with user confirmation
- Web search capabilities

## Security Notes

- Never commit your `.env` file to the repository
- The email tool will ask for confirmation before sending any email
- Docker containers run with read-only access to source code by default for added security

## Acknowledgements
Special thanks to [Hugging Face](https://huggingface.co/) for their [smolagents](https://github.com/huggingface/smolagents) framework that makes this project possible. SmolaAgents provides an efficient way to build lightweight agent-based applications with AI models.

## License

[MIT License](LICENSE)
