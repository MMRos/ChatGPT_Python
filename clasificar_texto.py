import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def clasificar_texto(texto):
    categorias = [
        "arte",
        "ciencia",
        "deportes",
        "economía",
        "educación",
        "entretenimiento",
        "medio ambiente",
        "política",
        "salud",
        "tecnología"
    ]

    prompt = [
        {"role": "user", "content": f"Por favor, clasifica el siguiente texto '{texto}' en una de estas categorías: "
                                    f"{','.join(categorias)}. La categoría es: "}
    ]
    respuesta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        n=1,
        max_tokens=50,
        temperature=0.5,
    )

    return respuesta.choices[0].message.content

texto_para_clasificar = input("Ingrese un texto: ")
clasificacion = clasificar_texto(texto_para_clasificar)
print(clasificacion)