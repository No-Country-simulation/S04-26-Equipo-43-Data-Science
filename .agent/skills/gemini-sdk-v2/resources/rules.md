# Reglas Específicas: Gemini SDK v2

## Reglas de Implementación
1. **Importación Única**: Usar siempre `from google import genai`. No mezclar con el SDK antiguo.
2. **Configuración Tipada**: Utilizar `from google.genai import types` para construir los objetos de configuración.
3. **JSON Garantizado**: Siempre que se requiera una salida estructurada, definir un `response_schema` (preferiblemente Pydantic para mayor legibilidad en Python).
4. **Manejo de Errores**: Capturar `json.JSONDecodeError` y realizar una limpieza de los caracteres invisibles o bloques de Markdown si el modelo no respeta el formato (aunque con `response_schema` esto es raro).

## Tipos de Datos (SDK Mapping)
- `str` -> `STRING`
- `int` -> `INTEGER` / `NUMBER`
- `float` -> `NUMBER`
- `bool` -> `BOOLEAN`
- `list` -> `ARRAY`
- `dict` -> `OBJECT`
