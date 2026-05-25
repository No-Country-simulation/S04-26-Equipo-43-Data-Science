# Reporte de Avances - Semana 1: Ingesta Resiliente y Motor de Características

He completado con éxito los objetivos de la **Semana 1: Ingesta Resiliente y Motor de Características**.

## Logros Alcanzados

1. **Entorno y Estructura**:
    - Se configuró el entorno virtual y se instalaron las dependencias críticas (`pandera`, `pandas`, `polars`, `lightgbm`, `sentence-transformers`, etc.).
    - Se estableció la estructura de carpetas:
        - `src/core/`: Lógica principal del sistema.
        - `src/utils/`: Utilidades como el logger.
        - `data/raw/`: Datos de entrada sin procesar.
        - `data/processed/`: Salidas procesadas (Parquet).
        - `data/dlq/`: Dead Letter Queue para registros corruptos.

2. **IngestAdapter**:
    - Implementado con validación estricta de esquemas mediante `pandera`.
    - **Carga de CSV/JSON**: Con forzado de encoding UTF-8 y fallback a latin-1.
    - **Dead Letter Queue (DLQ)**: Los registros que fallan la validación se guardan automáticamente en `data/dlq/errores_ingesta.parquet` con el motivo técnico del error.
    - **Normalización de Roles**: Heurísticas para mapear roles variados (ej: 'cliente', 'asistente') a los estándares `user`, `bot` y `system`.

3. **FeatureExtractor**:
    - Motor de 22+ características a nivel de mensaje.
    - **Detección multilingüe (ES/PT)**: Identificación automática del idioma para aplicar diccionarios de señales correctos.
    - **Heurísticas de texto**: `uppercase_ratio`, `has_char_elongation`, conteo de exclamaciones/interrogaciones.
    - **Señales NLU**: Detección de negaciones, lenguaje hostil (profanity) y peticiones de escalamiento humano.
    - **Coherencia Semántica**: Integración de `Sentence-BERT` (`paraphrase-multilingual-MiniLM-L12-v2`) para calcular `cosine_similarity` entre la solicitud del usuario y la respuesta del bot.

4. **FeatureAggregator**:
    - Transforma las señales individuales en una matriz consolidada por conversación.
    - Cálculo de métricas agregadas: `avg_cosine_similarity`, `user_repetition_ratio`, `bot_fallback_count`, y aceleración de señales de frustración.

5. **Validación**:
    - Se verificó el pipeline completo mediante `tests/test_pipeline_s1.py`.
    - El sistema procesa exitosamente flujos multilingües y genera la matriz de características final.

---

## Entregables Disponibles

| Archivo | Descripción |
| :--- | :--- |
| `src/core/ingest_adapter.py` | Clase para ingesta y validación con Pandera. |
| `src/core/feature_extractor.py` | Extractor de heurísticas y similitud semántica. |
| `src/core/feature_aggregator.py` | Agregador de métricas a nivel de conversación. |
| `src/core/signal_dictionaries.py` | Diccionarios regex multilingües (ES/PT). |
| `data/processed/features_S1.parquet` | Matriz de 47 features lista para el modelo LightGBM. |
| `src/utils/logger.py` | Sistema de logging centralizado. |
| `requirements.txt` | Dependencias del proyecto. |

---

**Estado del Proyecto**: 🟢 En tiempo (Semana 1 completada).
**Próximo Paso**: Semana 2 - Implementación del Clasificador LightGBM y análisis de explicabilidad con SHAP.
