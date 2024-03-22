import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def analizar_sentimientos(texto):
    prompt = [
        {"role": "user", "content": f"Por favor, analiza el sentimiento predominante en el siguiente texto: '{texto}'. "
                                    f"El sentimiento es: ."}
    ]
    respuesta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        n=1,
        max_tokens=100,
        temperature=0.5,
    )

    return respuesta.choices[0].message.content

texto_para_analizar = input("Ingresa un texto: ")
sentimiento = analizar_sentimientos(texto_para_analizar)
print(sentimiento)
