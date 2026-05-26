---
name: minilm-embeddings
description: Experto en el modelo de embeddings paraphrase-multilingual-MiniLM-L12-v2 para NLU multilingüe.
---

# Skill: minilm-embeddings

## Propósito
Este skill proporciona conocimiento técnico y patrones de implementación para el modelo `paraphrase-multilingual-MiniLM-L12-v2`. Se centra en su uso para el cálculo de similitud semántica, detección de coherencia en diálogos y clasificación rápida de sentimientos en entornos multilingües (ES/PT).

## Cuándo Usar
- Al implementar lógica de comparación de textos en el pipeline de datos.
- Para optimizar la velocidad de procesamiento de grandes volúmenes de conversaciones (ETL).
- Cuando se requiere soporte nativo para múltiples idiomas sin traducción previa.

## Instrucciones
1. **Inicialización**: Usar `SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')`.
2. **Pre-procesamiento**: Limpiar ruidos básicos (emojis, links) si es necesario, aunque el modelo es robusto.
3. **Encoding**: Usar `model.encode()` preferiblemente en lotes (batch processing) para mayor eficiencia.
4. **Validación**: Utilizar los umbrales definidos en `resources/rules.md` para clasificar la calidad de las respuestas.

## Ejemplos
Ver carpeta `examples/ejemplo_basico.md` para el cálculo de coherencia en diálogos.

## Resources
- `resources/knowledge-source.md`: Especificaciones técnicas y comparativa de rendimiento.
- `resources/rules.md`: Reglas de implementación y umbrales de negocio.

## Solución de Problemas
- **Lentitud en CPU**: Asegurarse de no estar recargando el modelo en cada llamada. Usar el modo batch si hay muchos mensajes.
- **Memory Error**: Revisar si se están acumulando tensores en la GPU sin liberar.

## Logs
- LOG_INFO: "minilm-embeddings: Cargando modelo en memoria..."
- LOG_INFO: "minilm-embeddings: Calculando similitud para [N] pares de mensajes"
- LOG_WARN: "minilm-embeddings: Texto excede la longitud máxima, será truncado"
