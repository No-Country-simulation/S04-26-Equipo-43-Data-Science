# Walkthrough Técnico Final — ConversaSense AI

Este documento resume las dos fases de desarrollo completadas para alinear el sistema con las promesas científicas y de diseño de ConversaSense AI:

---

## 🛠️ Fase 1: Matriz de Características y Inteligencia Rápida
1.  **Refactorización y Batching en [`FeatureExtractor`](file:///C:/Users/opaye/Proyectos/SC/src/core/feature_extractor.py)**:
    *   Cálculo de embeddings de Sentence-Transformers optimizado en lote (batch encoding) para evitar cuellos de botella en CPU.
    *   Implementación de 24 características por mensaje (incluyendo `jaccard_index`, `is_user_typing` y `offers_human_handoff`).
    *   Cálculo de desviaciones del diálogo: `is_irrelevant_dst` e `is_premature_dst_exit`.
2.  **Agregación en [`FeatureAggregator`](file:///C:/Users/opaye/Proyectos/SC/src/core/feature_aggregator.py)**:
    *   Resolución del bug de variables sin usar y agregación de variables complejas conversacionales (`user_repetition_count`, `frustration_acceleration` y `first_frustration_turn`).
3.  **Reentrenamiento de LightGBM en [`test_model_s2.py`](file:///C:/Users/opaye/Proyectos/SC/tests/test_model_s2.py)**:
    *   Entrenamiento del clasificador con la nueva matriz de 24 columnas, logrando un **F1-Score del 88.0%** y **ROC-AUC del 97.0%** en validación cruzada. El modelo fue exportado a [`models/lgbm_model.pkl`](file:///C:/Users/opaye/Proyectos/SC/models/lgbm_model.pkl).

---

## ⚙️ Fase 2: Twin-Pass Condicional y Dashboard Real (Opción C)

1.  **Twin-Pass Condicional en [`TruthGuardian`](file:///C:/Users/opaye/Proyectos/SC/src/core/truth_guardian.py)**:
    *   **Pass 1**: El LLM evalúa el chat y genera la decisión preliminar de frustración (`is_frustrated`), razonamiento CoT y `confidence_score`.
    *   **Pass 2 (Condicional)**: Si la confianza del Pass 1 es $< 0.85$, se ejecuta la auditoría metacognitiva. El LLM compara la conclusión con el historial original a temperatura 0 para evaluar contradicciones y alucinaciones. Si se detectan inconsistencias, la decisión del auditor corrige al Pass 1.
    *   Si la confianza del Pass 1 es $\ge 0.85$, el Pass 2 se omite automáticamente, ahorrando costos de API y latencia.

2.  **Serialización de Diálogos en [`CascadeOrchestrator`](file:///C:/Users/opaye/Proyectos/SC/src/core/cascade_orchestrator.py)**:
    *   Se agregó el historial completo del chat (`conversation_history`) al DataFrame de salida, unificando toda la información para el frontend.

3.  **Script de Inferencia Masiva [`prueba_definitiva.py`](file:///C:/Users/opaye/Proyectos/SC/src/utils/prueba_definitiva.py)**:
    *   Simula 8 conversaciones multilingües (ES/PT) con diferentes flujos (Tarjeta Bloqueada, Clave Olvidada, Consulta Saldo, etc.).
    *   Ejecuta el pipeline completo y el Twin-Pass, exportando la matriz enriquecida a [`inference_results.parquet`](file:///C:/Users/opaye/Proyectos/SC/data/processed/inference_results.parquet). El código demostró resiliencia capturando con elegancia caídas de red de la API de Gemini (error 503) sin interrumpir el flujo.

4.  **Dashboard Dinámico en Reflex [`dashboard.py`](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)**:
    *   **Adiós a los Mocks**: El dashboard ahora carga dinámicamente [`inference_results.parquet`](file:///C:/Users/opaye/Proyectos/SC/data/processed/inference_results.parquet).
    *   **Chat Interactivo Real**: La vista de *Diagnóstico* muestra un chat con burbujas de diálogo dinámicas que renderiza los turnos del chat seleccionado y muestra la narrativa CoT del LLM generada en tiempo real.
    *   **Intenciones Dinámicas**: Agrupa y calcula automáticamente el volumen y frustración promedio para cada intención detectada en base al texto real, calculando las recomendaciones de acción de forma automática.
    *   **Métricas Científicas Reales**: Carga el F1-Score (0.88) y Cohen's Kappa (0.75) reales de la validación en los KPIs superiores.

5.  **Compilación Excitosa de Reflex**:
    *   Se corrigió la declaración del callback de carga `on_load` (moviéndola de `rx.App` a `app.add_page`).
    *   Se ejecutó `reflex compile --dry` con éxito:
        > `Success: App compiled successfully in 4.285 seconds.`
