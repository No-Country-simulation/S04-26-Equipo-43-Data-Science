# Roadmap de Gestión de Proyectos - ConversaSense AI

**Duración del Sprint**: 30 Días (4 Semanas)
**Metodología**: Desarrollo Ágil orientado a Componentes (Cascade Learning)

---

## Semana 1: Ingesta Resiliente y Motor de Características
**Objetivo**: Construir los cimientos de datos (DLQ) y la extracción masiva de las 47 heurísticas determinísticas en CPU.
**Entregables**: `ingest_adapter.py`, `feature_extractor.py`, DataFrames en formato Parquet.

*   **Día 1-2: Ingesta y Validación (IngestAdapter)**
    *   [ ] Configurar esquemas de `pandera` para validación estricta de CSV/JSON.
    *   [ ] Forzar codificación UTF-8 en lectura (RF-01).
    *   [ ] Implementar patrón **Dead Letter Queue (DLQ)** para registros corruptos (`errores_ingesta.parquet`).
    *   [ ] Crear heurísticas de detección de roles (User/Bot) para datos sin formato estricto.
*   **Día 3-5: Extracción por Mensaje y Señales NLU (FeatureExtractor)**
    *   [ ] Programar conteos básicos (mayúsculas, elongación de caracteres `has_char_elongation`, negaciones).
    *   [ ] Implementar extracción de **Dialog State Tracking (DST)** (`is_irrelevant_dst`, `is_premature_dst_exit`).
    *   [ ] Integrar `Sentence-BERT` para calcular `cosine_similarity` y `jaccard_index` entre pares User→Bot.
*   **Día 6-7: Agregación Vectorizada (FeatureAggregator)**
    *   [ ] Agrupar features a nivel de conversación (`aggregate_conversation_features`) usando operaciones vectorizadas en Pandas/Polars.
    *   [ ] Exportar matriz de 47 features a formato columnar **Parquet** para carga rápida en LightGBM.

---

## Semana 2: Inteligencia Rápida y Explicabilidad
**Objetivo**: Entrenar el "Enfermero" (LightGBM), validar su velocidad y conectar SHAP para transparencia matemática.
**Entregables**: Modelo ONNX/Pickle, SLA verificado, SHAP values.

*   **Día 8-10: Entrenamiento LightGBM (FrustrationClassifier)**
    *   [ ] Configurar modelo con `is_unbalance=True` y entrenamiento por hojas (*leaf-wise growth*).
    *   [ ] Entrenar utilizando la matriz Parquet excluyendo metadata temporal (Nivel 4).
    *   [ ] Validar convergencia y serializar modelo para inferencia rápida.
*   **Día 11-12: Explicabilidad (SHAP Engine)**
    *   [ ] Integrar `shap.TreeExplainer` sobre el modelo entrenado.
    *   [ ] Validar que SHAP procese las predicciones casi a costo cero sin perturbaciones locales.
*   **Día 13-14: Pruebas de Rendimiento y Ruido (UAT-05 y UAT-06)**
    *   [ ] **Test SLA**: Correr pipeline sobre 20,000 conversaciones. Verificar ejecución en `< 3 minutos`.
    *   [ ] **Test SHAP**: Inyectar variables de "Domingo 3AM" y verificar que SHAP les asigne peso `0` en la predicción.

---

## Semana 3: Orquestación de Cascada y Diagnóstico LLM
**Objetivo**: Implementar el enrutador inteligente y la arquitectura anti-alucinaciones con LLM para el 15% crítico.
**Entregables**: `cascade_orchestrator.py`, `truth_guardian.py` (LLM Second Pass).

*   **Día 15-16: Uncertainty-Driven Routing (CascadeOrchestrator)**
    *   [ ] Configurar umbrales de incertidumbre: $\tau_{low}=0.45$, $\tau_{high}=0.75$.
    *   [ ] Crear lógica de derivación: Predicciones en "zona gris" o $>0.75$ pasan al LLM; $<0.45$ finalizan flujo.
*   **Día 17-19: Capa Profunda y Anti-Alucinaciones (TruthGuardian)**
    *   [ ] Diseñar prompt de anclaje estricto encapsulando el historial en comillas triples.
    *   [ ] Implementar arquitectura **Twin-Pass CoT-Ensembling**: 
        *   *Pass 1*: Generación de razonamiento.
        *   *Pass 2*: Evaluación metacognitiva de la propia confianza.
*   **Día 20-21: Optimización de API y Batch Inference**
    *   [ ] Configurar `Exponential Backoff` para manejo seguro de Rate Limits de la API.
    *   [ ] Implementar **Batch Inference** agolpando peticiones para procesar el lote crítico dentro de las 22.2 horas estimadas.

---

## Semana 4: Validación Humana, Dashboard y Producción
**Objetivo**: Cierre del proyecto, validación científica contra humanos y empaquetado para el "Pitch".
**Entregables**: Dataset etiquetado (Métricas Kappa/F1), Dashboard Streamlit, Repositorio DVC.

*   **Día 22-24: Etiquetado Humano y Métricas Base**
    *   [ ] Extraer muestra aleatoria estratificada de 500 conversaciones.
    *   [ ] Ejecutar etiquetado doble ciego y Fase de Consenso (Juez).
    *   [ ] Calcular *Cohen's Kappa* (Objetivo 0.50 - 0.60).
    *   [ ] Calcular *F1-Score* contra el modelo híbrido (Objetivo $\ge 0.80$).
*   **Día 25-27: Dashboard de Insights (Streamlit)**
    *   [ ] Desarrollar UI aplicando **Leyes de Gestalt** (proximidad, contraste).
    *   [ ] Integrar gráficos de barra horizontales para *SHAP Importance* globales.
    *   [ ] Crear visor interactivo de conversaciones con la narrativa *CoT* generada por el LLM.
*   **Día 28-29: Integración DVC y Pruebas UAT Finales**
    *   [ ] Inicializar `dvc` y versionar el dataset original, el modelo LightGBM y los pipelines.
    *   [ ] Ejecutar UAT-01 ("The Death Spiral") y UAT-02 ("Sarcasmo Sutil").
*   **Día 30: Preparación del Pitch**
    *   [ ] Generar reporte resumen: Costo final (`< $5`), Tiempo procesamiento y Métricas de Éxito.
    *   [ ] Congelar código (`git tag v1.0`).

---

## Dependencias de Bloqueo Críticas (Critical Path)
1. **Día 7**: Si el *FeatureExtractor* no está vectorizado, el *SLA de 3 min* de la Semana 2 fallará.
2. **Día 10**: Si el modelo LightGBM tiene bajo Recall, el *Routing* enviará demasiados datos al LLM en la Semana 3, destruyendo el presupuesto de $5.
3. **Día 19**: Si el *Twin-Pass CoT* falla, el *Dashboard* de la Semana 4 mostrará alucinaciones, perdiendo la confianza del negocio.
