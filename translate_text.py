import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def translate_text(text, language):
    prompt = [
        {"role": "user", "content": f"Translate text '{text}' to {language}."}
    ]
    answer = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        n=1,
        temperature=0.5,
    )

    return answer.choices[0].message.content


my_text = input("Input the text to translate: ")
my_language = input("What language do you want that text translated to? ")
translation = translate_text(my_text, my_language)
print(translation)