import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

preguntas_anteriores = []
respuestas_anteriores = []


def preguntar_chat_gpt(ingreso_usuario, modelo="gpt-3.5-turbo"):
    # Construir la lista de mensajes con el rol y el contenido adecuados
    mensajes = [
        {"role": "system", "content": "Tú eres un asistente muy útil."},
        {"role": "user", "content": ingreso_usuario}
    ]

    respuesta = openai.chat.completions.create(
        model=modelo,
        messages=mensajes,  # Usar la lista de mensajes
        max_tokens=100,
        temperature=0.5,
    )
    # Acceder correctamente a los elementos de la respuesta
    return respuesta.choices[0].message.content

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
