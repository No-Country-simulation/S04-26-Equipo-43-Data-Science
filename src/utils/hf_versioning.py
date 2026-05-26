import os
from huggingface_hub import HfApi
from dotenv import load_dotenv
from src.utils.logger import logger

def upload_to_huggingface():
    """
    Sube los artefactos clave del proyecto (Modelo y Datos Procesados) 
    al Hugging Face Hub, reemplazando la necesidad de DVC local.
    """
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    
    if not hf_token:
        logger.error("HF_TOKEN no encontrado en el archivo .env")
        return

    # IMPORTANTE: Reemplaza 'FerpayeC1' con tu usuario real si es diferente
    USERNAME = "FerpayeC1" 
    MODEL_REPO = f"{USERNAME}/conversasense-lgbm"
    DATA_REPO = f"{USERNAME}/conversasense-data"

    api = HfApi(token=hf_token)

    logger.info("Iniciando versionado en Hugging Face Hub...")

    try:
        # 1. Subir el Modelo LightGBM
        model_path = "models/lgbm_model.pkl"
        if os.path.exists(model_path):
            logger.info(f"Subiendo {model_path} a {MODEL_REPO}...")
            api.upload_file(
                path_or_fileobj=model_path,
                path_in_repo="lgbm_model.pkl",
                repo_id=MODEL_REPO,
                repo_type="model"
            )
            logger.info("✅ Modelo subido exitosamente.")
        else:
            logger.warning(f"No se encontró el modelo en {model_path}")

        # 2. Subir los Datos Procesados (Dataset Parquet)
        data_path = "data/processed/features_S1.parquet"
        if os.path.exists(data_path):
            logger.info(f"Subiendo {data_path} a {DATA_REPO}...")
            api.upload_file(
                path_or_fileobj=data_path,
                path_in_repo="features_S1.parquet",
                repo_id=DATA_REPO,
                repo_type="dataset"
            )
            logger.info("✅ Dataset Parquet subido exitosamente.")
        else:
            logger.warning(f"No se encontraron los datos en {data_path}")

    except Exception as e:
        logger.error(f"Error durante la subida a Hugging Face: {e}")
        logger.info("Asegúrate de que los repositorios 'conversasense-lgbm' (Model) y 'conversasense-data' (Dataset) existan en tu cuenta de HF.")

if __name__ == "__main__":
    upload_to_huggingface()
