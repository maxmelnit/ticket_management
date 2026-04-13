import ollama # I'll use a simple Ollama model to avoid using 

def route(Ticket):
    
    def generate_schema(Ticket):
        schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"]
            },
            "tier": {
                "type": "integer",
                "enum": [1, 2, 3, 4]
            },
            "language": {"type": "string"}
        },
        "required": ["title", "priority", "tier", "language"]
    }

        response = ollama.chat(
            model='gemma3',
            messages=[{'role': 'user', 'content': 'Extract a task title and priority from: Fix login bug urgently'}],
            format=schema,
        )

        return response.message.content

if __name__ == "__main__":
    router()
