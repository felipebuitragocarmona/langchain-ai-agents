from dotenv import load_dotenv

load_dotenv()

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
def calculadora(a: int, b: int, operacion: str) -> int:
    """
    Realiza operaciones matemáticas básicas.
    operacion: 'suma', 'resta', 'multiplicacion', 'division'
    """
    if operacion == "suma":
        return a + b
    if operacion == "resta":
        return a - b
    if operacion == "multiplicacion":
        return a * b
    if operacion == "division":
        return a / b
    raise ValueError("Operación no soportada")


tools = [calculadora]

# 3️⃣ Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente que puede usar herramientas para calcular. "
     "Usa la herramienta SOLO si es necesario."),
    ("human", "{input}")
])

# 4️⃣ Cadena con tools
agent_chain = prompt | llm.bind_tools(tools)

# 5️⃣ Ejecutar primera vez
pregunta = "¿Cuánto es 5 mas 4 ?"
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

    # Ejecutar la herramienta
    resultado = calculadora.invoke(tool_call['args'])
    print(f"   Resultado: {resultado}")

    # Agregar resultado al historial
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