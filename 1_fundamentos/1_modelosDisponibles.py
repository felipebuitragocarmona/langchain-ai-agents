import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
# Configurar API key
os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY")

# Configurar la biblioteca de Google
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Listar todos los modelos disponibles
print("=== MODELOS DISPONIBLES ===\n")
for modelo in genai.list_models():
    if 'generateContent' in modelo.supported_generation_methods:
        print(f"Nombre: {modelo.name}")
        print(f"Display: {modelo.display_name}")
        print(f"Descripción: {modelo.description}")
        print(f"Límite de tokens de entrada: {modelo.input_token_limit}")
        print(f"Límite de tokens de salida: {modelo.output_token_limit}")
        print("-" * 60)