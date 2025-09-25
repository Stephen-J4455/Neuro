import os
import re
from huggingface_hub import InferenceClient


class NeuroAi:
    def __init__(self):
        self.patterns = [
            (re.compile(r"\b(who are you|who are u)\b", re.I),[
                "I am Neuro, a SMART ENTITY for LEARNING, MANAGEMENT and ASSISTANCE, a Ghanaian startup headquartered in The University of Professional Studies Accra."
            ]),
            (re.compile(r"\b(who created you|who created u)\b", re.I),[
                "I was developed by Stephen J. Amuzu, a Ghanaian software engineer and entrepreneur, as part of a project to create an AI assistant for learning and management."
            ])
        ]
        # Hugging Face client
        hf_token = os.environ.get("HF_TOKEN")
        self.hf_client = InferenceClient(token=hf_token) if hf_token else None

    def ask(self, prompt, history=[]):
        if not self.hf_client:
            return "Hugging Face API is not configured."

        messages = []
        for message in history:
            if message.get('sender') == 'user':
                messages.append({'role': 'user', 'content': message.get('text')})
            elif message.get('sender') == 'ai':
                messages.append({'role': 'assistant', 'content': message.get('text')})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.hf_client.chat.completions.create(
                model="Qwen/Qwen3-Next-80B-A3B-Instruct",
                messages=messages,
                max_tokens=2048 # Lowered to reduce memory usage
            )
            content = response.choices[0].message.content
            print(f"[DEBUG] Hugging Face response length: {len(content) if content else 0}")
            if content and len(content) < 3500:
                print("[DEBUG] Response may be incomplete or truncated:", content)
            return content
        except Exception as e:
            print(f"[DEBUG] Hugging Face API error: {e}")
            return f"Error with Hugging Face API: {e}"

    def chat(self):
        print("SELMA: Hi! I'm your personal chat assistant. What would you like to do?")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                response = self.ask(user_input)
                print(f"SELMA: {response}")
            except KeyboardInterrupt:
                print("\nSELMA: Goodbye!")
                break
            except Exception as e:
                print(f"SELMA: Oops! Error: {e}")


if __name__ == "__main__":
    bot = NeuroAi()
    bot.chat()