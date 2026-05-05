# Análisis de Diseño - ConversaSense AI

## 1. Arquitectura del Sistema: El Embudo Inteligente
El sistema implementa una arquitectura de **Online Cascade Learning** diseñada para maximizar el balance entre coste y precisión:
- **Capa Rápida (Filtrado Masivo)**: Utiliza un clasificador ligero para procesar 2 millones de mensajes, descartando interacciones normales y detectando "síntomas" obvios de frustración.
- **Capa Profunda (Análisis Diagnóstico)**: Un LLM de frontera procesa únicamente el 10-15% crítico de los datos.
- **Uncertainty-Driven Routing (El Puente Inteligente)**: La conexión entre capas no es lineal. Un enrutador evalúa la probabilidad del clasificador; si el resultado cae en la "zona gris" (incertidumbre semántica), delega automáticamente la decisión al LLM para asegurar que no se pierdan casos complejos como el sarcasmo.

## 2. Stack Tecnológico Optimizado
- **Machine Learning & Explicabilidad**:
    - **LightGBM**: Clasificador basado en árboles de decisión para inferencia ultra-rápida en CPU.
    - **SHAP (SHapley Additive exPlanations)**: Motor matemático que transforma el modelo de "caja negra" en una herramienta transparente, explicando qué características (features) causaron cada predicción a coste computacional casi cero.
- **Procesamiento y Validación de Datos**:
    - **Pandas / Polars**: Manipulación eficiente de grandes volúmenes de datos.
    - **Pandera**: Validación estricta de esquemas para garantizar que los datos cumplan con el contrato de calidad (encoding UTF-8, tipos de datos) antes de entrar al pipeline.
- **Control de Versiones y Auditoría**:
    - **DVC (Data Version Control)**: Creación de snapshots inmutables de datasets y modelos, permitiendo trazabilidad total y *rollbacks* instantáneos.

## 3. Componentes de Software (Separación de Responsabilidades)
- **IngestAdapter**: "Guardia de seguridad" del sistema. Fuerza la codificación UTF-8, aísla eventos del sistema y valida cada fila mediante Pandera.
- **FeatureEngine**: Generador de "magia determinística". Extrae heurísticas como conteos de repetición, métricas de **Dialog State Tracking (DST)** y utiliza **Sentence-BERT** para medir caídas en la coherencia semántica usuario-bot.
- **CascadeOrchestrator**: "Cerebro financiero". Ajusta los umbrales de probabilidad (τ) para garantizar que el volumen enviado a la API no supere el presupuesto de $5 USD mensuales.
- **TruthGuardian**: Aniquilador de alucinaciones. Implementa la arquitectura **Twin-Pass CoT-Ensembling**: el LLM genera una respuesta (Pass 1) y luego evalúa su propia conclusión contra el historial original para estimar su confianza (Pass 2).

## 4. Persistencia y Eficiencia Extrema
- **Estructura Columnar (Parquet)**: El uso de archivos Parquet permite que LightGBM lea únicamente las columnas necesarias para el entrenamiento/inferencia, acelerando el proceso de minutos a segundos al ignorar datos irrelevantes en disco.
- **Optimización de Inferencia (ONNX)**: La serialización del modelo a formato **ONNX (Open Neural Network Exchange)** elimina dependencias pesadas en producción y optimiza el uso de la CPU local, garantizando una respuesta inmediata en el entorno del cliente.
