import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
# Configurar API key
os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY")



model = init_chat_model(
    model="google_genai:gemini-2.5-flash-lite",
    temperature=1,
)

response = model.invoke("Why do parrots talk?")
print(response)