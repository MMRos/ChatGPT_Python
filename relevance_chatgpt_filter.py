import openai
import os
import spacy
import numpy as np
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

previous_questions = []
previous_answers = []
spacy_model = spacy.load("es_core_news_md")
banned_words = ["madrid", "palabra2"]


def cosine_similarity(vec1, vec2):
    superposition = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    sim_cos = superposition / (magnitude1 * magnitude2)
    return sim_cos


def is_relevant(answer, entry, treshold=0.5):
    vectorized_entry = spacy_model(entry).vector
    vectorized_answer = spacy_model(answer).vector
    similarity = cosine_similarity(vectorized_entry, vectorized_answer)
    return similarity >= treshold


def black_list_filter(text, black_list):
    token = spacy_model(text)
    result = []

    for t in token:
        if t.text.lower() not in black_list:
            result.append(t.text)
        else:
            result.append("[xxxxx]")

    return " ".join(result)


def ask_chat_gpt(user_input, model="gpt-3.5-turbo"):
    # Build list with content and role
    messages = [
        {"role": "user", "content": user_input}
    ]

    answer = openai.chat.completions.create(
        model=model,
        messages=messages,  # Usar la lista de mensajes
        max_tokens=100,
        temperature=0.5,
    )
    uncontrolled_answers = answer.choices[0].message.content
    controlled_answers = black_list_filter(uncontrolled_answers, banned_words)
    return controlled_answers


print("Welcome to our chatbot. Write 'exit' to escape")

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
    gpt_answer = ask_chat_gpt(historical_conversation)

    relevant = is_relevant(gpt_answer, user_input)

    if relevant:
        print(f"{gpt_answer}")
        previous_questions.append(user_input)
        previous_answers.append(gpt_answer)
    else:
        print("Not relevant answer.")
