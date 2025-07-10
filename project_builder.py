# project_builder.py

import os
from ai_engines.gpt4free import GPT4FreeEngine

class ProjectBuilder:
    def __init__(self, root_dir="generated_project"):
        self.root_dir = root_dir
        self.ai = GPT4FreeEngine()

    def build_from_prompt(self, prompt):
        try:
            os.makedirs(self.root_dir, exist_ok=True)
            plan_prompt = f"Based on this prompt, generate a folder and file structure plan:\n\n{prompt}"
            plan = self.ai.ask(plan_prompt)

            self.save_to_file("plan.txt", plan)

            for filename in self.extract_filenames(plan):
                file_prompt = f"Generate the full code for the file `{filename}` based on the project: {prompt}"
                code = self.ai.ask(file_prompt)
                self.save_to_file(filename, code)

            return f"✅ Project generated in: {self.root_dir}"

        except Exception as e:
            return f"[Error] {str(e)}"

    def extract_filenames(self, plan):
        lines = plan.splitlines()
        return [line.strip().lstrip("- ").strip("/") for line in lines if "." in line and not line.startswith("#")]

    def save_to_file(self, relative_path, content):
        full_path = os.path.join(self.root_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
