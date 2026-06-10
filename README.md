# Fundamentos de Programación Agéntica con LangChain y LangGraph

Repositorio práctico para aprender y experimentar con agentes de IA usando LangChain y LangGraph en Python.

El objetivo es construir bases sólidas en:

- Modelos y cadenas (chains)
- Memoria conversacional
- RAG básico
- Uso de herramientas (tool calling)
- Diseño de agentes reflexivos
- Manejo de estados y flujos con grafos

## Estructura del proyecto

- 1_fundamentos/: ejercicios introductorios y progresivos

## Requisitos

- Python 3.10 o superior
- pip actualizado
- Una API key de proveedor LLM (por ejemplo, Google Gemini)

## Instalación

1. Clona el repositorio y entra al directorio del proyecto.
2. Crea un entorno virtual.
3. Activa el entorno virtual.
4. Instala las dependencias.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requeriments.txt
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requeriments.txt
```

## Configuración de variables de entorno

Crea un archivo .env en la raíz del proyecto.

Ejemplo mínimo:

```env
GOOGLE_API_KEY=tu_api_key_aqui
```

Ejemplo extendido (si pruebas más proveedores/herramientas):

```env
GOOGLE_API_KEY=tu_api_key_aqui
OPENAI_API_KEY=tu_openai_api_key_opcional
TAVILY_API_KEY=tu_tavily_api_key_opcional
```

Nota: no subas tu archivo .env al repositorio.

## Ejecutar ejemplos

Desde la raíz del proyecto:

```bash
python 1_fundamentos/2_2_hola_mundo.py
python 1_fundamentos/3_chain_con_memoria.py
python 1_fundamentos/4_rag_basico.py
python 1_fundamentos/5_a_agente_calculador.py
```

Si un script requiere variables adicionales, define esas claves en tu archivo .env antes de ejecutarlo.
