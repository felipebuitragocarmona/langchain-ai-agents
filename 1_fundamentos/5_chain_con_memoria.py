from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Prompt (igual al tuyo)
template = """Eres un asistente amigable. Historial de conversación:
{history}

Humano: {input}
Asistente:"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

# Cadena nueva: Prompt -> LLM
chain = prompt | llm

# Almacén simple de historiales por sesión
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrapper con historial
conversacion = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Múltiples interacciones
respuestas = [
    "Hola, me llamo Carlos y tengo 25 años",
    "¿Cuál es mi nombre?",
    "¿Cuántos años tengo?",
    "Resume todo lo que sabes de mí"
]

session_id = "demo"  # cambia esto si quieres otra conversación independiente

for pregunta in respuestas:
    print(f"\n{'='*60}")
    print(f"PREGUNTA: {pregunta}")
    print(f"{'='*60}")

    resp = conversacion.invoke(
        {"input": pregunta},
        config={"configurable": {"session_id": session_id}}
    )

    # resp es un AIMessage
    print(f"RESPUESTA: {resp.content}")

# Ver historial almacenado
print(f"\n{'='*60}")
print("HISTORIAL COMPLETO EN MEMORIA:")
print(f"{'='*60}")

hist = get_history(session_id)
for msg in hist.messages:
    role = "Humano" if msg.type == "human" else "Asistente"
    print(f"{role}: {msg.content}")
