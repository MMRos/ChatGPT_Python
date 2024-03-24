import os
import openai
import spacy
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

model = "gpt-3.5-turbo-0613"
prompt = "Tell me a story about visiting a European contry."

# Change to use chat endpoing
answer = openai.chat.completions.create(
    model=model,
    messages=[{"role": "system", "content": "You are a usefull assistant."},
              {"role": "user", "content": prompt}],
    temperature=0.1,
    n=1,
    max_tokens=100
)
# n gives the number of responses, temperature is how creative it is from 0.1-1, max_tokens are the values it gives (letters in this
# case)
# If we set n=3, this allows us to call 3 options and print them
# for idx, option in enumerate(response.choices):
# generated_text = option.message.content.strip()
# print(f"Response {idx + 1}: {generated_text}\n")

generated_text = answer.choices[0].message.content
print(generated_text)

print("*******************")

spacy_model = spacy.load("es_core_news_md")
analisis = spacy_model(generated_text)

# for token in analysis:
#     print(token.text, token.pos_, token.dep_, token.head.text)
# # text shows us the word (word by word), pos tells us what it is, dep the relationship, and head what it is related to.

# for ent in analysis.ents:
#     print(ent.text, ent.label_)
# Shows us what kind of entities there are (people, animals, miscellaneous, locations...)

# With the following, we will locate places and create new prompts that delve into it

location = None

for ent in analisis.ents:
    if ent.label_ == "LOC":
        location = ent
        break

if location:
    prompt2 = f"Tell me more about {location}"
    answer2 = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "You are a usefull assistant."},
                  {"role": "user", "content": prompt2}],
        temperature=0.1,
        n=1,
        max_tokens=100
    )
    print(answer2.choices[0].message.content)
