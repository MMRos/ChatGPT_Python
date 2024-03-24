import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def feeling_assesment(text):
    prompt = [
        {"role": "user", "content": f"Please, analize the main feeling in this text: '{text}'. "
                                    f"The feeling is: ."}
    ]
    answer = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        n=1,
        max_tokens=100,
        temperature=0.5,
    )

    return answer.choices[0].message.content

text_to_analize = input("Input a text: ")
feeling = feeling_assesment(text_to_analize)
print(feeling)

