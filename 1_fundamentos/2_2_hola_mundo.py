from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar el modelo con Gemini 2.5 Flash
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Crear prompt
prompt = PromptTemplate(
    input_variables=["nombre"],
    template="""¡Hola {nombre}! 🌟

Qué lindo nombre tienes. Déjame decirte algo especial sobre él:

Explica de forma amigable y breve (máximo 3 líneas):
- El significado del nombre {nombre}
- Su origen cultural
- Una curiosidad interesante

Termina con un mensaje positivo relacionado con el significado del nombre."""
)

# Crear cadena
cadena = prompt | llm

# Solicitar nombre del usuario
print("=== BIENVENIDO AL DESCUBRIDOR DE NOMBRES ===\n")
nombre_usuario = input("¿Cómo te llamas? ")

# Generar respuesta
print("\n🤖 Generando tu mensaje personalizado con Gemini 2.5 Flash...\n")
resultado = cadena.invoke({"nombre": nombre_usuario})
print(resultado.content)