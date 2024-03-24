import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def create_content(topic, tokens, temperature, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "You are a very usefull assistant."},
        {"role": "user", "content": f"Please, write a short article about: {topic}"}
    ]
    answer = openai.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=tokens,
        temperature=temperature
    )
    return answer.choices[0].message.content


def summarize(text, tokens, temperature, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "You are a very usefull assistant."},
        {"role": "user", "content": f"Please, summarize this topic: {text}\n\n"}
    ]
    answer = openai.chat.completions.create(
        model=model,
        messages=messages,
        n=1,
        max_tokens=tokens,
        temperature=temperature
    )
    return answer.choices[0].message.content

topic = input("Choose a topic: ")
tokens = int(input("How many tokens must the article have? "))
temperature = int(input("In a scale of 1 to 10, how creative do you want the article to be? ")) / 10
created_article = create_content(topic, tokens, temperature)
print(created_article)

original = input("Paste here the text: ")
tokens = int(input("How many tokens should have the summary as a maximum? "))
temperature = int(input("In a scale of 1 to 10, how creative do you want the summary to be? ")) / 10
summary = summarize(original, tokens, temperature)
print(summary)