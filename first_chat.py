import requests as req

response = req.post(
    "http://localhost:11434/api/chat",
    json={
        "model":"llama3.2:3b",
        "messages":[
            {
                "role": "user",
                "content":"Explain what an API is in two sentences."
            }
        ],
        "stream": False
    },
    timeout=120,
)

print(response.json()["message"]["content"])