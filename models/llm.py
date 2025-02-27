from dataclasses import dataclass
from mistralai import Mistral
from typing import Optional


@dataclass
class LLMResponse:
    content: str


class MistralLLM:
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"

    def __call__(self, prompt: str, **kwargs) -> LLMResponse:
        """Call Mistral API, return response"""
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """Tu es un assistant qui peut utiliser les fonctions fournies pour effectuer des tâches.
                                            Les fonctions sont disponibles, utilises les directement, c'est très important.
                                            Répond toujours en respectant ce forat:

                                            Thought: Your thoughts
                                            Code:
                                            ```py
                                            # Your code here
                                            ```<end_code>""",
                },
                {"role": "user", "content": str(prompt)},
            ],
        )
        return LLMResponse(content=response.choices[0].message.content)
