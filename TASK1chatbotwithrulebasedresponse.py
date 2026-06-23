import re, random
from datetime import datetime

class ChatBot:
    def __init__(self):
        self.name = None
        self.topics = []
        self.kb = {
            "python": {
                "k": ["python", "programming", "coding"],
                "r": ["Python is beginner-friendly!", "Start with basics and practice!", "Python reads like English!"]
            },
            "loops": {
                "k": ["loop", "for", "while", "repeat"],
                "r": ["Loops repeat code for you!", "Use 'for' for fixed times, 'while' for conditions", "Loops save time and effort!"]
            },
            "functions": {
                "k": ["function", "def", "method"],
                "r": ["Functions are reusable code!", "Write once, use many times!", "Functions keep code organized!"]
            },
            "variables": {
                "k": ["variable", "store", "data"],
                "r": ["Variables hold data!", "Use meaningful names!", "Variables are containers for values!"]
            },
            "debugging": {
                "k": ["error", "bug", "crash"],
                "r": ["Read error messages!", "Use print() to track values!", "Break problem into pieces!"]
            },
            "datatypes": {
                "k": ["int", "string", "list", "dict"],
                "r": ["int, str, list, dict are main types!", "Choose right type for data!", "Different types for different needs!"]
            }
        }
    
    def chat(self, inp):
        inp_l = inp.lower()
        
        if re.search(r"\b(hi|hello|hey)\b", inp_l):
            n = re.search(r"(?:i'm|my name is|call me)\s+(\w+)", inp, re.I)
            if n and not self.name:
                self.name = n.group(1)
                return f"Hi {self.name}!  What would you like to learn?"
            return "Hello! Ask me about Python, loops, functions, variables, data types, or debugging!"
        
        if re.search(r"\b(bye|quit|exit)\b", inp_l):
            msg = f"Goodbye {self.name}! " if self.name else "Goodbye! Keep coding!"
            return msg
        
        if inp_l == "help":
            return "Ask about: Python, loops, functions, variables, data types, debugging. Commands: 'topics', 'quit'"
        
        if inp_l == "topics":
            return f"Topics: {', '.join(self.topics) if self.topics else 'None yet!'}"
        
        for topic, data in self.kb.items():
            if any(k in inp_l for k in data["k"]):
                if topic not in self.topics:
                    self.topics.append(topic)
                return random.choice(data["r"])
        
        return random.choice([
            "Can you rephrase that?",
            "Tell me more!",
            "Ask about Python topics!",
            "I didn't catch that!"
        ])

def main():
    print("\n" + "="*50)
    print("PYTHON CHATBOT")
    print("="*50)
    print("Ask about: Python, loops, functions, variables, data types, debugging")
    print("Commands: 'topics', 'help', 'quit'\n")
    
    bot = ChatBot()
    while True:
        try:
            u = input("You: ").strip()
            if not u: continue
            print(f"Bot: {bot.chat(u)}\n")
            if u.lower() in ["quit", "bye", "exit"]:
                break
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye!")
            break

if __name__ == "__main__":
    main()