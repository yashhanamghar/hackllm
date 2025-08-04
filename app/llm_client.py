from app.config import OPENAI_API_KEY
import requests
def get_openai_answer(context: str, question: str) -> str:
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4",  # or "gpt-3.5-turbo" if you want faster/cheaper
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\nAnswer:"}
        ],
        "temperature": 0.2
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.text}"