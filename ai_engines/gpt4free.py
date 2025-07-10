# ai_engines/gpt4free.py

import requests
from ai_engines.base import BaseAIEngine

class GPT4FreeEngine(BaseAIEngine):
    def __init__(self):
        super().__init__()
        self.api_url = "https://chatgpt-free.p.rapidapi.com/chat"  # Example placeholder
        self.headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "demo",  # Replace with actual if needed
            "X-RapidAPI-Host": "chatgpt-free.p.rapidapi.com"
        }

    def ask(self, prompt: str) -> str:
        try:
            payload = {
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
            return f"[Error] API returned {response.status_code}"
        except Exception as e:
            return f"[Exception] {str(e)}"
