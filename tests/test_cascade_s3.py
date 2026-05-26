import pandas as pd
import os
import sys

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.ingest_adapter import IngestAdapter
from src.core.feature_extractor import FeatureExtractor
from src.core.feature_aggregator import FeatureAggregator
from src.core.cascade_orchestrator import CascadeOrchestrator
from dotenv import load_dotenv

# Cargar variables de entorno al inicio
load_dotenv()

def test_full_cascade():
    # 1. Datos de prueba con casos claros y grises
    data = [
        # Caso 1: Muy frustrado (Gritos, repetición, bot no entiende)
        {"id_conv": "FRUST_01", "turno": 1, "rol": "user", "mensaje": "Hola"},
        {"id_conv": "FRUST_01", "turno": 2, "rol": "bot", "mensaje": "Hola, ¿en qué puedo ayudarte?"},
        {"id_conv": "FRUST_01", "turno": 3, "rol": "user", "mensaje": "QUIERO MI REEMBOLSO YA NO SIRVE NADA"},
        {"id_conv": "FRUST_01", "turno": 4, "rol": "bot", "mensaje": "Lo siento, no he entendido. ¿Puedes repetir?"},
        {"id_conv": "FRUST_01", "turno": 5, "rol": "user", "mensaje": "ERES INÚTIL PÁSAME CON UN HUMANO!!!!!!"},
        
        # Caso 2: Neutral (Consulta simple)
        {"id_conv": "NEUT_01", "turno": 1, "rol": "user", "mensaje": "Hola, ¿cuál es el horario?"},
        {"id_conv": "NEUT_01", "turno": 2, "rol": "bot", "mensaje": "Abrimos de 9 a 18 hs."},
        {"id_conv": "NEUT_01", "turno": 3, "rol": "user", "mensaje": "Gracias, muy amable."},
        
        # Caso 3: Zona Gris (Sarcasmo o frustración leve)
        {"id_conv": "GRAY_01", "turno": 1, "rol": "user", "mensaje": "Mi pedido llegó roto"},
        {"id_conv": "GRAY_01", "turno": 2, "rol": "bot", "mensaje": "Entiendo, envíanos una foto."},
        {"id_conv": "GRAY_01", "turno": 3, "rol": "user", "mensaje": "Qué maravilla de servicio, siempre igual..."},
    ]
    
    df_raw = pd.DataFrame(data)
    
    # 2. Pipeline de Features
    extractor = FeatureExtractor()
    df_msg = extractor.extract_message_features(df_raw)
    df_msg = extractor.extract_bot_signals(df_msg)
    df_msg = extractor.compute_semantic_coherence(df_msg)
    
    aggregator = FeatureAggregator()
    df_features = aggregator.aggregate_conversation_features(df_msg)
    
    # 3. Generar Historiales para el LLM
    histories = {}
    for cid, group in df_raw.groupby("id_conv"):
        hist = "\n".join([f"{r}: {m}" for r, m in zip(group['rol'], group['mensaje'])])
        histories[cid] = hist
        
    # 4. Orquestación
    # Usamos tau_low alto para forzar escalación en el test si no hay modelo entrenado con estos datos
    orchestrator = CascadeOrchestrator(tau_low=0.1, llm_provider="gemini")
    
    print("\n--- 🌊 Iniciando Inferencia en Cascada ---")
    results = orchestrator.run_inference(df_features, histories)
    
    print("\n--- 📊 Resultados Finales ---")
    output_cols = ['id_conv', 'frustration_probability', 'final_is_frustrated', 'layer_used', 'final_reasoning']
    print(results[output_cols])

if __name__ == "__main__":
    # Asegúrate de tener las llaves en el .env antes de correr esto
    if os.getenv("GEMINI_API_KEY") or os.getenv("OPENROUTER_API_KEY"):
        test_full_cascade()
    else:
        print("⚠️  Skipping test: No API keys found in .env")
