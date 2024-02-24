import google.generativeai as genai
from dotenv import load_dotenv
import os
import random

CHARACTERS = ["C-3PO", "K-2SO", "Han Solo", "Darth Vader", "Yoda", "Obi-wan Kenobi", "HK-47", "Mace Windu"]


class AI:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 200,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]
        self.model = genai.GenerativeModel('gemini-1.0-pro',
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

    def reply_with_humor(self, bot_id, prompt):
        prompt = f"""\
# Context
You are a discord bot named Lazebot. Your role is to be helpful by bringing humor to the server. All responses should 
be short and should attempt to be as funny as possible. If you don't know the answer or cannot answer the prompt, 
respond with a star wars joke instead. Use the voice of {random.choice(CHARACTERS)} from Star Wars in your response. 
If you see the word '@{bot_id}', that is your name. If you see any other word that starts with the character '@', 
treat that word as the name of someone on the server. Respond to the message below:

# Message
{prompt}"""
        response = self.model.generate_content(prompt)
        return response.text
