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
GOOGLE_SHEETS_CREDENTIALS_FILE=credenciales/credentials_google_sheet.json
```

Ejemplo extendido (si pruebas más proveedores/herramientas):

```env
GOOGLE_API_KEY=tu_api_key_aqui
OPENAI_API_KEY=tu_openai_api_key_opcional
TAVILY_API_KEY=tu_tavily_api_key_opcional
GOOGLE_SHEETS_CREDENTIALS_FILE=credenciales/credentials_google_sheet.json
```

Nota: no subas tu archivo .env al repositorio.

## Credenciales de Google Sheets

La carpeta credenciales se versiona para que exista en el repositorio remoto, pero su contenido se ignora en Git.

Estructura recomendada:

```text
credenciales/
	.gitkeep
	credentials_google_sheet.json   # local, no versionado
```

Pasos:

1. Descarga tu JSON de Service Account desde Google Cloud.
2. Guárdalo como credenciales/credentials_google_sheet.json.
3. Asegura que GOOGLE_SHEETS_CREDENTIALS_FILE apunte a ese archivo en el .env.
4. Comparte la hoja de cálculo con el email de la Service Account.

Si ya subiste credenciales por error, quítalas del índice sin borrar tus archivos locales:

```bash
git rm -r --cached credenciales/*.json
git commit -m "remove tracked credentials"
```

## Ejecutar ejemplos

Desde la raíz del proyecto:

```bash
python 1_fundamentos/1_modelosDisponibles.py
python 1_fundamentos/2_1_primera_prueba.py
python 1_fundamentos/2_2_hola_mundo.py
python 1_fundamentos/3_a_agente_calculador.py
python 1_fundamentos/3_b_agente_busqueda_internet.py
python 1_fundamentos/3_c_clima.py
python 1_fundamentos/3_d_google_sheets.py
python 1_fundamentos/4_respuestas_estructuradas.py
python 1_fundamentos/5_chain_con_memoria.py
python 1_fundamentos/6_rag_basico.py
```

Si un script requiere variables adicionales, define esas claves en tu archivo .env antes de ejecutarlo.

## Orden de lectura recomendado (Fundamentos)

Sigue este orden para avanzar de lo básico a lo aplicado:

1. 1_fundamentos/1_modelosDisponibles.py
2. 1_fundamentos/2_1_primera_prueba.py
3. 1_fundamentos/2_2_hola_mundo.py
4. 1_fundamentos/3_a_agente_calculador.py
5. 1_fundamentos/3_b_agente_busqueda_internet.py
6. 1_fundamentos/3_c_clima.py
7. 1_fundamentos/3_d_google_sheets.py
8. 1_fundamentos/4_respuestas_estructuradas.py
9. 1_fundamentos/5_chain_con_memoria.py
10. 1_fundamentos/6_rag_basico.py
