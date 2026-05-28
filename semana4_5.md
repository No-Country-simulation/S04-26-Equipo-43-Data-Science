 El plan  plan_final.md  ha sido aplicado con éxito y el proyecto compila perfectamente. A continuación se detallan los cambios realizados y los pasos 
  para su validación.                                                                                                                                   
  ──────                                                                                                                                                
  ### Resumen de Cambios Realizados                                                                                                                     
                                                                                                                                                        
  1. Estética Enterprise Dark Mode (dashboard.py y rxconfig.py):                                                                                   
      • Se configuró Radix Themes para usar por defecto la apariencia  dark  y el color de acento  cyan .                                               
      • Se implementaron los tokens de color del mockup: fondos  #0f1923  (base) /  #152232  (sidebar), tarjetas de datos  #1a2d42  /  #1e3448 , y      
      acentos cian ( #00e5ff ), lima ( #76ff03 ), naranja ( #ff6d00 ), y rojo ( #ff1744 ).                                                              
      • Se aplicó la fuente de Google Fonts  Inter  globalmente y se añadió un logo decorativo en absoluto ("sparkle") en la esquina inferior derecha.  
  2. Visualizaciones Dinámicas:                                                                                                                         
      • Matriz Intención × Frustración: Se reemplazó el heatmap estático por un  @rx.var  dinámico ( heatmap_option ) que lee las intenciones únicas del
      parquet activo y las mapea contra deciles de frustración, utilizando un gradiente cálido/frío.                                                    
      • Sparklines de Sentimiento: Las tendencias de Positivo, Neutral y Frustración calculan promedios dinámicos en 9 bins cronológicos.               
      • Atribución Global SHAP: Se implementó un bar-chart dinámico con gradiente cian-lima que muestra el impacto de las variables de diálogo en la    
      predicción.                                                                                                                                       
      • Línea de Tiempo Visual: En la vista de Diagnóstico, se renderizan dinámicamente nodos User (cian) y Bot (gris) alternados, conectados por una   
      línea y finalizando en una alerta visual de Falla (rojo con brillo).                                                                              
  3. Carga Drag-and-Drop Nativa:                                                                                                                        
      • Se integró un modal nativo  rx.dialog.root  con un componente  rx.upload .                                                                      
      • Al hacer clic en "Procesar Ingesta", el backend ejecuta en memoria el pipeline ETL real ( IngestAdapter  →  FeatureExtractor  →                 
      FeatureAggregator  →  CascadeOrchestrator ), guarda el parquet en  data/processed/ , lo auto-selecciona y refresca la UI en caliente mostrando un 
      estado de carga ( is_uploading ).                                                                                                                 
  4. Resumen de Prioridades Dinámico:                                                                                                                   
      • El texto bajo "Prioridad Estratégica Automática (Crucial)" se autogenera dinámicamente mediante el cálculo del producto de Volumen × Frustración
      Promedio de cada intención encontrada en el parquet activo.                                                                                       
                                                                                                                                                        
  ──────                                                                                                                                                
  ### Instrucciones de Validación Manual                                                                                                                
                                                                                                                                                        
  Para iniciar el servidor de desarrollo y validar la UI:                                                                                               
                                                                                                                                                        
  1. Iniciar Reflex:                                                                                                                                    
  Abre una consola de PowerShell en tu sistema y ejecuta:                                                                                               
    cd C:\Users\opaye\Proyectos\SC\src\dashboard                                                                                                        
    ..\..\venv\Scripts\reflex.exe run                                                                                                                   
                                                                                                                                                        
  2. Abrir en Navegador:                                                                                                                                
  Navega a http://localhost:3000.                                                                                                                       
  3. Probar Carga Drag-and-Drop:                                                                                                                        
      • En el sidebar, haz clic en Cargar CSV/JSON.                                                                                                     
      • Arrastra un archivo de datos crudos (ej. un CSV con mensajes e identificadores de conversación) o haz clic para seleccionarlo.                  
      • Haz clic en Procesar Ingesta. Verás el indicador de carga y la interfaz se actualizará al finalizar.                                            
  4. Verificar Heatmap y Prioridades:                                                                                                                   
      • Ve a la sección Intenciones.                                                                                                                    
      • Cambia entre archivos de inferencia en el selector y observa cómo el heatmap, el listado de flujos y el resumen de prioridad estratégica cambian
      en tiempo real de acuerdo a los datos del archivo activo.           