import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

previous_questions = []
previous_answers = []


def ask_chat_gpt(user_input, model="gpt-3.5-turbo"):
    # Build a list with role and messages
    messages = [
        {"role": "system", "content": "You are a very usefull assistant"},
        {"role": "user", "content": user_input}
    ]

    answer = openai.chat.completions.create(
        model=model,
        messages=messages,  # Use list of messages
        max_tokens=100,
        temperature=0.5,
    )
    # Access to the list of answers
    return answer.choices[0].message.content

print("Welcome to our chatbot. Write exit to escape.")

while True:
    historical_conversation = ""
    user_input = input("\nTú: ")
    if user_input.lower() == "exit":
        break

    for question, answer in zip(previous_questions, previous_answers):
        historical_conversation += f"User asks: {question}\n"
        historical_conversation += f"Chatgpt answers: {answer}\n"

    prompt = f"User asks: {user_input}\n"
    historical_conversation += prompt
    gpt_answer = ask_chat_gpt(historical_conversation)
    print(f"{gpt_answer}")

    previous_questions.append(user_input)
    previous_answers.append(gpt_answer)
