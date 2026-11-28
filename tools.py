from datetime import datetime
import memory

def save_fact(text):
    memory.save_fact(text)
    return "Saved."

def current_time():
    return datetime.now().strftime("%A %d %B %Y, %H:%M")

REGISTRY = {
    "save_fact": save_fact,
    "current_time": current_time
}

SCHEMAS = [
    {
        "type":"function",
        "function":{
            "name":"save_fact",
            "description":"Save one lasting fact about the user to long-term memory. Use it only when the user explicitly asks you to remember something. Do not use it for questions, passing remarks, or things said in conversation without a request to remember them. Never save passwords or other secrets.",
            "parameters":{
                "type":"object",
                "properties": {"text": {"type": "string", "description": "The fact to remember"}},
                "required": ["text"]
            },
        },
    },
    { 
        "type":"function",
        "function":{
            "name":"current_time",
            "description":"Get the current date and time from the computer's clock. Use it whenever the user asks for the time, date or day. Do not guess the time yourself, and do not use it for anything else.",
            "parameters":{
                "type":"object",
                "properties": {}
            },
        },
    },
]