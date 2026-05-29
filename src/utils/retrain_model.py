import os
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Añadir la raíz del proyecto al path para resolver las importaciones de src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.logger import logger
from src.core.frustration_classifier import FrustrationClassifier
from src.core.explainability import SHAPExplainer
from src.utils.hf_versioning import upload_to_huggingface

def main():
    load_dotenv()
    logger.info("--- Iniciando Reentrenamiento de Clasificador de Frustración (LightGBM) ---")
    
    # 1. Cargar el dataset de características procesadas
    data_path = "data/processed/conversaciones_generadas_gemini.parquet"
    
    if not os.path.exists(data_path):
        logger.error(f"No se encontró el dataset generado en {data_path}")
        logger.info("Por favor, asegúrate de ejecutar primero la generación de datos: src/utils/data_generator_llm.py")
        sys.exit(1)
        
    logger.info(f"Cargando dataset de entrenamiento desde: {data_path}")
    df_features = pd.read_parquet(data_path)
    
    if 'is_frustrated' not in df_features.columns:
        logger.error("El dataset no contiene la columna objetivo 'is_frustrated'.")
        sys.exit(1)
        
    logger.info(f"Dataset cargado con éxito. Dimensiones: {df_features.shape}")
    logger.info(f"Distribución del target 'is_frustrated':\n{df_features['is_frustrated'].value_counts(normalize=True)}")
    
    # 2. Entrenar el FrustrationClassifier con Validación Cruzada
    classifier = FrustrationClassifier()
    
    # Ajustamos CV a 5 folds
    logger.info("Entrenando clasificador LightGBM con Stratified 5-Fold Cross Validation...")
    metrics = classifier.train(df_features, target_col='is_frustrated', cv=5)
    
    logger.info(f"Reentrenamiento completado con éxito.")
    logger.info(f"Métricas finales promedio: F1-Score={metrics['f1']:.4f}, AUC-ROC={metrics['auc']:.4f}, Accuracy={metrics['accuracy']:.4f}")
    
    # 3. Generar Explicabilidad con SHAP
    logger.info("Actualizando explicador SHAP con el nuevo modelo reentrenado...")
    explainer = SHAPExplainer(classifier.model, classifier.features_cols)
    
    # Generar y guardar el gráfico de resumen SHAP
    shap_plot_path = "data/processed/shap_summary.png"
    explainer.generate_summary_plot(df_features, shap_plot_path)
    logger.info(f"Gráfico SHAP actualizado y guardado en: {shap_plot_path}")
    
    # 4. Sincronizar automáticamente con Hugging Face Hub si se cuenta con token
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        logger.info("HF_TOKEN detectado. Iniciando sincronización de artefactos con Hugging Face Hub...")
        try:
            # Primero nos aseguramos de que hf_versioning suba la versión correcta
            # Modificamos temporalmente el comportamiento si queremos subir conversaciones_generadas_gemini.parquet en lugar de features_S1.parquet
            # Pero dado que hf_versioning usa features_S1.parquet, podemos hacer una copia o subirlo directamente
            import shutil
            shutil.copyfile(data_path, "data/processed/features_S1.parquet")
            logger.info("Copiado conversaciones_generadas_gemini.parquet a features_S1.parquet para sincronización con Hugging Face.")
            
            upload_to_huggingface()
            logger.info("✅ Artefactos sincronizados con Hugging Face Hub correctamente.")
        except Exception as e:
            logger.error(f"Error sincronizando con Hugging Face Hub: {e}")
    else:
        logger.warning("HF_TOKEN no configurado en el archivo .env. Sincronización omitida.")
        
    print("\n¡Proceso de reentrenamiento completado! El clasificador ya está utilizando las nuevas señales y diálogos generados por Gemini.")

if __name__ == "__main__":
    main()
