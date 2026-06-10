from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

# ─────────────────────────────────────────
# 1️⃣ LLM
# ─────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ─────────────────────────────────────────
# 2️⃣ Tool
# ─────────────────────────────────────────
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1gZ71oPD1DoF7qXeld4EeDaQFX24PU1GlJJhjJASudwo"


def obtener_ruta_credenciales() -> Path:
    """Resuelve la ruta del JSON de credenciales de forma robusta."""
    base_dir = Path(__file__).resolve().parent

    ruta_env = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
    if ruta_env:
        ruta = Path(ruta_env)
        if not ruta.is_absolute():
            ruta = (base_dir / ruta).resolve()
        if ruta.exists():
            return ruta

    candidatos = [
        base_dir.parent / "credenciales" / "credentials_google_sheet.json",
        base_dir.parent / "credenciales" / "credentials.json",
    ]

    for ruta in candidatos:
        if ruta.exists():
            return ruta

    rutas_texto = "\n".join(f"- {r}" for r in candidatos)
    raise FileNotFoundError(
        "No se encontró el archivo de credenciales de Google Sheets. "
        "Define GOOGLE_SHEETS_CREDENTIALS_FILE en el .env o crea uno de estos archivos:\n"
        f"{rutas_texto}"
    )

@tool
def registrar_cita(nombre: str, apellido: str, tipo_cita: str) -> str:
    """
    Registra una cita médica en Google Sheets.
    Recibe nombre, apellido y tipo de cita del paciente.
    """
    ruta_credenciales = obtener_ruta_credenciales()
    creds = Credentials.from_service_account_file(str(ruta_credenciales), scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    sheet.append_row([nombre, apellido, tipo_cita])
    return f"✅ Cita registrada: {nombre} {apellido} — {tipo_cita}"

tools = [registrar_cita]
llm_con_tools = llm.bind_tools(tools)

# ─────────────────────────────────────────
# 3️⃣ Historial con system prompt fijo
# ─────────────────────────────────────────
historial = [
    SystemMessage(content="""Eres un asistente de agenda médica.
Cuando el usuario solicite una cita, extrae:
- nombre
- apellido
- tipo de cita (ej: medicina general, odontología, cardiología)

Luego usa la herramienta para registrarla.
Si falta algún dato, pregúntalo antes de usar la herramienta.
Después de registrar, pregunta si desea agendar otra cita.""")
]

# ─────────────────────────────────────────
# 4️⃣ Ciclo infinito
# ─────────────────────────────────────────
print("🏥 Asistente de citas médicas (escribe 'salir' para terminar)\n")

while True:

    # Input del usuario
    entrada = input("Tú: ").strip()
    if entrada.lower() in ["salir", "exit", "quit"]:
        print("👋 Hasta luego.")
        break

    # Agregar mensaje del usuario al historial
    historial.append(HumanMessage(content=entrada))

    # Llamada al LLM
    response = llm_con_tools.invoke(historial)
    historial.append(response)

    # Si el modelo quiere usar una tool
    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"\n🔧 Registrando cita...")
            resultado = registrar_cita.invoke(tool_call['args'])
            print(f"   {resultado}\n")

            historial.append(ToolMessage(
                content=str(resultado),
                tool_call_id=tool_call['id']
            ))

        # Segunda llamada para que el modelo responda al usuario
        respuesta_final = llm_con_tools.invoke(historial)
        historial.append(respuesta_final)
        print(f"Asistente: {respuesta_final.content}\n")

    else:
        # Respuesta directa sin tool
        print(f"Asistente: {response.content}\n")