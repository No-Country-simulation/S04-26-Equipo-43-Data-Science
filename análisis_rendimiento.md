# Análisis de Rendimiento - ConversaSense AI

## 1. Benchmarks de Velocidad (Optimización por Lotes)

| Proceso | Volumen | Tiempo Estimado | Estrategia de Optimización |
| :--- | :--- | :--- | :--- |
| Ingesta y Limpieza | 2M Mensajes | 5 - 8 minutos | I/O Columnar (Parquet) |
| Extracción de Features | 200K Conv | 10 - 15 minutos | Multiprocessing + Vectorización |
| Inferencia LightGBM | 200K Conv | < 1 minuto | Inferencia nativa en CPU |
| Inferencia LLM (Pass 2) | 20K Conv (10%) | ~22.2 horas | **Batch Inference** (Minimiza cuellos de red) |

> [!NOTE]
> El tiempo del LLM se basa en el Free Tier de Gemini (15 RPM = 900 req/h). El uso de *Batch Inference* permite agrupar solicitudes para maximizar el rendimiento real.

## 2. Escalabilidad y Eficiencia
- **Procesamiento Vectorizado**: Todas las transformaciones de datos se realizarán mediante operaciones vectorizadas en memoria (NumPy/Pandas/Polars). Esto permite que el hardware procese múltiples datos en paralelo, garantizando que el tiempo de ejecución crezca de forma **lineal** y no exponencial ante aumentos de carga (hasta 3M de mensajes).
- **Almacenamiento Columnar**: El uso de archivos Parquet asegura que la lectura de las 47 características sea eficiente, cargando solo los bytes necesarios desde el disco.
- **Gestión de Memoria**: Procesamiento por lotes (chunking) para mantener el uso de RAM por debajo de los 16GB, incluso con el corpus masivo.

## 3. Estabilidad y Robustez Empresarial
- **Patrón Dead Letter Queue (DLQ)**: En lugar de simples registros de log, los mensajes o conversaciones mal formadas/corruptas se desviarán automáticamente a una cola de "mensajes muertos" (`errores_ingesta.parquet`). Esto permite que el pipeline principal fluya sin interrupciones y facilita una auditoría estructurada posterior.
- **Snapshotting (Checkpoints)**: Guardado de estados intermedios en formato Parquet después de cada fase crítica (Ingesta, Extracción, Inferencia). Si el sistema falla, puede retomar desde el último checkpoint exitoso.
- **Graceful API Handling**: Implementación de *Exponential Backoff* para manejar errores de límite de cuota (Rate Limits) o caídas temporales del servicio de la API del LLM.
