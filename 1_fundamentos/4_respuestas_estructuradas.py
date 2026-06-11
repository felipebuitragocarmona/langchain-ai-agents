from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1️⃣ Modelo Pydantic (contrato de salida)
class Persona(BaseModel):
    nombre: str = Field(description="Nombre de la persona")
    edad: int = Field(description="Edad en años")
    ciudad: str = Field(description="Ciudad de residencia")

# 2️⃣ Parser JSON
parser = JsonOutputParser(pydantic_object=Persona)

# 3️⃣ LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# 4️⃣ Prompt (incluye instrucciones del parser)
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Extrae la información solicitada y responde SOLO en el formato JSON indicado.\n"
     "{format_instructions}"),
    ("human", "{input}")
])

# 5️⃣ Cadena completa
chain = (
    prompt
    | llm
    | parser
)

# 6️⃣ Ejecutar
texto = "Qué dia es hoy?"

resultado = chain.invoke({
    "input": texto,
    "format_instructions": parser.get_format_instructions()
})

print(resultado)
print(type(resultado))
