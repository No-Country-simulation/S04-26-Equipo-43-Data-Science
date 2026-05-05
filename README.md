# ConversaSense AI: Arquitectura Multilingüe para la Retención y Detección de Frustración

> Sistema avanzado de análisis de sentimiento e intención para optimizar flujos conversacionales y reducir el abandono de usuarios.

---

## 📁 Estructura del Proyecto

```
├── .agent/                             # Cerebro de Antigravity (Skills, Rules, Workflows)
├── data/                               # Corpus de conversaciones (CSV/Parquet)
├── src/
│   ├── core/                           # Motores de NLP y Clasificación
│   │   ├── preprocess.py               # Limpieza multilingüe (ES/PT)
│   │   ├── sentiment.py                # Modelo de Frustración Multi-turno (ICL)
│   │   ├── intent.py                   # Detección de Intenciones (Symbol Tuning)
│   │   └── predictive.py               # Predicción de Abandono (LightGBM)
│   ├── dashboard/                      # Visualización e Insights
│   │   └── app.py                      # Streamlit Dashboard
│   └── utils/
│       └── logger.py                   # Sistema de logs especializado
├── notebooks/                          # Experimentos y validación de clusters OOS
└── README.md
```

## 🧠 Arquitectura Técnica

### 1. Pipeline Multilingüe (ES / PT)
Procesamiento nativo mediante **BETO** y **BERTimbau**, evitando traducciones para mantener el matiz emocional de los mensajes transaccionales.

### 2. Detección de Frustración Multi-turno
Implementación de **In-Context Learning (ICL)** mediante LLMs para detectar señales sutiles de enojo (repeticiones, negaciones críticas) analizando el historial completo de la conversación.

### 3. Intent Discovery & Symbol Tuning
- **Symbol Tuning**: Compresión semántica de etiquetas para mejorar la precisión.
- **Out-of-Scope (OOS)**: Clustering no supervisado con **LOF** para descubrir nuevas intenciones no resueltas por el bot actual.

### 4. Predicción de Abandono (Factor X)
Modelo predictivo basado en señales de comportamiento:
- Entrada de texto libre vs. botones.
- Errores de incapacidad del bot ("No entendí").
- Reinicios de flujo innecesarios.

## 📊 Dashboard de Insights (Gestalt UI)
Visualización diseñada para la toma de decisiones del equipo de producto:
- **Sparklines**: Tendencias de sentimiento en tiempo real.
- **Bullet Graphs**: KPIs de escalamiento vs. objetivos.
- **Data Storytelling**: Identificación de los flujos que causan mayor frustración.

## 📜 Convenciones del Proyecto

- **Lenguaje**: Python 3.10+
- **Naming**: `snake_case` para variables y funciones, `PascalCase` para clases.
- **Documentación**: Comentarios breves en español; código en inglés.
- **Logging**: Seguimiento obligatorio del flujo de procesamiento de los 2M de mensajes.

---

## 🛠️ Herramientas de Antigravity
Este proyecto cuenta con una configuración completa de agentes:
- `/alinear-contexto`: Para mantener la consistencia técnica.
- `arquitectura-nlp.md`: Reglas específicas de modelado.
- `stack-tecnologico.md`: Seguimiento de dependencias (Transformers, Scikit-learn).
