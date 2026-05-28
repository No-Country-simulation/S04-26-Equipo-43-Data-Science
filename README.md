# ConversaSense AI: Arquitectura Híbrida para la Detección de Frustración y Retención Multilingüe

ConversaSense AI es una solución empresarial de **Online Cascade Learning** diseñada para ingestar, validar, clasificar y diagnosticar flujos conversacionales masivos (español y portugués) en CPU estándar, combinando una **Capa Rápida (LightGBM)** local con una **Capa Profunda (LLM Gemini)** a través de un enrutamiento por incertidumbre.

---

## 📁 Estructura Real del Proyecto

```
├── data/
│   ├── raw/                            # Entradas crudas (ej: nuevas_conversaciones.csv)
│   ├── processed/                      # inference_results.parquet para el Dashboard
│   └── dlq/                            # Dead Letter Queue (errores_ingesta.parquet)
├── models/
│   └── lgbm_model.pkl                  # Clasificador LightGBM entrenado (F1: 0.88)
├── src/
│   ├── core/                           # Núcleo de Procesamiento e IA
│   │   ├── ingest_adapter.py           # Ingesta resiliente y validación Pandera
│   │   ├── feature_extractor.py        # Extracción de 24 variables por mensaje
│   │   ├── feature_aggregator.py       # Agregación de 23 variables conversacionales
│   │   ├── frustration_classifier.py   # Clasificación binaria (LightGBM)
│   │   ├── cascade_orchestrator.py     # Orquestador del enrutamiento de incertidumbre
│   │   ├── truth_guardian.py           # LLM Second Pass con auditoría Twin-Pass
│   │   └── signal_dictionaries.py      # Regex y palabras clave (ES/PT)
│   ├── dashboard/                      # Visualización Científica (Reflex App)
│   │   └── dashboard/
│   │       └── dashboard.py            # Componentes, State y UI de Reflex
│   └── utils/
│       ├── logger.py                   # Logger unificado del sistema
│       └── prueba_definitiva.py        # Pipeline de ejecución ETL masivo
├── tests/
│   ├── test_model_s2.py                # Test de validación cruzada del LightGBM
│   └── stress_testing.py               # Suite integrada de stress tests (SLA/DLQ)
└── README.md
```

---

## 📥 Estándar de Conversaciones y Contrato de Datos

Cualquier archivo de entrada que deba procesar el pipeline ETL de ConversaSense AI debe respetar estrictamente el formato estructurado por conversación. 

### 1. El Contrato de Columnas
Ya sea un archivo **CSV** o **JSON**, debe contener obligatoriamente las siguientes columnas:

| Columna | Tipo de Dato | Validación | Descripción |
| :--- | :--- | :--- | :--- |
| **`id_conv`** | String / Object | Requerido, no nulo | Identificador único de la sesión o conversación (ej: `CONV_01`). |
| **`turno`** | Entero (int64) | $\ge 0$, Coercible | El orden correlativo del mensaje dentro de la sesión (ej: 1, 2, 3...). |
| **`rol`** | String | In-list: `['user', 'bot', 'system']` | Quién emite el mensaje. El adaptador normaliza roles automáticamente. |
| **`mensaje`** | String | Permite nulos (nullable) | El texto del mensaje. Si es nulo, el extractor le da tratamiento neutro. |

### 2. Validación de Esquema con Pandera
La ingesta está gobernada por `ConversationSchema` en [`ingest_adapter.py`](file:///C:/Users/opaye/Proyectos/SC/src/core/ingest_adapter.py). Antes de que los datos toquen el motor de Machine Learning, Pandera ejecuta validaciones de tipado estricto y de coherencia:
*   Fuerza la coerción de tipos (ej. strings que representen números en `turno` son convertidos a enteros).
*   Garantiza que el campo `rol` pertenezca estrictamente al conjunto cerrado.
*   En caso de que el archivo no cumpla con las columnas o la estructura estricta (`strict = True`), Pandera lanza un `SchemaErrors` que el adaptador captura.

### 3. Heurísticas de Normalización de Roles y UTF-8
Para garantizar flexibilidad ante fuentes externas heterogéneas, el `IngestAdapter`:
*   **Mapea Roles Dinámicamente**: Convierte sin fallar variaciones comunes de roles al estándar oficial:
    *   `usuario`, `customer`, `client` $\rightarrow$ **`user`**
    *   `asistente`, `assistant`, `agent` $\rightarrow$ **`bot`**
*   **Fuerza de Encoding**: Intenta abrir los archivos forzando codificación **UTF-8**, y en caso de error de caracteres de control de Windows, cae de forma resiliente a **Latin-1** para no interrumpir el flujo.

### 4. Aislamiento en Dead Letter Queue (DLQ)
Si un bloque de registros o filas específicas fallan en las validaciones de tipo o esquema de Pandera:
1.  El adaptador captura el error y extrae los registros corruptos.
2.  **No detiene el pipeline**: Guarda las filas fallidas en el archivo de mensajes muertos [`data/dlq/errores_ingesta.parquet`](file:///C:/Users/opaye/Proyectos/SC/data/dlq/).
3.  Agrega la columna `error_reason` indicando la validación exacta que falló (ej: *Error de coerción en turno de tipo str a int*) y el timestamp de ingesta para auditoría posterior.
4.  Permite que el pipeline prosiga procesando únicamente los registros limpios y validados.

---

## ⚙️ Ejecución del Pipeline Dinámico (ETL + Inferencia)

El pipeline de ejecución [`prueba_definitiva.py`](file:///C:/Users/opaye/Proyectos/SC/src/utils/prueba_definitiva.py) está diseñado para ser dinámico y procesar flujos de datos reales bajo demanda:

### 1. Inyectar nuevos diálogos
Coloca tu archivo CSV con conversaciones en la ruta:
[`data/raw/nuevas_conversaciones.csv`](file:///C:/Users/opaye/Proyectos/SC/data/raw/nuevas_conversaciones.csv) respetando las columnas estándar.

### 2. Ejecutar el Pipeline ETL
Corre el script en consola para ejecutar el flujo completo (Ingesta $\rightarrow$ Pandera $\rightarrow$ Extracción de 24 features $\rightarrow$ Agregación de 23 features $\rightarrow$ Inferencia en Cascada LightGBM/Gemini $\rightarrow$ Exportación):
```powershell
venv\Scripts\python.exe src/utils/prueba_definitiva.py
```
*Si no existe el archivo personalizado, el pipeline se ejecutará de forma automática con el dataset de prueba de 8 casos por defecto.*

### 3. Verificar en el Dashboard
El archivo resultante se exportará a [`inference_results.parquet`](file:///C:/Users/opaye/Proyectos/SC/data/processed/inference_results.parquet). La aplicación Reflex recargará los datos al instante, permitiéndote navegar y auditar las intenciones, métricas y diálogos reales de forma interactiva en la UI.

---

## 🧪 Pruebas de Estrés
Para certificar la robustez del sistema, dispones de una suite de estrés que evalúa los límites de memoria, volumen y control de fallas:
```powershell
venv\Scripts\python.exe tests/stress_testing.py
```
Este comando corre:
1.  **Test 1 (Volumen/SLA)**: 1,000 conversaciones procesadas en 25 segundos en un solo hilo de CPU.
2.  **Test 2 (Casos Edge)**: Ingesta de DataFrames vacíos e inputs malformados (nulos, solo bot o solo usuario).
3.  **Test 3 (Datos Corruptos/DLQ)**: Ingesta de 900 registros corruptos para validar el desvío automático al DLQ.
