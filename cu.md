Para verificar el rediseño completo, la ingesta nativa y el comportamiento reactivo global del umbral, puedes seguir esta guía de Casos de Uso        
  estructurada como Acción ➔ Resultado Esperado.                                                                                                        
  ──────                                                                                                                                                
  ### 🧪 Caso de Uso 1: Ingesta de Nuevas Conversaciones en Caliente (Drag-and-Drop)                                                                    
                                                                                                                                                        
  Este caso de uso prueba que el pipeline ETL real en memoria funciona desde la interfaz y recarga los datos sin necesidad de reiniciar el servidor.    
                                                                                                                                                        
   # │ Acciones del Usuario                                                   │ Resultado Esperado (Detallado a Nivel de Usuario)
  ───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
   1 │ En el sidebar (panel izquierdo), haz clic en el botón azul Cargar      │ Se abrirá un modal de fondo oscuro ( #1a2d42 ) titulado "Carga e        
     │ CSV/JSON.                                                              │ Ingesta de Conversaciones".
   2 │ Arrastra el archivo de prueba  conversaciones_es.csv  (o cualquier CSV │ El nombre del archivo aparecerá debajo con letras verdes ( #76ff03 ) en 
     │ de conversaciones en  data/raw/ ) a la zona de arrastre punteada, o    │ la sección Archivos Seleccionados.
     │ haz clic en ella para buscarlo y seleccionarlo.                        │
   3 │ Haz clic en el botón Procesar Ingesta.                                 │ 1. Aparecerá un spinner animado cian junto al texto "Ejecutando         
     │                                                                        │ pipeline ETL real en memoria..." mientras el sistema ejecuta las 24     
     │                                                                        │ heurísticas de extracción y realiza la predicción.2. El modal se        
     │                                                                        │ cerrará automáticamente al finalizar.3. El panel de la izquierda se     
     │                                                                        │ actualizará y verás el archivo procesado autoseleccionado en el         
     │                                                                        │ selector ARCHIVO DE INFERENCIA. Todos los KPI superiores y tendencias   
     │                                                                        │ se actualizarán instantáneamente con los nuevos datos cargados.
  ──────                                                                                                                                                
  ### 🧪 Caso de Uso 2: Filtrado Reactivo del Umbral de Frustración                                                                                     
                                                                                                                                                        
  Este caso de uso prueba que el slider de frustración filtra dinámicamente todo el sistema en tiempo real y gestiona la visualización de forma         
  inteligente.                                                                                                                                          
                                                                                                                                                        
   # │ Acciones del Usuario                                                   │ Resultado Esperado (Detallado a Nivel de Usuario)
  ───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
   1 │ Selecciona la pestaña Diagnóstico en la navegación del sidebar. En el  │ 1. La barra de Confidence Score de la conversación elegida se cargará   
     │ selector de diálogos, elige una conversación que tenga un score        │ con su porcentaje en cian brillante.2. Verás el chat de esa             
     │ moderado (ej.  CONV_03  con un score de frustración de  55% ). Mueve   │ conversación con burbujas de diseño oscuro y el razonamiento detallado  
     │ el slider de Umbral Frustración a  50.0% .                             │ del LLM.3. El dropdown mostrará todas las conversaciones del dataset    
     │                                                                        │ que tengan un score $\ge 50\%$.
   2 │ Mueve el slider de Umbral Frustración a  70.0%  (incrementando el      │ 1. El dropdown de conversaciones se contraerá instantáneamente,         
     │ límite de criticidad).                                                 │ eliminando las conversaciones que tienen puntuaciones entre  50%  y     
     │                                                                        │ 69% . 2. Dado que tu conversación activa ( 55% ) ahora quedó excluida   
     │                                                                        │ por el nuevo umbral, la UI no se romperá: de forma automática se        
     │                                                                        │ seleccionará y visualizará el primer caso crítico disponible que sí     
     │                                                                        │ cumpla con $\ge 70\%$ (ej. un caso con  85%  de frustración),           
     │                                                                        │ actualizando el chat, el CoT y la línea de tiempo.
   3 │ Mueve el slider de Umbral Frustración a  100.0% .                      │ 1. Al no haber ninguna conversación con frustración perfecta del 100%,  
     │                                                                        │ el dropdown de casos quedará vacío.2. El visor de chat y diagnóstico    
     │                                                                        │ mostrará elegantemente el texto "No hay datos." y "No hay diagnóstico   
     │                                                                        │ disponible." sin lanzar ningún error de consola.
  ──────                                                                                                                                                
  ### 🧪 Caso de Uso 3: Heatmap e Intenciones Dinámicas                                                                                                 
                                                                                                                                                        
  Este caso de uso prueba que el heatmap y las prioridades estratégicas se calculan dinámicamente según la intersección de volumen y frustración en el  
  subconjunto filtrado.                                                                                                                                 
                                                                                                                                                        
   # │ Acciones del Usuario                                                   │ Resultado Esperado (Detallado a Nivel de Usuario)
  ───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
   1 │ Mueve el slider de Umbral Frustración de vuelta a  0.0%  (para ver el  │ 1. El gráfico Heatmap mostrará la intensidad total con bloques de
     │ panorama completo) y selecciona la pestaña Intenciones en la           │ colores que van del azul oscuro (frustración baja) al rojo ardiente
     │ navegación.                                                            │ (frustración crítica) para todas las categorías (Tarjeta, Clave, Saldo,
     │                                                                        │ etc.).2. El cuadro de Prioridad Estratégica Automática (Crucial) en la
     │                                                                        │ parte inferior identificará de forma dinámica qué categoría genera el
     │                                                                        │ mayor impacto negativo combinando volumen y frustración.
   2 │ Observa la tabla de Flujos Fallidos Críticos del panel derecho y el    │ 1. El Heatmap eliminará los bloques de baja intensidad (scores menores
     │ cuadro de Prioridad Estratégica abajo. Ahora, sube el slider a  60.0%  │ a 60), mostrando celdas únicamente en las zonas calientes
     │ .                                                                      │ (rojas/naranjas).2. La tabla derecha filtrará las categorías eliminando
     │                                                                        │ las filas de bajo riesgo.3. El texto del cuadro de Prioridad
     │                                                                        │ Estratégica se reescribirá en tiempo real para enfocarse únicamente en
     │                                                                        │ el flujo crítico sobreviviente del filtro, recalculando el porcentaje
     │                                                                        │ de frustración promedio y el Performance Boost de mejora esperada.
+-



  ### 🧪 Caso de Uso 1 (Corregido): Ingesta Nativa Drag-and-Drop                                                                                        
                                                                                                                                                        
  Este caso de uso valida que los archivos se carguen y procesen correctamente y que la lista de selección se limpie en el momento justo.               
                                                                                                                                                        
   # │ Acciones del Usuario                                                   │ Resultado Esperado (Nivel Usuario)
  ───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
   1 │ Abre el panel Cargar CSV/JSON en el sidebar. Selecciona el archivo     │ El archivo aparece en el listado de archivos seleccionados.
     │ original  conversaciones_es.csv  (o cualquier otro archivo de          │                                                                         
     │ data/raw/ ).                                                           │
   2 │ Haz clic en Procesar Ingesta.                                          │ 1. Verás el indicador animado "Ejecutando pipeline ETL real en          
     │                                                                        │ memoria..." durante unos segundos.2. Al finalizar, el modal se cerrará  
     │                                                                        │ automáticamente.3. El listado de archivos en el navegador se limpiará   
     │                                                                        │ correctamente (ya no aparecerá el archivo seleccionado en verde) y la   
     │                                                                        │ interfaz de usuario se actualizará cargando los resultados.
  ──────                                                                                                                                                
  ### 🧪 Caso de Uso 4: Carga y Procesamiento Dinámico de Datos Sin Pagos                                                                               
                                                                                                                                                        
  Este caso de uso valida la agilidad del sistema para autogenerar categorías, heatmap, tablas y resúmenes de prioridad en base a un tema totalmente    
  diferente (sin pagos ni tarjetas).                                                                                                                    
                                                                                                                                                        
   # │ Acciones del Usuario                                                   │ Resultado Esperado (Nivel Usuario)
  ───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
   1 │ En el modal Cargar CSV/JSON, selecciona y carga el nuevo archivo de    │ El sistema ejecutará el pipeline en memoria y creará un archivo         
     │ prueba generado:                                                       │ procesado con el nombre  conversaciones_sin_pagos.parquet  en           
     │ C:\Users\opaye\Proyectos\SC\data\raw\conversaciones_sin_pagos.csv .    │ data/processed/ , autoseleccionándolo en el dashboard.
     │ Haz clic en Procesar Ingesta.                                          │
   2 │ Selecciona la pestaña Dashboard (Visión General).                      │ El número de Conversaciones Evaluadas se actualizará a  3  (los 3 casos 
     │                                                                        │ del nuevo CSV). Las tendencias (Sparklines) se adaptarán en tiempo real 
     │                                                                        │ al comportamiento de estos 3 casos.
   3 │ Ve a la pestaña Diagnóstico. Abre el selector de conversaciones.       │ El selector solo mostrará las conversaciones del nuevo archivo (        
     │                                                                        │ CONV_S01 ,  CONV_S02 ,  CONV_S03 ). Al seleccionar  CONV_S01  verás el
     │                                                                        │ chat de restablecimiento de claves y el razonamiento del LLM enfocado
     │                                                                        │ en el bloqueo de accesos y la molestia de las claves.
   4 │ Dirígete a la pestaña Intenciones con el Umbral Frustración en  0.0% . │ 1. Eje Y del Heatmap: Las categorías antiguas relacionadas con tarjetas
     │                                                                        │ y pagos habrán desaparecido. Ahora el Heatmap mostrará dinámicamente en
     │                                                                        │ el eje Y:  Consulta Saldo ,  Seguridad/Claves  y  General .2. Tabla de
     │                                                                        │ Flujos: Solo listará las intenciones detectadas en este nuevo archivo
     │                                                                        │ con sus respectivos volúmenes (1 caso para cada una).
   5 │ En la pestaña Intenciones, revisa la tarjeta Prioridad Estratégica     │ El algoritmo de ponderación identificará automáticamente que la mayor
     │ Automática (Crucial) en la parte inferior.                             │ prioridad es  Seguridad/Claves  (ya que es la única con un score de
     │                                                                        │ frustración alto del 75.0% y volumen 1), reescribiendo el texto en
     │                                                                        │ caliente: "La intención 'Seguridad/Claves' representa la mayor
     │                                                                        │ prioridad de optimización con un volumen de 1 casos y una frustración
     │                                                                        │ promedio del 75.0%..."

─────────────────────────────────────────────────────────────────────────────────────
### 🧪 Caso de Uso 5: Configuración MLOps e In-App File Explorer Dialog                                                                              

Este caso de uso valida la correcta interacción de la pantalla de configuración MLOps (Capa Rápida y Capa Profunda), el uso del in-app Folder Picker
Dialog para autocompletar rutas locales de modelos y las alertas de consistencia de APIs.

 # │ Acciones del Usuario                                                   │ Resultado Esperado (Nivel Usuario)
───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
 1 │ En el sidebar, selecciona la pestaña Configuración.                    │ Se mostrará la interfaz de Configuración MLOps de Modelos con 3 tarjetas:
   │                                                                        │ Embeddings, Capa Rápida y Capa Profunda.
 2 │ En la tarjeta de la Capa Rápida, haz clic en el icono de carpeta       │ Se abrirá el modal "Explorador de Archivos Local" listando el directorio
   │ (folder-open) junto al campo de la ruta del modelo.                    │ actual del workspace del backend.
 3 │ En el modal, haz doble clic o navega en las carpetas para entrar a      │ El input del modelo de Capa Rápida se autocompletará con la ruta absoluta
   │  models/  y selecciona el archivo  lgbm_model.pkl .                    │ del archivo PKL seleccionado y el modal se cerrará automáticamente.
 4 │ En la tarjeta de la Capa Profunda, selecciona como tipo de ejecución:  │ Aparecerán los botones de selección rápida de modelos recomendados de
   │ "API (Google GenAI)". Haz clic en el botón  gemini-2.5-flash .         │ Gemini. El input del modelo cambiará a  gemini-2.5-flash  sin alertas.
 5 │ Cambia manualmente el valor del input del modelo a  gpt-4o-mini .      │ Aparecerá debajo una alerta roja de advertencia de consistencia indicando
   │                                                                        │ que los modelos de Google deben comenzar con "models/gemini-" o "gemini-".
 6 │ Corrige haciendo clic en el botón  gemini-3.5-flash .                  │ El input se actualizará correctamente y la alerta roja desaparecerá.
 7 │ Cambia la Capa Profunda a "API (OpenRouter)" e ingresa en el modelo    │ Aparecerá una alerta roja de consistencia avisando que en OpenRouter no
   │ el valor  models/deepseek-chat .                                       │ se debe utilizar el prefijo  models/ .
 8 │ Haz clic en el botón sugerido  DeepSeek Chat .                         │ El modelo cambiará a  deepseek/deepseek-chat  y la alerta roja
   │                                                                        │ desaparecerá de inmediato.
 9 │ Introduce tu API key en el campo respectivo y haz clic en la sección   │ Se confirmará que los cambios se aplicarán en el próximo reprocesamiento
   │ de abajo: "Aplicar Configuración de Arquitectura".                     │ de datos y la configuración quedará almacenada en la sesión del servidor.
──────                                                                                                                                              
### 🧪 Caso de Uso 6: Diagnóstico de Explicabilidad SHAP y Validación Twin-Pass                                                                       

Este caso de uso valida que el usuario puede analizar el porqué de una clasificación de frustración a través de las variables locales (SHAP)
y la explicación del LLM verificada por la arquitectura de doble pasada (Twin-Pass).

 # │ Acciones del Usuario                                                   │ Resultado Esperado (Nivel Usuario)
───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
 1 │ Dirígete a la pestaña Diagnóstico y selecciona una conversación que    │ 1. Se cargará el chat correspondiente con burbujas de diseño oscuro.
   │ tenga un nivel alto de frustración (ej.  CONV_03  con  75% ).          │ 2. En el panel "Explicabilidad Local (SHAP)" verás el impacto de las
   │                                                                        │ variables del diálogo que influyeron en la clasificación (ej. número de
   │                                                                        │ fallos seguidos del bot, mayúsculas del usuario).
 2 │ Pasa el mouse o inspecciona las barras de características en el panel  │ Se visualizará qué variables agregaron valor positivo al score (color rojo)
   │ de SHAP.                                                               │ u omitieron criticidad (color azul), justificando matemáticamente la
   │                                                                        │ decisión de la Capa Rápida (LightGBM).
 3 │ Lee la sección "Razonamiento Cognitivo (Second Pass)" generada por el  │ Verás una explicación textual del flujo que llevó al usuario a la molestia,
   │ LLM en el panel derecho.                                               │ redactada bajo la técnica Chain-of-Thought (CoT).
 4 │ Localiza el indicador de Validación Twin-Pass junto al texto.          │ El indicador mostrará la etiqueta verde  ✓ Verificado (Confianza Alta) 
   │                                                                        │ confirmando que la doble pasada de verificación no detectó alucinaciones
   │                                                                        │ y que la justificación coincide con los datos históricos reales.
──────                                                                                                                                              
### 🧪 Caso de Uso 7: Simulación de Casos Complejos (Sarcasmo y Abandono Silencioso)                                                                 

Este caso de uso valida la capacidad del enrutamiento híbrido para detectar y clasificar correctamente tipos sofisticados de frustración como
sarcasmo y abandono sin insultos directos.

 # │ Acciones del Usuario                                                   │ Resultado Esperado (Nivel Usuario)
───┼────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────
 1 │ En el modal de carga, sube un archivo que contenga casos avanzados     │ El pipeline en memoria procesará el archivo y actualizará el dashboard.
   │ (ej. sarcasmo y abandono silencioso) y procesa la ingesta.             │
 2 │ Ve a la pestaña Diagnóstico y selecciona la conversación con sarcasmo  │ El sistema mostrará que LightGBM detectó un score intermedio, cayendo en
   │ (ej. "¡Excelente! Me borraron la cuenta, son los mejores.").           │ la Zona Gris (0.45 - 0.75), lo que derivó el caso de forma transparente al
   │                                                                        │ LLM. El LLM clasificó el caso como "Frustrada (1)" explicando el sarcasmo.
 3 │ En el selector, elige la conversación con abandono silencioso (el bot  │ El sistema registrará la frustración del usuario en base a las variables
   │ falla reiteradamente y el usuario corta la conversación sin despedirse)│ heurísticas de abandono. El gráfico SHAP mostrará alta contribución de las
   │                                                                        │ métricas de inactividad del usuario y fallos del bot.
─────────────────────────────────────────────────────────────────────────────────────