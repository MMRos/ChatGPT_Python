import os
import openai
import spacy
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

modelo = "gpt-3.5-turbo-0613"
prompt = "Cuenta una historia breve sobre un viaje a un país Europeo"

# Cambiar a utilizar el endpoint de chat
respuesta = openai.chat.completions.create(
    model=modelo,
    messages=[{"role": "system", "content": "Tú eres un asistente muy útil."},
              {"role": "user", "content": prompt}],
    temperature=0.1,
    n=1,
    max_tokens=100
)
# n da número de respuestas, temperature es qué tan creativo es 0.1-1, max_tokens son los valores que da (letras en este
# caso)

# Si ponemos n=3 esto nos permite llamar 3 opciones e imprimirlas
# for idx, opcion in enumerate(respuesta.choices):
#     texto_generado = opcion.message.content.strip()
#     print(f"Respuesta {idx + 1}: {texto_generado}\n")

texto_generado = respuesta.choices[0].message.content
print(texto_generado)

print("*******************")

modelo_spacy = spacy.load("es_core_news_md")
analisis = modelo_spacy(texto_generado)

# for token in analisis:
#     print(token.text, token.pos_, token.dep_, token.head.text)
# # text nos muestra la palabra (por palabra), pos nos dice qué es, dep la relación y head con qué se relaciona.

# for ent in analisis.ents:
#     print(ent.text,ent.label_)
# Nos muestra qué tipo de entidades hay (personas, animales, miscelánea, ubicaciones...)


# Con lo siguiente localizaremos ubicaciones y realizaremos prompts nuevos que se adentren en ello
ubicacion = None

for ent in analisis.ents:
    if ent.label_ == "LOC":
        ubicacion = ent
        break

if ubicacion:
    prompt2 = f"Dime más acerca de {ubicacion}"
    respuesta2 = openai.chat.completions.create(
        model=modelo,
        messages=[{"role": "system", "content": "Tú eres un asistente muy útil."},
                  {"role": "user", "content": prompt2}],
        temperature=0.1,
        n=1,
        max_tokens=100
    )
    print(respuesta2.choices[0].message.content)
