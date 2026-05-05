# Pruebas de Aceptación - ConversaSense AI

## 1. Criterios de Aceptación (UAT)

| ID | Caso de Uso | Escenario de Prueba | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **UAT-01** | **Detección de Bucles** | El usuario pide algo 3 veces y el bot no entiende (sin insultos). | Clasificado como 1 (Frustrado) por caída de coherencia semántica. |
| **UAT-02** | **Sarcasmo Sutil** | "¡Excelente! Me borraron la cuenta, son los mejores." | Identificado en la "Zona Gris" (0.45-0.75) y resuelto por el LLM. |
| **UAT-03** | **Ingesta Resiliente** | Carga de CSV con columnas desordenadas o en otro idioma. | Adaptado correctamente mediante heurísticas de rol forzando UTF-8. |
| **UAT-04** | **Validación Twin-Pass** | LLM intenta alucinar un motivo que no está en el chat. | El sistema detecta baja confianza en el Pass 2 y marca "Información insuficiente". |
| **UAT-05** | **SLA de Rendimiento** | Ingestar y clasificar 20,000 conversaciones en CPU 16GB. | Proceso completo (47 features + predicción) finaliza en < 3 minutos. |
| **UAT-06** | **Test de SHAP (Ruido)** | Clasificar conversación normal en "Domingo a las 3:00 AM". | Predicción "0" (Normal). SHAP muestra peso nulo para variables de Día/Hora. |
| **UAT-07** | **Mezcla Lingüística (Portuñol)** | "Eu preciso de ayuda con mi tarjeta, não funciona." | Clasificado correctamente por el pipeline multilingüe (ES/PT) sin pérdida de intención. |
| **UAT-08** | **Entradas Técnicas Densas** | Usuario pega un log de error o código de 50 líneas. | El preprocesador trunca/limpia y el modelo evita falsos positivos de "Frustración" por densidad. |
| **UAT-09** | **Abandono Silencioso** | Bot dice "No entendí" -> Usuario deja de escribir (sin despedida). | LightGBM detecta alta probabilidad de abandono basado en el último estado del bot. |
| **UAT-10** | **Frustración Pasivo-Agresiva** | "No te preocupes, buscaré otra solución que sí funcione." | El LLM (Twin-Pass) detecta la intención de abandono pese a la falta de insultos. |

## 2. Casos Edge

| Categoría | Escenario de Prueba | Ejecución | Resultado Esperado | Notas |
| :--- | :--- | :--- | :--- | :--- |
| **Datos Híbridos** | Carga mixta CSV + Parquet con 1M+ filas. | `/app/src/core/preprocess.py` (2M dataset) | Éxito | El motor de ingesta fusiona y estandariza columnas sin errores de memoria. |
| **Escalabilidad** | Pipeline en CPU (16GB RAM) sin GPU. | `preprocess.py` (line 75) | Éxito | Procesamiento en 2 min 12 seg (benchmark). |
| **Feature Stability** | Generación de variables sin conversación real. | `calculate_features` sin datos | Éxito | Retorna DataFrame con 47 columnas vacías (`NaN`). |
| **Ingesta Rápida** | Carga de 50,000 filas. | `./run_analysis_batch.py` | Éxito | Tiempo < 1 min (optimizado con muestreo de datos). |
| **Sin Frustración** | Conversaciones puramente informativas. | Dataset `no_frustration_batch.csv` | Éxito | Predicción 100% "0" (Normal). |
| **Datos Corruptos** | Archivo CSV con UTF-8 inválido. | `/app/src/core/preprocess.py` | Fallo Controlado | Lanza `UnicodeDecodeError` capturado por `try-except`. |
| **Variables Ruidosas** | Generación de features en domingo. | `preprocess_sentiment` `timestamp="2025-12-14 10:00:00"` | Éxito | SHAP muestra peso nulo para variables de tiempo. |
| **Abandono** | Conversación con "No entendí" del bot. | `analyze_sentiment` `"No entendí"` | Éxito | Predicción "1" (Frustrado). |
| **Lingüística** | Texto mixto ES/PT. | `preprocess_text` `"Eu preciso... não funciona"` | Éxito | Clasificado como español con alta probabilidad de frustración. |




## 3. Métricas de Validación Humana (Criterios de Calidad)

- **Prioridad de Recall (Sensibilidad)**: El objetivo principal es identificar el mayor número de usuarios frustrados. Se acepta una tasa moderada de falsos positivos para no ignorar crisis reales.
- **Acuerdo Inter-anotador (IAA)**:
    - **Métrica**: Cohen's Kappa.
    - **Objetivo**: **0.50 - 0.60** (Fiabilidad moderada). Se reconoce la subjetividad intrínseca de la frustración.
- **Fase de Resolución de Desacuerdos**:
    - **Criterio**: El "Juez" (anotador principal) actúa como árbitro final.
    - **Regla de Oro**: La persistencia en el problema (User Escalation) tiene mayor peso que el tono puntual.
    - **Proceso**: En caso de duda extrema, se consulta al equipo completo para establecer un precedente.
- **Puntaje F1-Score (Balance)**: 
    - **Objetivo**: **>= 0.75**. 
    - **Razón**: Mantiene un equilibrio entre detectar frustración real (Recall) y evitar ruido innecesario (Precision). Un F1 bajo (<0.70) invalidaría el sistema de alertas.

## 4. Protocolo de Evaluación Final
1.  **Muestreo**: Selección de 500 conversaciones mediante muestreo aleatorio estratificado.
2.  **Etiquetado**: Doble ciego por el equipo de la hackathon.
3.  **Cálculo**: Generación de matriz de confusión, Precision, Recall y Macro-F1.
4.  **Auditoría de SHAP**: Revisión manual de 20 casos para confirmar que las razones matemáticas de LightGBM coinciden con la lógica humana.
5.  **Sesgos**: Verificar que el modelo no penaliza "días festivos" o "horas nocturnas" (SHAP ruido).

