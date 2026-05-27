# Análisis de Requisitos - ConversaSense AI

## 1. Requisitos Funcionales (RF)

| ID | Nombre | Descripción |
| :--- | :--- | :--- |
| RF-01 | Ingesta Multiformato | El sistema debe procesar archivos CSV y JSON de forma agnóstica al esquema. |
| RF-02 | Normalización de Roles | Identificar y unificar roles (Usuario, Bot, Sistema) incluso si las columnas varían. |
| RF-03 | Extracción de Heurísticas | Calcular 47 métricas (mayúsculas, repeticiones, similitud coseno, DST deviation). |
| RF-04 | Clasificación Binaria | Clasificar conversaciones como "Frustrada" (1) o "Normal" (0) usando LightGBM. |
| RF-05 | Enrutamiento de Incertidumbre | Detectar casos en la zona gris (probabilidad 0.45 - 0.75) para análisis profundo. |
| RF-06 | Razonamiento CoT | Generar una explicación humana del fallo del bot mediante un LLM (Second Pass). |
| RF-07 | Twin-Pass Verification | Validar el razonamiento del LLM para evitar alucinaciones. |
| RF-08 | Dashboard de Insights | Visualizar métricas SHAP, tendencias y narrativas en Streamlit. |

## 2. Requisitos No Funcionales (RNF)

| ID | Categoría | Requisito |
| :--- | :--- | :--- |
| RNF-01 | Rendimiento | Procesar 2 millones de mensajes en menos de 30 minutos (Capa Rápida). |
| RNF-02 | Costo | El costo de API en producción debe ser inferior a $5 USD mensuales. |
| RNF-03 | Precisión | Alcanzar un F1-Score >= 0.80 en la clase "Frustrada". |
| RNF-04 | Escalabilidad | Capacidad para ejecutarse en una CPU estándar con 16GB de RAM sin GPU. |
| RNF-05 | Privacidad | Los datos masivos se procesan localmente; solo el 15% crítico viaja a la API. |
| RNF-06 | Mantenibilidad | Uso de DVC para versionamiento de modelos y datasets. |

---

## 3. Validación de Requisitos

### 3.1. Validación de los Requisitos Funcionales (RF)

- **RF-01 y RF-02 (Ingesta y Normalización)**: Implementar un adaptador agnóstico que reconstruya roles mediante heurísticas y centralice el control de formato es la decisión correcta para manejar la alta variabilidad del lenguaje y los datos no estructurados en sistemas de diálogo. **Nota de refinamiento**: Se exige contractualmente la codificación UTF-8 en el RF-01 usando validadores como `pandera`.
- **RF-03 (Extracción de Heurísticas)**: Calcular métricas como la similitud del coseno para la coherencia semántica y el seguimiento del estado del diálogo (DST) está directamente respaldado por la literatura sobre predicción de abandono y quiebres conversacionales.
- **RF-04 (Clasificación con LightGBM)**: Usar LightGBM sobre un conjunto de características numéricas en lugar de un modelo de lenguaje masivo (LLM) permite clasificaciones ultra rápidas y robustas, y es la base de las arquitecturas en cascada eficientes.
- **RF-05 (Enrutamiento de Incertidumbre)**: Definir la "zona gris" en el rango de probabilidad de **0.45 - 0.75** es el estándar de oro para el *Uncertainty-Driven LLM Routing*. Esto asegura que los casos de sarcasmo o ambigüedad no se pierdan, derivándolos al LLM como bisturí fino.
- **RF-06 y RF-07 (CoT y Twin-Pass Verification)**: Aplicar *Chain-of-Thought* para extraer narrativas y blindarlo con una arquitectura de doble pasada (*Twin-Pass CoT-Ensembling*) es la contramedida científica exacta para evitar alucinaciones, garantizando que el modelo base sus explicaciones en el historial real y estime correctamente su nivel de confianza.
- **RF-08 (Dashboard y SHAP)**: Utilizar SHAP (*SHapley Additive exPlanations*) complementa las métricas de evaluación tradicionales al transformar las predicciones opacas en justificaciones transparentes e interpretables, alimentando el panel de control de forma determinística.

### 3.2. Validación de los Requisitos No Funcionales (RNF)

- **RNF-01 y RNF-04 (Rendimiento y Escalabilidad en CPU)**: La extracción de características tabulares combinada con algoritmos basados en árboles de decisión justifica plenamente la capacidad de procesar 2 millones de interacciones en minutos sobre una CPU de 16GB, erradicando la dependencia de hardware costoso (GPU) para la primera fase de inferencia.
- **RNF-02 y RNF-05 (Costo y Privacidad)**: El diseño en cascada (*Online Cascade Learning*) garantiza que el grueso de los datos nunca abandone el entorno local. Al enviar un máximo del 15% del tráfico anómalo a la API, los costos operativos se mantienen por debajo del presupuesto de $5 USD mensuales.
- **RNF-03 (Precisión F1 >= 0.80)**: Este objetivo es científicamente viable. Investigaciones en la industria bancaria y de telecomunicaciones demuestran que los clasificadores ligeros entrenados sobre características heurísticas del diálogo superan rutinariamente un F1-Score de 0.80 en la detección de frustración.
- **RNF-06 (Mantenibilidad con DVC)**: La integración de Control de Versiones de Datos (DVC) es un componente imperativo para rastrear linajes complejos, permitiendo revertir con confianza a versiones anteriores si se degrada el rendimiento durante la iteración.

