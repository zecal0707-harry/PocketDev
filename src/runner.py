import urllib.request
import json

class AgentRunner:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def call_llm(self, prompt: str, model: str) -> str:
        url = "https://api.example.com/v1/generate"
        data = json.dumps({"prompt": prompt, "model": model}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={"Authorization": self.api_key})
        
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
