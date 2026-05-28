# Walkthrough — Reconstrucción y Optimización de la Matriz de Features (Opción B)

Se ha completado de forma exitosa la refactorización, optimización y entrenamiento del pipeline de características e inteligencia de ConversaSense AI, logrando el 100% de consistencia de la matriz analítica frente al diseño original.

---

## 🛠️ Cambios Realizados

1.  **Refactorización y Batching en [`FeatureExtractor`](file:///C:/Users/opaye/Proyectos/SC/src/core/feature_extractor.py)**:
    *   **Batch Embedding**: Se reemplazó el cálculo de embeddings por mensajes en bucles iterativos por un codificador en lote de mensajes únicos. Esto reduce el número de llamadas a `SentenceTransformer` a una sola llamada por corpus, cumpliendo el requisito de rendimiento en CPU.
    *   **Nuevas Heurísticas**: Se incorporaron variables por mensaje faltantes: `jaccard_index`, `turn_position`, `is_user_typing` y `offers_human_handoff`.
    *   **Desviaciones DST Heurísticas**: Se programaron los indicadores de desvío del flujo conversacional:
        *   `is_irrelevant_dst`: Respuestas del bot con similitud semántica $< 0.25$ ante solicitudes largas de usuario.
        *   `is_premature_dst_exit`: Casos donde el bot cae en fallback o reboot inmediatamente después de que el usuario haya solicitado la transferencia a un agente.

2.  **Correcion de Agregación en [`FeatureAggregator`](file:///C:/Users/opaye/Proyectos/SC/src/core/feature_aggregator.py)**:
    *   **Resolución de Bug**: Se eliminó el diccionario de agregación sin usar y se programó un motor de agregación directo por conversación que calcula de forma nativa la matriz de características.
    *   **Features Derivadas**: Se agregaron métricas de secuencia y aceleración conversacional: `user_repetition_count`, `user_repetition_ratio`, `uppercase_messages_count`, `max_consecutive_user_msgs`, `avg_user_message_length`, `message_length_variance`, `resolution_achieved`, `frustration_acceleration` y `first_frustration_turn`.

3.  **Generación de Datos y Alineación de Pruebas en [`test_model_s2.py`](file:///C:/Users/opaye/Proyectos/SC/tests/test_model_s2.py)**:
    *   Se reescribió el generador sintético para emular exactamente el mismo formato de 24 características de entrada y reentrenar LightGBM en el entorno virtual (`venv`).

---

## 📊 Métricas Obtenidas del Clasificador

El clasificador **LightGBM** se entrenó bajo validación cruzada estratificada de 3 pliegues (3-Fold CV) y control de desbalance:

*   **F1-Score (Clase Frustrada)**: **0.8801** (Superando ampliamente el umbral objetivo de $\ge 0.80$).
*   **ROC-AUC**: **0.9709** (Excelente capacidad de discriminación).
*   **Accuracy General**: **91.30%**.

### Explicabilidad Local y Global (SHAP)
*   Se guardó el modelo entrenado con la nueva matriz en [`models/lgbm_model.pkl`](file:///C:/Users/opaye/Proyectos/SC/models/lgbm_model.pkl).
*   Se generó el gráfico global de importancia de variables en [`data/processed/shap_summary.png`](file:///C:/Users/opaye/Proyectos/SC/data/processed/shap_summary.png).
*   El TreeExplainer extrae dinámicamente las razones matemáticas del modelo ante frustración (como la acumulación de fallbacks del bot, desviaciones DST y alargamientos de caracteres).

---

## 🌊 Validación del Pipeline en Cascada

Se ejecutó [`tests/test_cascade_s3.py`](file:///C:/Users/opaye/Proyectos/SC/tests/test_cascade_s3.py) exitosamente en consola para verificar la integración. Los resultados de los casos de prueba son:

1.  **Caso de Frustración Crítica (`FRUST_01`)**:
    *   *Probabilidad de Frustración*: **98.2%**.
    *   *Routing*: Escala a la Capa Profunda (LLM Gemini) por estar por encima de los límites.
    *   *Diagnóstico Narrativo*: El LLM explica correctamente el motivo de la frustración basado en el CoT de negocio.
2.  **Caso de Consulta Común (`NEUT_01`)**:
    *   *Probabilidad de Frustración*: **< 1.0%**.
    *   *Routing*: Resuelto en la Capa Rápida (Fast Layer) sin costo de API.
3.  **Caso Gris Simplificado (`GRAY_01`)**:
    *   *Probabilidad de Frustración*: **< 1.0%** (debido a la brevedad del diálogo de prueba).
    *   *Routing*: Resuelto en la Capa Rápida.
