import sys
import os
import time
import pandas as pd
import numpy as np

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.ingest_adapter import IngestAdapter
from src.core.feature_extractor import FeatureExtractor
from src.core.feature_aggregator import FeatureAggregator
from src.core.frustration_classifier import FrustrationClassifier
from src.core.explainability import SHAPExplainer

def run_stress_test_volume(n_conversations=1000):
    print(f"\n==========================================")
    print(f"STRESS TEST 1: Volumen y SLA de Inferencia (n={n_conversations} convs)")
    print(f"==========================================")
    
    # 1. Generar lote masivo en memoria
    # Promedio de 5 mensajes por conversación = 5000 mensajes
    data = []
    for i in range(n_conversations):
        cid = f"STRESS_{i:04d}"
        turns = np.random.randint(2, 8)
        for t in range(1, turns + 1):
            rol = "user" if t % 2 != 0 else "bot"
            msg = "Hola necesito ayuda" if rol == "user" else "Disculpa no entendí"
            # Inyectar algo de ruido y frustración
            if i % 10 == 0 and rol == "user":
                msg = "QUIERO HABLAR CON UN AGENTE YA"
            data.append({"id_conv": cid, "turno": t, "rol": rol, "mensaje": msg})
            
    df_raw = pd.DataFrame(data)
    print(f"Dataset generado: {len(df_raw)} mensajes.")
    
    # 2. Medir tiempos de Ingesta (simulada en memoria o guardando en temp)
    temp_csv = "data/raw/temp_stress.csv"
    df_raw.to_csv(temp_csv, index=False, encoding="utf-8")
    
    adapter = IngestAdapter()
    
    t0 = time.time()
    df_ingested = adapter.load_csv(temp_csv)
    t_ingest = time.time() - t0
    print(f"-> Ingesta y Validación Pandera: {t_ingest:.4f} segundos")
    
    # 3. Medir Feature Extraction (Batch)
    extractor = FeatureExtractor()
    t0 = time.time()
    df_msg = extractor.extract_message_features(df_ingested)
    df_msg = extractor.extract_bot_signals(df_msg)
    df_msg = extractor.compute_semantic_coherence(df_msg)
    t_features = time.time() - t0
    print(f"-> Extracción de Features (24 variables per-message + embeddings): {t_features:.4f} segundos")
    
    # 4. Medir Agregación
    aggregator = FeatureAggregator()
    t0 = time.time()
    df_conv = aggregator.aggregate_conversation_features(df_msg)
    t_agg = time.time() - t0
    print(f"-> Agregación Conversacional (23 variables finales): {t_agg:.4f} segundos")
    
    # 5. Medir Inferencia LightGBM
    classifier = FrustrationClassifier()
    # Cargar modelo reentrenado
    classifier.load_model()
    
    t0 = time.time()
    results = classifier.predict(df_conv)
    t_inf = time.time() - t0
    print(f"-> Inferencia LightGBM: {t_inf:.4f} segundos")
    
    t_total = t_ingest + t_features + t_agg + t_inf
    print(f"\nTIEMPO TOTAL PIPELINE: {t_total:.4f} segundos")
    
    # Validar SLA (20k conversaciones < 3 min = 180s. Para 1k debería ser < 15s)
    expected_sla_1k = 15.0
    if t_total < expected_sla_1k:
        print(f"SLA Cumplido. Ritmo proyectado: {(t_total * 20):.2f}s para 20k convs (Meta: <180s)")
    else:
        print(f"SLA Incumplido. Ritmo proyectado: {(t_total * 20):.2f}s para 20k convs")
        
    # Limpieza
    if os.path.exists(temp_csv):
        os.remove(temp_csv)

