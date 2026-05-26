---
trigger: always_on
---

# 📋 Decisiones Pendientes

Registro de decisiones tomadas y por tomar en ConversaSense AI.

---

## Estado: 🟢 Definido

---

## Decisiones Técnicas Confirmadas ✅

### 1. Stack de Datos & ML
- **Lenguaje:** Python 3.10+
- **Motor de Clasificación:** LightGBM (Capa rápida)
- **Second Pass:** LLM (Gemini Flash / GPT-4o-mini) para casos inciertos (Routing p > 0.45).
- **Validación:** Pandera (Schema enforcement).

### 2. Frontend (Dashboard)
- **Framework:** Streamlit.
- **Visualización:** SHAP Explainer + Sparklines + Bullet Graphs.

### 3. Convenciones
- **Naming:** snake_case para variables/funciones/archivos.
- **Logging:** Sistema especializado ES/PT.

---

## Decisiones Pendientes 📋

| Decisión | Opciones | Impacto |
|----------|----------|---------|
| **Hosting Dashboard** | Streamlit Cloud, AWS, On-premise | Accesibilidad del equipo |
| **Dataset de Entrenamiento** | Corpus 2M (estratificado) vs Subsample | Calidad del modelo |

---

## Historial de Decisiones

| Fecha | Decisión | Elegido |
|-------|----------|---------|
| 2026-05-25 | Stack Completo | Python + LightGBM + Streamlit |
| 2026-05-25 | Arquitectura | Online Cascade Learning |
