# ai_engines/base.py

class BaseAIEngine:
    def __init__(self):
        pass

    def ask(self, prompt: str) -> str:
        raise NotImplementedError("ask() must be implemented by subclasses")
