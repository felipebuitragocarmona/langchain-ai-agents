from dotenv import load_dotenv
load_dotenv()

import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, ToolMessage

# 1️⃣ LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# 2️⃣ Tool
@tool
def obtener_clima_por_ciudad(ciudad: str) -> str:
    """Obtiene el clima actual dado el nombre de una ciudad."""

    # Geocodificación
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1, "language": "es"}
    ).json()

    result = geo["results"][0]
    lat, lon = result["latitude"], result["longitude"]

    # Clima actual
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "windspeed_10m", "relative_humidity_2m"],
            "timezone": "auto"
        }
    ).json()

    current = clima["current"]
    return (
        f"{result['name']}, {result['country']}: "
        f"{current['temperature_2m']}°C, "
        f"humedad {current['relative_humidity_2m']}%, "
        f"viento {current['windspeed_10m']} km/h"
    )


tools = [obtener_clima_por_ciudad]

# 3️⃣ Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente que puede consultar el clima de cualquier ciudad. "
     "Usa la herramienta SOLO si es necesario."),
    ("human", "{input}")
])

# 4️⃣ Cadena con tools
agent_chain = prompt | llm.bind_tools(tools)

# 5️⃣ Ejecutar primera vez
pregunta = "¿Cómo está el clima en Roma?"
print(f"PREGUNTA: {pregunta}\n")

response = agent_chain.invoke({"input": pregunta})

print("=" * 60)
print("PRIMERA RESPUESTA DEL MODELO:")
print(f"Tool calls: {response.tool_calls}")

# 6️⃣ Ejecutar las herramientas solicitadas
mensajes = [HumanMessage(content=pregunta)]
mensajes.append(response)

for tool_call in response.tool_calls:
    print(f"\n🔧 Ejecutando: {tool_call['name']}")
    print(f"   Argumentos: {tool_call['args']}")

    resultado = obtener_clima_por_ciudad.invoke(tool_call['args'])
    print(f"   Resultado: {resultado}")

    mensajes.append(ToolMessage(
        content=str(resultado),
        tool_call_id=tool_call['id']
    ))

# 7️⃣ Segunda llamada con los resultados
print("\n" + "=" * 60)
print("OBTENIENDO RESPUESTA FINAL...\n")

llm_con_tools = llm.bind_tools(tools)
respuesta_final = llm_con_tools.invoke(mensajes)

print("=" * 60)
print("RESPUESTA FINAL:")
print(respuesta_final.content)