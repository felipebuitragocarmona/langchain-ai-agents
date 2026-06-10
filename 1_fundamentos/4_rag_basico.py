from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1️⃣ Documentos
docs = [
    Document(page_content="Python es un lenguaje de programación."),
    Document(page_content="LangChain es un framework para LLMs."),
]

# 2️⃣ Vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3️⃣ LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

# 4️⃣ Prompt RAG
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Responde SOLO con la información del CONTEXTO. "
     "Si no sabes, di: 'No lo sé con la información disponible.'"),
    ("human",
     "PREGUNTA:\n{question}\n\nCONTEXTO:\n{context}\n\nRESPUESTA:")
])

# 5️⃣ Cadena RAG (LCEL puro)
rag_chain = (
    {
        "context": retriever,
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 6️⃣ Preguntar
respuesta = rag_chain.invoke({"question": "¿Qué es Python?"})
print(respuesta)
