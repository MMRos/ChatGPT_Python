import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def traducir_texto(texto, idioma):
    prompt = [
        {"role": "user", "content": f"Traduce el texto '{texto}' al {idioma}."}
    ]
    respuesta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        n=1,
        temperature=0.5,
    )

    return respuesta.choices[0].message.content


mi_texto = input("Ingresa el texto a traducir: ")
mi_idioma = input("¿A qué idioma lo quieres traducir? ")
traduccion = traducir_texto(mi_texto, mi_idioma)
print(traduccion)