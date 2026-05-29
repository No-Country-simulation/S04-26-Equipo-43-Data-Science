# Investigación de Señales Lingüísticas Implícitas (NLP) - ConversaSense AI

Esta investigación tiene como objetivo ampliar los diccionarios heurísticos en [signal_dictionaries.py](file:///C:/Users/opaye/Proyectos/SC/src/core/signal_dictionaries.py) mediante Gemini Deep Research, incrementando la sensibilidad del clasificador rápido (LightGBM) ante frustración pasiva, sarcasmo o desvíos sutiles sin depender de insultos explícitos.

---

## 📝 Prompt para Gemini Deep Research

Copia y pega el siguiente prompt en **Gemini Deep Research** u otro LLM de análisis profundo:

```text
Actúa como un Lingüista Computacional y Experto en NLP especializado en el análisis de interacciones conversacionales en canales de atención al cliente (Fintech, Banca y E-commerce). 

El sistema ConversaSense AI utiliza un pipeline de inferencia híbrido en cascada. La primera capa (LightGBM en CPU) clasifica conversaciones basándose en la extracción de características heurísticas simples. Para que esta capa sea altamente sensible, necesitamos ampliar el diccionario de expresiones regulares en español (ES) y portugués (PT) para capturar señales implícitas de frustración, impaciencia y descontento conversacional.

### TU TAREA
Realiza una investigación profunda y exhaustiva sobre las expresiones coloquiales, modismos regionales, ironías sutiles y patrones lingüísticos que indican fricción del cliente al interactuar con un asistente virtual (chatbot).

Proporciona los resultados organizados estrictamente en las siguientes categorías para ESPAÑOL (ES) y PORTUGUÉS (PT) (incluyendo variaciones de Latinoamérica, España, Brasil y Portugal):

1. PROFANITY / AGRESIVIDAD IMPLÍCITA:
   - Insultos atenuados, expresiones pasivo-agresivas, ironías agresivas.
   - Ejemplos en ES: "es un chiste", "vaya ayuda", "estafadores", "pésimo servicio", "me están tomando el pelo".
   - Ejemplos en PT: "palhaçada", "estão me tirando", "que piada", "pessimo servico", "brincadeira".

2. NEGATION / FRUSTRACIÓN PASIVA Y RESIGNACIÓN:
   - Frases donde el usuario expresa desacuerdo o resignación tras un fallo del bot.
   - Ejemplos en ES: "no me sirve", "deja así", "no es eso", "olvídalo", "otra vez con lo mismo", "no entiendes nada".
   - Ejemplos en PT: "deixa pra lá", "não adianta", "esquece", "de novo isso", "você não entende", "não serve".

3. ESCALATION / SOLICITUD DE ESCALAMIENTO IMPLÍCITO:
   - Formas alternativas de pedir ayuda humana sin usar directamente palabras obvias como "agente".
   - Ejemplos en ES: "alguien real", "con una persona", "que me atienda alguien", "con un supervisor", "teléfono de soporte", "asistencia de verdad".
   - Ejemplos en PT: "alguém de verdade", "falar com pessoa", "atendente real", "ajuda humana", "atendimento especializado".

4. SARCASMO Y FRUSTRACIÓN VELADA:
   - Expresiones de descontento camufladas de agradecimiento u optimismo exagerado.
   - Ejemplos en ES: "genial, me bloquearon", "excelente ayuda", "gracias por nada", "buenísima la atención (sarcástico)".
   - Ejemplos en PT: "ótimo, me bloquearam", "obrigado por nada", "ótima ajuda (irônico)".

### FORMATO DE SALIDA REQUERIDO
Para cada categoría y lenguaje (ES y PT), genera una lista de patrones de Expresiones Regulares (regex) válidas en Python (`re.search`). Los patrones deben ser:
- Insensibles a mayúsculas y minúsculas (ignora mayúsculas/minúsculas).
- Resistentes a variaciones tipográficas comunes (ej. acentos opcionales).
- Compactos (usa agrupaciones eficientes con `|` y límites de palabra `\b`).
- Acompañados de 3 ejemplos reales que disparan el regex y su justificación lingüística.

Presenta el código directamente en un bloque de código Python listo para copiar y pegar, estructurado como el diccionario `SIGNALS` de ConversaSense AI.
```

---

## 🛠️ Cómo Integrar los Resultados en el Código

Una vez que obtengas la respuesta de Gemini Deep Research, puedes integrar las nuevas expresiones regulares en [signal_dictionaries.py](file:///C:/Users/opaye/Proyectos/SC/src/core/signal_dictionaries.py). 

### Pasos para la Integración:
1. Abre [signal_dictionaries.py](file:///C:/Users/opaye/Proyectos/SC/src/core/signal_dictionaries.py).
2. Incorpora los patrones regex generados en las llaves respectivas (`"fallback"`, `"apology"`, `"profanity"`, `"negation"`, `"escalation"`) tanto en el bloque `"es"` como en `"pt"`.
3. Ejecuta de nuevo el reprocesamiento de lotes en el Dashboard para validar cómo impacta en las predicciones del clasificador LightGBM.

Esto mejorará las características determinísticas extraídas por el [FeatureExtractor](file:///C:/Users/opaye/Proyectos/SC/src/core/feature_extractor.py), permitiendo que LightGBM detecte correctamente la fricción de Zona Gris sin necesidad de intervención manual o heurísticas de rescate restrictivas en producción.
