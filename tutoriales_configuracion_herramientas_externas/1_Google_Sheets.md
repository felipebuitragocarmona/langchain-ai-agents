## Paso a paso — Credenciales Google Sheets

---

### Paso 1 — Crear proyecto en Google Cloud

1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
2. Clic en el selector de proyectos (arriba a la izquierda)
3. **New Project** → ponle un nombre → **Create**

---

### Paso 2 — Habilitar Google Sheets API

1. En el menú lateral: **APIs & Services → Library**
2. Busca `Google Sheets API`
3. Clic en el resultado → **Enable**

---

### Paso 3 — Crear la Service Account

1. Ve a **APIs & Services → Credentials**
2. Clic en **+ Create Credentials → Service Account**
3. Ponle un nombre (ej: `agente-citas`)
4. Clic en **Create and Continue**
5. En el paso de roles selecciona **Editor** → **Continue → Done**

---

### Paso 4 — Descargar el JSON de credenciales

1. En la lista de Service Accounts, clic en la que acabas de crear
2. Ve a la pestaña **Keys**
3. **Add Key → Create new key → JSON → Create**
4. Se descarga automáticamente un archivo `.json`
5. Renómbralo `credentials.json` y ponlo en la raíz de tu proyecto

---

### Paso 5 — Crear el Google Sheet

1. Ve a [sheets.google.com](https://sheets.google.com)
2. Crea una hoja nueva
3. Ponle encabezados en la primera fila:

| A | B | C |
|---|---|---|
| nombre | apellido | tipo_cita |

4. Copia el **ID** de la URL:
```
https://docs.google.com/spreadsheets/d/  ESTE_ES_EL_ID  /edit
```

---

### Paso 6 — Compartir el Sheet con la Service Account

1. Abre el archivo `credentials.json` y busca el campo `client_email`:
```json
"client_email": "agente-citas@tu-proyecto.iam.gserviceaccount.com"
```
2. En tu Google Sheet: botón **Compartir**
3. Pega ese email → rol **Editor** → **Enviar**

---

### Paso 7 — Configurar el proyecto

Estructura de archivos:
```
mi_proyecto/
├── credentials.json   ← el que descargaste
├── .env
└── main.py
```

En tu `.env`:
```
GOOGLE_API_KEY=tu_clave_de_gemini
```

En tu `main.py` reemplaza:
```python
SPREADSHEET_ID = "ESTE_ES_EL_ID"  # el que copiaste en el paso 5
```

---

### Verificación rápida antes de correr el agente

```python
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
sheet = client.open_by_key("TU_SPREADSHEET_ID").sheet1
sheet.append_row(["Test", "Conexión", "OK"])
print("✅ Conexión exitosa")
```

Si ves la fila aparecer en el Sheet, todo está listo.