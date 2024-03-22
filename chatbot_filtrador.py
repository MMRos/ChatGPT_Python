import openai
import os
import spacy
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

preguntas_anteriores = []
respuestas_anteriores = []
modelo_spacy = spacy.load("es_core_news_md")
palabras_prohibidas = ["madrid", "palabra2"]


def filtrar_lista_negra(texto, lista_negra):
    token = modelo_spacy(texto)
    resultado = []

    for t in token:
        if t.text.lower() not in lista_negra:
            resultado.append(t.text)
        else:
            resultado.append("[xxxxx]")

    return " ".join(resultado)


def preguntar_chat_gpt(ingreso_usuario, modelo="gpt-3.5-turbo"):
    # Construir la lista de mensajes con el rol y el contenido adecuados
    mensajes = [
        {"role": "user", "content": ingreso_usuario}
    ]

    respuesta = openai.chat.completions.create(
        model=modelo,
        messages=mensajes,  # Usar la lista de mensajes
        max_tokens=100,
        temperature=0.5,
    )
    respuesta_sin_controlar = respuesta.choices[0].message.content
    respesta_controlada = filtrar_lista_negra(respuesta_sin_controlar,palabras_prohibidas)
    return respesta_controlada


print("Bienvenido a nuestro chatbot básico. Escribe 'salir' cuando quieras terminar.")

while True:
    conversacion_historica = ""
    ingreso_usuario = input("\nTú: ")
    if ingreso_usuario.lower() == "salir":
        break

    for pregunta, respuesta in zip(preguntas_anteriores, respuestas_anteriores):
        conversacion_historica += f"El usuario pregunta: {pregunta}\n"
        conversacion_historica += f"Chatgpt responde: {respuesta}\n"

    prompt = f"El usuario pregunta: {ingreso_usuario}\n"
    conversacion_historica += prompt
    respuesta_gpt = preguntar_chat_gpt(conversacion_historica)
    print(f"{respuesta_gpt}")

    preguntas_anteriores.append(ingreso_usuario)
    respuestas_anteriores.append(respuesta_gpt)
