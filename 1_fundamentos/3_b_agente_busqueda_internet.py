from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# 1️⃣ LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 2️⃣ Herramienta de búsqueda
search = DuckDuckGoSearchRun()


@tool
def buscar_internet(query: str) -> str:
    """Busca información actualizada en internet."""
    try:
        resultado = search.run(query)
        return resultado
    except Exception as e:
        return f"Error al buscar: {str(e)}"


tools = [buscar_internet]
llm_con_tools = llm.bind_tools(tools)


# 3️⃣ Función para ejecutar el agente
def agente_con_busqueda(pregunta: str):
    print(f"PREGUNTA: {pregunta}\n")
    print("=" * 60)

    mensajes = [HumanMessage(content=pregunta)]

    max_iteraciones = 5
    for i in range(max_iteraciones):
        response = llm_con_tools.invoke(mensajes)
        mensajes.append(response)

        # Si no hay tool calls, terminamos
        if not response.tool_calls:
            print("\n" + "=" * 60)
            print("RESPUESTA FINAL:")
            print(response.content)
            break

        # Ejecutar cada tool call
        for tool_call in response.tool_calls:
            print(f"\n🔍 Buscando: {tool_call['args']['query']}")
            resultado = buscar_internet.invoke(tool_call['args'])
            print(f"✅ Resultados obtenidos ({len(resultado)} caracteres)")

            mensajes.append(ToolMessage(
                content=str(resultado),
                tool_call_id=tool_call['id']
            ))


# 4️⃣ Probar con diferentes preguntas
preguntas = [
    "cual es el clima en manizales colombia para hoy y probabilidad de lluvia? en grados centigrados"
    #"¿Cuál es el precio actual del dólar en Colombia?",
    #"¿Qué pasó hoy en las noticias de tecnología?",
    #"¿Quién ganó el último partido de la selección Colombia?"
]

for pregunta in preguntas:
    agente_con_busqueda(pregunta)
    print("\n" + "=" * 80 + "\n")