def run_stress_test_edge_cases():
    print(f"\n==========================================")
    print(f"STRESS TEST 2: Casos Edge y Robustez de Datos")
    print(f"==========================================")
    
    # Caso A: DataFrame vacío
    print("-> Caso A: Ingesta de DataFrame vacío")
    extractor = FeatureExtractor()
    aggregator = FeatureAggregator()
    
    df_empty = pd.DataFrame(columns=["id_conv", "turno", "rol", "mensaje"])
    try:
        df_msg = extractor.extract_message_features(df_empty)
        df_msg = extractor.extract_bot_signals(df_msg)
        df_msg = extractor.compute_semantic_coherence(df_msg)
        df_conv = aggregator.aggregate_conversation_features(df_msg)
        print(f"   Exito. Columnas resultantes: {df_conv.columns.tolist()}")
        print(f"   Shape: {df_conv.shape} (Esquema preservado)")
    except Exception as e:
        print(f"   Fallo: {e}")
        
    # Caso B: Diálogos rotos (Solo Bot, Solo User, Mensajes Nulos)
    print("\n-> Caso B: Diálogos malformados (nulos, un solo rol)")
    data = [
        {"id_conv": "ERR_01", "turno": 1, "rol": "user", "mensaje": np.nan}, # Mensaje Nulo
        {"id_conv": "ERR_02", "turno": 1, "rol": "bot", "mensaje": "Hola"},   # Solo Bot
        {"id_conv": "ERR_03", "turno": 1, "rol": "user", "mensaje": "Hola"},  # Solo User
        {"id_conv": "ERR_03", "turno": 2, "rol": "user", "mensaje": "Hola de nuevo"} # Doble turno User
    ]
    df_broken = pd.DataFrame(data)
    try:
        df_msg = extractor.extract_message_features(df_broken)
        df_msg = extractor.extract_bot_signals(df_msg)
        df_msg = extractor.compute_semantic_coherence(df_msg)
        df_conv = aggregator.aggregate_conversation_features(df_msg)
        print(f"   Exito. Inferencia procesada: {len(df_conv)} conversaciones.")
        print(df_conv[['id_conv', 'total_turns', 'user_message_count', 'avg_cosine_similarity']])
    except Exception as e:
        print(f"   Fallo: {e}")

def run_stress_test_corrupt_dlq(n_conversations=500):
    print(f"\n==========================================")
    print(f"STRESS TEST 3: Ingesta de Datos Corruptos y Aislamiento en DLQ (n={n_conversations} convs)")
    print(f"==========================================")
    
    # 1. Generar datos con fallos de tipo y esquema
    data = []
    for i in range(n_conversations):
        cid = f"DLQ_STRESS_{i:04d}"
        if i % 5 != 0:
            data.append({"id_conv": cid, "turno": 1, "rol": "user", "mensaje": "Consulta normal"})
            data.append({"id_conv": cid, "turno": 2, "rol": "bot", "mensaje": "Respuesta normal"})
        else:
            # Fila corrupta: turno no es número entero, rol es inválido
            data.append({"id_conv": cid, "turno": "turno_invalido", "rol": "invitado", "mensaje": "Mensaje corrupto"})
            
    df_raw = pd.DataFrame(data)
    
    temp_corrupt_csv = "data/raw/temp_corrupt_stress.csv"
    df_raw.to_csv(temp_corrupt_csv, index=False, encoding="utf-8")
    
    adapter = IngestAdapter(dlq_path="data/dlq/stress_errors.parquet")
    
    # Limpiar DLQ viejo si existe
    if os.path.exists("data/dlq/stress_errors.parquet"):
        try:
            os.remove("data/dlq/stress_errors.parquet")
        except:
            pass
        
    print(f"Cargando dataset con filas corruptas ({len(df_raw)} filas)...")
    t0 = time.time()
    df_valid = adapter.load_csv(temp_corrupt_csv)
    t_load = time.time() - t0
    print(f"-> Ingesta procesada en {t_load:.4f} segundos.")
    
    # Verificar si se generaron errores en el DLQ
    if os.path.exists("data/dlq/stress_errors.parquet"):
        df_dlq = pd.read_parquet("data/dlq/stress_errors.parquet")
        print(f"-> Aislamiento DLQ Exitoso. Filas validas: {len(df_valid)}. Filas enviadas al DLQ: {len(df_dlq)}")
        print(f"   Muestra de razones en DLQ:\n{df_dlq['error_reason'].head(2).values}")
    else:
        print("-> Alerta: No se aislaron errores en el DLQ.")
        
    # Limpieza
    if os.path.exists(temp_corrupt_csv):
        os.remove(temp_corrupt_csv)
    if os.path.exists("data/dlq/stress_errors.parquet"):
        try:
            os.remove("data/dlq/stress_errors.parquet")
        except:
            pass

if __name__ == "__main__":
    run_stress_test_volume(1000)
    run_stress_test_edge_cases()
    run_stress_test_corrupt_dlq(500)
