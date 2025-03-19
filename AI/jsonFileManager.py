import json


class JsonFileManager:
    def __init__(self):
        self.clean_memory = "AI/init_memory.json"
        self.memory = "AI/memory.json"

    def read(self):
        with open(self.memory, "r", encoding="utf-8") as f:
            result = json.load(f)
        return result["logs"]

    def write(self, new_memory):
        with open(self.memory, "w", encoding="utf-8") as f:
            json.dump({"logs": new_memory}, f, ensure_ascii=False, indent=4)

    def add_user_message(self, text):
        data = self.read()
        data.append({"role": "user", "content": text})
        self.write(data)

    def add_assistant_message(self, text):
        data = self.read()
        data.append({"role": "assistant", "content": text})
        self.write(data)

    def clear_memory(self):
        with open(self.clean_memory, "r", encoding="utf-8") as f:
            result = json.load(f)
        self.write(result["logs"])