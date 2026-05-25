import pandas as pd
import os
from src.core.ingest_adapter import IngestAdapter
from src.core.feature_extractor import FeatureExtractor
from src.core.feature_aggregator import FeatureAggregator

def test_pipeline():
    # 1. Crear datos sintéticos realistas
    data = [
        {"id_conv": "C1", "turno": 1, "rol": "user", "mensaje": "Hola, necesito ayuda con mi pedido"},
        {"id_conv": "C1", "turno": 2, "rol": "bot", "mensaje": "Hola, ¿en qué puedo ayudarte?"},
        {"id_conv": "C1", "turno": 3, "rol": "user", "mensaje": "MI PEDIDO NO LLEGA!!!!!"},
        {"id_conv": "C1", "turno": 4, "rol": "bot", "mensaje": "Lo siento, no he entendido. ¿Puedes repetir?"},
        {"id_conv": "C1", "turno": 5, "rol": "user", "mensaje": "QUIERO HABLAR CON UN AGENTE YA"},
        
        {"id_conv": "C2", "turno": 1, "rol": "user", "mensaje": "Quero saber meu saldo"},
        {"id_conv": "C2", "turno": 2, "rol": "bot", "mensaje": "Seu saldo é R$ 100,00"},
        {"id_conv": "C2", "turno": 3, "rol": "user", "mensaje": "Obrigado"},
        {"id_conv": "C2", "turno": 4, "rol": "bot", "mensaje": "De nada, tchau!"}
    ]
    
    df_test = pd.DataFrame(data)
    test_csv = "data/raw/pipeline_test.csv"
    os.makedirs("data/raw", exist_ok=True)
    df_test.to_csv(test_csv, index=False, encoding="utf-8")
    
    # 2. Ingesta
    adapter = IngestAdapter()
    df_ingested = adapter.load_csv(test_csv)
    
    # 3. Extracción de Features
    extractor = FeatureExtractor()
    df_msg = extractor.extract_message_features(df_ingested)
    df_msg = extractor.extract_bot_signals(df_msg)
    df_msg = extractor.compute_semantic_coherence(df_msg)
    
    # 4. Agregación
    aggregator = FeatureAggregator()
    df_final = aggregator.aggregate_conversation_features(df_msg)
    
    # 5. Resultados
    print("\n--- Pipeline Completo ---")
    print(f"Conversaciones procesadas: {len(df_final)}")
    print("\nFeatures por conversación:")
    print(df_final.T) # Transponer para ver mejor las columnas
    
    # Guardar en Parquet (Entregable de la semana 1)
    os.makedirs("data/processed", exist_ok=True)
    df_final.to_parquet("data/processed/features_S1.parquet")
    print("\nArchivo Parquet generado en data/processed/features_S1.parquet")

if __name__ == "__main__":
    test_pipeline()
