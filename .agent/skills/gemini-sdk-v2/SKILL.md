---
name: gemini-sdk-v2
description: Experto en el uso del SDK v2 de Google GenAI para modelos Gemini.
---

# Skill: gemini-sdk-v2

## Propósito
Este skill proporciona instrucciones y patrones de diseño para interactuar de forma robusta con la API de Gemini utilizando el SDK `google-genai` (v2). Se especializa en la generación de contenido estructurado (JSON) y la configuración avanzada de modelos.

## Cuándo Usar
- Al implementar o actualizar llamadas a modelos Gemini en Python.
- Cuando se requiere que el modelo responda estrictamente en formato JSON.
- Para configurar parámetros como temperatura, esquemas de respuesta y límites de tokens.

## Instrucciones
1. **Inicialización**: Usar `client = genai.Client(api_key=...)`.
2. **Definición de Esquema**: Crear una clase Pydantic que herede de `BaseModel` para definir la estructura de salida.
3. **Configuración**: Instanciar `types.GenerateContentConfig` pasando `response_mime_type='application/json'` y el esquema en `response_schema`.
4. **Ejecución**: Llamar a `client.models.generate_content`.
5. **Procesamiento**: Acceder a `response.text` y convertir a dict usando `json.loads()`.

## Ejemplos
Ver carpeta `examples/ejemplo_basico.md` para una implementación de clasificación de sentimientos.

## Resources
- `resources/knowledge-source.md`: Documentación oficial procesada.
- `resources/rules.md`: Reglas de mapeo de tipos y mejores prácticas.

## Solución de Problemas
- **Error 'Unterminated string'**: Asegurarse de estar usando `response_schema`. Si persiste, limpiar la respuesta eliminando bloques de Markdown (```json ... ```).
- **Atributos faltantes en el objeto Model**: En v2, los atributos han cambiado. Consultar `resources/knowledge-source.md` para la sintaxis de listado de modelos.

## Logs
- LOG_INFO: "gemini-sdk-v2: Generando contenido estructurado con el modelo [nombre-modelo]"
- LOG_INFO: "gemini-sdk-v2: Respuesta recibida y validada exitosamente"
