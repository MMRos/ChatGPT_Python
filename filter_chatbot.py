import openai
import os
import spacy
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

previous_questions = []
previous_answers = []
spacy_model = spacy.load("es_core_news_md")
banned_words = ["madrid", "word2"]


def filter_black_list(text, black_list):
    token = spacy_model(text)
    result = []

    for t in token:
        if t.text.lower() not in black_list:
            result.append(t.text)
        else:
            result.append("[xxxxx]")

    return " ".join(result)


def ask_chat_gpt(user_input, model="gpt-3.5-turbo"):
    # Build the list of content and roles
    messages = [
        {"role": "user", "content": user_input}
    ]

    answer = openai.chat.completions.create(
        model=model,
        messages=messages,  # Use list of messages
        max_tokens=100,
        temperature=0.5,
    )
    not_controlled_answers = answer.choices[0].message.content
    controlled_answer = filter_black_list(not_controlled_answers, banned_words)
    return controlled_answer


print("Welcome to our chatbot. Write exit to escape.")

while True:
    historical_conversation = ""
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break

    for question, answer in zip(previous_questions, previous_answers):
        historical_conversation += f"User asks: {question}\n"
        historical_conversation += f"Chatgpt answers: {answer}\n"

    prompt = f"User asks: {user_input}\n"
    historical_conversation += prompt
    gpts_answer = ask_chat_gpt(historical_conversation)
    print(f"{gpts_answer}")

    previous_questions.append(user_input)
    previous_answers.append(gpts_answer)
