import os
import random

class MessageManager:
    def __init__(self, filepath='data/messages.txt'):
        self.filepath = filepath

    def load_messages(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def save_message(self, message):
        messages = self.load_messages()
        messages.append(message)
        with open(self.filepath, "w", encoding="utf-8") as f:
            for msg in messages:
                f.write(msg + "\n")
    
    def delete_message(self, message_to_delete):
        messages = self.load_messages()
        messages = [msg for msg in messages if msg != message_to_delete]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for msg in messages:
                f.write(msg + '\n')
    
    def get_random_message(self):
        messages = self.load_messages()
        if messages:
            return random.choice(messages)
        else:
            return "¡Feliz cumpleaños!"
