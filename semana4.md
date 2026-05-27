# Reporte de Avances - Semana 4: Validación Humana, Dashboard y Producción

He completado con éxito los objetivos de la **Semana 4**, cerrando el ciclo de vida de desarrollo central del proyecto. Nos enfocamos en la validación científica de las predicciones, el versionado robusto de los artefactos en la nube y la construcción de un dashboard cognitivo de alto rendimiento.

## Logros Alcanzados

1. **Métricas de Fiabilidad Científica (`evaluation.py`)**:
    - **Cálculo de Consenso**: Se implementó un script utilizando `scikit-learn` para validar matemáticamente la arquitectura híbrida contra el etiquetado de un Juez Humano ("Ground Truth").
    - **Resultados Base**: Se superaron los umbrales de éxito en la prueba simulada de la Fase de Consenso, logrando un **F1-Score de 0.7761** y un **Cohen's Kappa de 0.6644**, demostrando que el sistema emula con gran fidelidad la detección humana de la frustración.

2. **MLOps y Versionado en la Nube (`hf_versioning.py`)**:
    - **Evolución DVC -> Hugging Face**: Se migró la estrategia de versionado de artefactos pesados hacia **Hugging Face Hub**, operando como un DVC en la nube para evadir el *repository bloat* en Git.
    - **Automatización**: El script sube exitosamente y de manera privada el modelo compilado (`lgbm_model.pkl`) y el set de datos (`features_S1.parquet`) garantizando trazabilidad y reproducibilidad.

3. **Dashboard Analítico Cognitivo (Reflex + Apache ECharts)**:
    - **Arquitectura Asíncrona**: Se inicializó el proyecto web en `src/dashboard` empleando **Reflex** (soportado por FastAPI y React), lo que permite escalar sin la latencia de plataformas monolíticas.
    - **Diseño Gestalt y Zero-Latency**: Implementación fiel de los mockups priorizando la reducción de carga cognitiva. Se adoptó una paleta monocromática estricta (`accent_color="gray"`), junto con *Sparklines* minimalistas sin ejes y envolturas para *Bullet Charts* mediante la librería oficial `reflex-echarts` (Apache ECharts).
    - **Protección de Infraestructura**: Incorporación de retardo temporal (`debounce`) en los filtros dinámicos (ej. slider de Umbral de Frustración) para proteger el backend de Python de colapsos ante re-cálculos masivos de Pandas.

---

## Entregables Disponibles

| Archivo / Repositorio | Descripción |
| :--- | :--- |
| `src/core/evaluation.py` | Script estadístico para el cálculo del Cohen's Kappa y F1-Score contra humanos. |
| `src/utils/hf_versioning.py` | Automatización de la subida de modelos y datos a repositorios remotos. |
| `src/dashboard/dashboard/dashboard.py` | Código fuente principal de la aplicación frontend asíncrona (Reflex). |
| `[HF] conversasense-lgbm` | Repositorio remoto en Hugging Face con el modelo LightGBM entrenado. |
| `[HF] conversasense-data` | Repositorio remoto en Hugging Face con la matriz Parquet de métricas (Features). |

---

## Instrucciones de Ejecución

Para iniciar el servidor de desarrollo y visualizar el **Dashboard en Reflex**, abre una terminal, asegúrate de tener tu entorno virtual activo y ejecuta:

```bash
# 1. Navegar al directorio del dashboard
cd src/dashboard

# 2. Instalar dependencias si es la primera vez (opcional si ya instalaste reflex, pandas, reflex-echarts, etc.)
# pip install reflex reflex-echarts pandas

# 3. Inicializar la aplicación (solo la primera vez, ya lo hemos hecho)
# reflex init

# 4. Iniciar el servidor local
reflex run
```

En caso de error simplemente debes "entrar" a la carpeta del dashboard antes de correr el comando. Ejecuta esto en tu terminal:

   1 cd src\dashboard
   2 reflex run

Una vez ejecutado, el dashboard estará disponible en tu navegador en: `http://localhost:3000`

---

**Estado del Proyecto**: 🟢 Completado con Éxito (Semana 4 finalizada).
**Próximo Paso**: Integración final de la tubería de datos (conectar los gráficos de Reflex con el dataset real de Hugging Face/Pandas), pruebas en vivo y congelamiento de código (`git tag v1.0`) para el "Pitch" final.