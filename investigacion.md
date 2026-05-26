Basándome en el estado actual del proyecto (hemos finalizado la arquitectura central hasta la Semana 3) y el Roadmap Oficial de la Semana 4, aquí tienes
  una lista de los temas que potencialmente podríamos investigar antes de escribir el código final.

  Elige el que consideres más crítico para el éxito del proyecto:

  📊 1. Principios de Interfaz "Gestalt" para el Dashboard
   * Contexto (Semana 4, Día 25-27): El roadmap exige un dashboard en Streamlit que aplique "Leyes de Gestalt" (proximidad, contraste) para contar una
     historia de datos (Data Storytelling).
   * Qué investigaríamos: Cómo estructurar componentes nativos de Streamlit (métricas, gráficos de Altair/Plotly) para cumplir con estas leyes psicológicas
     de diseño sin sobrecargar la interfaz. (Podríamos crear un skill streamlit-gestalt).

  📦 2. Versionado de Modelos y Datos con DVC
   * Contexto (Semana 4, Día 28-29): El roadmap exige usar DVC (Data Version Control) para versionar el dataset original, el modelo LightGBM y los
     pipelines antes de la entrega final.
   * Qué investigaríamos: Mejores prácticas para configurar DVC en local, cómo vincularlo a Git sin subir archivos pesados al repositorio, y cómo
     estructurar el dvc.yaml para reproducibilidad.

  🧪 3. Métricas de Fiabilidad (Cohen's Kappa & F1-Score)
   * Contexto (Semana 4, Día 22-24): Necesitamos calcular métricas contra una "fase de consenso humano" para validar que el modelo no solo es rápido, sino
     científicamente fiable.
   * Qué investigaríamos: Cómo implementar scripts de evaluación con scikit-learn para obtener la matriz de confusión, el F1-Score híbrido y calcular el
     Cohen's Kappa inter-anotadores (para asegurar que el "Juez Humano" y la IA están alineados).

  ⚙️ 4. Optimización Batch para el LLM (Rate Limits)
   * Contexto (Semana 3 / Optimización pendiente): En el roadmap se menciona configurar Exponential Backoff y Batch Inference para no exceder los límites
     de la API de OpenRouter/Gemini al procesar miles de conversaciones.
   * Qué investigaríamos: Cómo usar la librería tenacity (que ya tienes instalada en tu entorno) para manejar reintentos automáticos, y cómo empaquetar
     consultas asíncronas (asyncio) para el TruthGuardian.
