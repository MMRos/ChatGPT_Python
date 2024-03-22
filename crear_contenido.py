import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def crear_contenido(tema, tokens, temperatura, modelo="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "Tú eres un asistente muy útil."},
        {"role": "user", "content": f"Por favor, escribe un artículo corto sobre el tema: {tema}"}
    ]
    respuesta = openai.chat.completions.create(
        model=modelo,
        messages=messages,
        max_tokens=tokens,
        temperature=temperatura
    )
    return respuesta.choices[0].message.content


def resumir_texto(texto, tokens, temperatura, modelo="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "Tú eres un asistente muy útil."},
        {"role": "user", "content": f"Por favor, resume el siguiente texto en español: {texto}\n\n"}
    ]
    respuesta = openai.chat.completions.create(
        model=modelo,
        messages=messages,
        n=1,
        max_tokens=tokens,
        temperature=temperatura
    )
    return respuesta.choices[0].message.content

tema = input("Escoja un tema para su artículo: ")
tokens = int(input("Cuántos tokens máximos tendrá tu artículo? "))
temperatura = int(input("Del 1 al 10, qué tan creativo quieres que sea tu artículo? "))/10
articulo_creado = crear_contenido(tema, tokens, temperatura)
print(articulo_creado)

original = input("Pega aquí el texto a resumir: ")
tokens = int(input("Cuántos tokens máximos tendrá tu resumen? "))
temperatura = int(input("Del 1 al 10, qué tan creativo quieres que sea tu resumen? "))/10
resumen = resumir_texto(original, tokens, temperatura)
print(resumen)