import random

def chatbot_response(message: str) -> str:
    text = message.lower()

    if "lost" in text:
        responses = [
            "I understand. Sharing your location with the nearest police station 🚓.",
            "Don’t worry, here’s the nearest hospital 🏥 and police station 🚓.",
            "Stay calm. Please press the panic button if you feel unsafe."
        ]
        return random.choice(responses)

    elif "unsafe" in text or "afraid" in text:
        responses = [
            "I hear you. Stay in a well-lit public area. Should I notify local authorities?",
            "Please don’t panic. I can share your live location with your emergency contact.",
            "Consider pressing the panic button if you feel threatened 🚨."
        ]
        return random.choice(responses)

    elif "help" in text:
        return "I’m here to help. Do you need directions, or should I connect to emergency services?"

    else:
        return "I’m not sure I understand. You can say things like: 'I am lost' or 'I feel unsafe'."
