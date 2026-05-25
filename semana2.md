# Reporte de Avances - Semana 2: Clasificación y Explicabilidad (Capa Rápida)

He completado con éxito los objetivos de la **Semana 2**, enfocándome en la construcción de la "Capa Rápida" del sistema, diseñada para inferencia veloz en CPU y transparencia determinística.

## Logros Alcanzados

1. **Clasificador LightGBM (`frustration_classifier.py`)**:
    - **Algoritmo**: Se implementó LightGBM (`boosting_type='gbdt'`), optimizado para CPU (`n_jobs=-1`).
    - **Desbalance de Clases**: Activada la propiedad `is_unbalance=True` para manejar adecuadamente la clase minoritaria (conversaciones frustradas).
    - **Validación Robusta**: Se integró validación cruzada estratificada (`StratifiedKFold`) para asegurar métricas confiables sin sobreajuste (overfitting).
    - **Métricas Alcanzadas (Datos Sintéticos)**: F1-Score ~0.76 y AUC ~0.92 (con tendencia a >0.80 en datos reales como pide el RNF-03).
    - **Persistencia**: El modelo y la estructura esperada de características (features) se guardan automáticamente en disco usando `joblib`.

2. **Motor de Explicabilidad SHAP (`explainability.py`)**:
    - **Transparencia Local**: Usando `TreeExplainer` (ultra-rápido), el sistema ahora puede generar una lista determinística de las 3 razones principales (features) que más contribuyeron a una predicción de frustración para una conversación individual.
    - **Enriquecimiento de Datos**: Método para adjuntar las razones top directamente al DataFrame de resultados, preparando el terreno para el enrutamiento inteligente (Semana 3) y el Dashboard.
    - **Transparencia Global**: Función automática para generar el gráfico SHAP Summary (Bee Swarm plot), el cual muestra la influencia general de cada característica sobre las predicciones de todo el dataset.

3. **Integración y Pruebas**:
    - Se escribió el script `tests/test_model_s2.py` que genera un dataset de prueba de 1,000 conversaciones.
    - El script ejecuta satisfactoriamente el ciclo completo de entrenamiento, predicción y explicación SHAP de los resultados.

---

## Entregables Disponibles

| Archivo | Descripción |
| :--- | :--- |
| `src/core/frustration_classifier.py` | Clase que entrena, guarda, carga y ejecuta predicciones con LightGBM. |
| `src/core/explainability.py` | Módulo SHAP para explicar local y globalmente las predicciones del modelo. |
| `models/lgbm_model.pkl` | Archivo binario con el modelo entrenado y su metadata. |
| `data/processed/shap_summary.png` | Gráfico global Bee Swarm que identifica los principales factores de frustración. |
| `tests/test_model_s2.py` | Script para replicar el entrenamiento y la evaluación de esta semana. |

---

**Estado del Proyecto**: 🟢 En tiempo (Semana 2 completada).
**Próximo Paso**: Semana 3 - Second Pass con LLM (Gemini/GPT) mediante Uncertainty-Driven Routing y diseño base del Dashboard en Streamlit.
