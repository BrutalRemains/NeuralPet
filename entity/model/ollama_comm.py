import requests

OLLAMA_URL = "http://localhost:11434"
MODEL = "gwen2.5:3b"

def generate_reply(system_prompt, user_input):
    payload = {
        "model": MODEL,
        "prompt": f"{system_prompt}\n\nOwner message: {user_input}",
        "stream": False
}

    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    response.raise_for_status()
    return response.json()["output"]