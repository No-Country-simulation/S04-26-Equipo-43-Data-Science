---
trigger: always_on
---

# 📜 Instrucciones de Comportamiento

Patrones de trabajo y convenciones del proyecto ConversaSense AI.

---

## Naming Conventions
- Todos los nombres de **variables, funciones, clases, archivos y directorios** deben estar en **INGLÉS**.
- La documentación y comentarios deben estar en **ESPAÑOL**.

### Variables y Funciones
- Variables: `snake_case` → `user_data`, `message_list`
- Funciones: `snake_case` → `get_frustration_score()`, `save_results()`
- Clases: `PascalCase` → `IngestAdapter`, `FeatureExtractor`
- Constantes: `SCREAMING_SNAKE_CASE` → `MAX_RETRIES`, `API_URL`

### Archivos y Directorios
- Directorios: `snake_case` → `core/`, `dashboard/`, `utils/`
- Archivos: `snake_case` → `ingest_adapter.py`, `logger.py`

### Comentarios
- En **español** (para legibilidad del equipo)
- Breves y directos
- Docstrings en funciones complejas siguiendo el estilo NumPy/Google (opcional pero recomendado).

---

## Logging Obligatorio

Usar el sistema de logs definido en `src/utils/logger.py`:

| Función | Uso |
|---------|-----|
| `log_debug()` | Detalles técnicos internos |
| `log_info()` | Información general |
| `log_sequence()` | Flujo de ejecución paso a paso |
| `log_warn()` | Situaciones inesperadas pero manejables |
| `log_error()` | Errores críticos |

---

## Estrategia de Validación

- ✅ **Validación de Schema**: Usar `pandera` para asegurar integridad de datos.
- ✅ **Logs**: Seguimiento exhaustivo del pipeline de 2M de mensajes.
- ✅ **Pruebas de Aceptación**: Ver `pruebas_aceptación.md` para criterios de éxito.

---

## Estructura de Código (Python)

### Imports
```python
# 1. Standard library imports
import os
import json

# 2. Third-party imports
import pandas as pd
import numpy as np

# 3. Local imports
from src.utils.logger import log_info, log_sequence
from src.core.preprocess import clean_text
```

### Funciones
```python
# Comentario breve del propósito
def calculate_score(data_frame):
    log_sequence('Calculando score', 'Iniciando proceso')
    
    # Lógica simple y modular
    result = data_frame['value'].mean()
    
    log_info(f'Score calculado: {result}')
    return result
```
