import pandas as pd
import numpy as np
import os
import sys

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.ingest_adapter import IngestAdapter
from src.core.feature_extractor import FeatureExtractor
from src.core.feature_aggregator import FeatureAggregator
from src.core.cascade_orchestrator import CascadeOrchestrator
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("--- Iniciando Pipeline de Inferencia Enriquecida ---")
    
    # 1. Datos realistas con variedad de intenciones y estados de frustración
    data = [
        # Tarjeta Bloqueada (Frustrado)
        {"id_conv": "CONV_01", "turno": 1, "rol": "user", "mensaje": "Hola, mi tarjeta de crédito está bloqueada y no puedo pagar"},
        {"id_conv": "CONV_01", "turno": 2, "rol": "bot", "mensaje": "Hola, disculpa, no he entendido tu consulta. ¿Puedes repetir?"},
        {"id_conv": "CONV_01", "turno": 3, "rol": "user", "mensaje": "QUE MI TARJETA ESTÁ BLOQUEADA!!! necesito ayuda ya"},
        {"id_conv": "CONV_01", "turno": 4, "rol": "bot", "mensaje": "Lo siento, ¿quieres volver al menú principal?"},
        {"id_conv": "CONV_01", "turno": 5, "rol": "user", "mensaje": "No, eres inútil. Pásame con un agente humano urgente!"},
        
        # Consulta Saldo (Neutra - PT)
        {"id_conv": "CONV_02", "turno": 1, "rol": "user", "mensaje": "Oi, gostaria de ver meu saldo da conta corrente"},
        {"id_conv": "CONV_02", "turno": 2, "rol": "bot", "mensaje": "Olá! O seu saldo atual é R$ 1.250,50."},
        {"id_conv": "CONV_02", "turno": 3, "rol": "user", "mensaje": "Muito obrigado pela ajuda"},
        {"id_conv": "CONV_02", "turno": 4, "rol": "bot", "mensaje": "De nada! Tenha um ótimo dia."},
        
        # Clave Olvidada (Zona Gris / Frustración Leve)
        {"id_conv": "CONV_03", "turno": 1, "rol": "user", "mensaje": "Hola, olvidé mi clave de acceso a la app"},
        {"id_conv": "CONV_03", "turno": 2, "rol": "bot", "mensaje": "Disculpa, para recuperar tu clave ingresa tu número de documento."},
        {"id_conv": "CONV_03", "turno": 3, "rol": "user", "mensaje": "Ya lo puse tres veces y sigue dando error... qué desastre de servicio"},
        {"id_conv": "CONV_03", "turno": 4, "rol": "bot", "mensaje": "Lo siento mucho. ¿Quieres que te envíe un link temporal de acceso?"},
        {"id_conv": "CONV_03", "turno": 5, "rol": "user", "mensaje": "Bueno, sí, mándalo rápido por favor"},

        # Pago Servicio (Frustrado)
        {"id_conv": "CONV_04", "turno": 1, "rol": "user", "mensaje": "No puedo pagar mi cuenta de luz, el botón da error 500"},
        {"id_conv": "CONV_04", "turno": 2, "rol": "bot", "mensaje": "No puedo hacer eso por aquí. Intente más tarde."},
        {"id_conv": "CONV_04", "turno": 3, "rol": "user", "mensaje": "Es una mierda de sistema, me van a cortar la luz hoy!"},
        
        # Actualización de Datos (Neutra)
        {"id_conv": "CONV_05", "turno": 1, "rol": "user", "mensaje": "Cómo actualizo mi número de teléfono en el sistema?"},
        {"id_conv": "CONV_05", "turno": 2, "rol": "bot", "mensaje": "Hola. Dirígete a Ajustes -> Perfil -> Teléfono y edita el campo."},
        {"id_conv": "CONV_05", "turno": 3, "rol": "user", "mensaje": "Ah ok, ya lo hice. Muchas gracias."},
        
        # Pago Servicio (Zona Gris - PT)
        {"id_conv": "CONV_06", "turno": 1, "rol": "user", "mensaje": "Não consigo pagar minha fatura com cartão"},
        {"id_conv": "CONV_06", "turno": 2, "rol": "bot", "mensaje": "Desculpe, não entendi. Pode digitar de outra forma?"},
        {"id_conv": "CONV_06", "turno": 3, "rol": "user", "mensaje": "Por favor, preciso de ajuda com este pagamento urgente"},
        
        # Cambio Clave (Neutra - PT)
        {"id_conv": "CONV_07", "turno": 1, "rol": "user", "mensaje": "Preciso trocar minha senha de segurança"},
        {"id_conv": "CONV_07", "turno": 2, "rol": "bot", "mensaje": "Enviei um link para alteração de senha no seu e-mail cadastrado."},
        {"id_conv": "CONV_07", "turno": 3, "rol": "user", "mensaje": "Excelente, deu tudo certo. Obrigado!"},
        
        # Tarjeta Bloqueada (Zona Gris / Abandono)
        {"id_conv": "CONV_08", "turno": 1, "rol": "user", "mensaje": "Me bloquearon mi tarjeta de débito sin avisar"},
        {"id_conv": "CONV_08", "turno": 2, "rol": "bot", "mensaje": "Lo siento, por seguridad bloqueamos tarjetas por movimientos sospechosos."},
        {"id_conv": "CONV_08", "turno": 3, "rol": "user", "mensaje": "No se preocupen, buscaré otro banco que sí funcione"},
    ]
    adapter = IngestAdapter()
    
    # Determinar qué archivos procesar
    files_to_process = []
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        if os.path.exists(target_file):
            files_to_process.append(target_file)
        else:
            print(f"Error: El archivo especificado no existe: {target_file}")
            sys.exit(1)
    else:
        raw_dir = "data/raw"
        if os.path.exists(raw_dir):
            for f in os.listdir(raw_dir):
                if f.endswith('.csv') or f.endswith('.json'):
                    files_to_process.append(os.path.join(raw_dir, f))
                    
    # Si no hay archivos para procesar, usar el dataset por defecto
    if not files_to_process:
        print("No se detectaron archivos de entrada personalizados en data/raw/. Procesando dataset de prueba por defecto.")
        df_raw = pd.DataFrame(data)
        out_name = "inference_results.parquet"
        process_and_infer(df_raw, out_name)
    else:
        for file_path in files_to_process:
            print(f"\nProcesando archivo: {file_path}")
            if file_path.endswith('.json'):
                df_raw = adapter.load_json(file_path)
            else:
                df_raw = adapter.load_csv(file_path)
                
            if df_raw.empty:
                print(f"Alerta: El archivo {file_path} está vacío o no pasó las validaciones de esquema de Pandera.")
                continue
                
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            out_name = f"{base_name}.parquet"
            process_and_infer(df_raw, out_name)

def process_and_infer(df_raw: pd.DataFrame, out_name: str):
    """Ejecuta el flujo ETL completo, Feature Engineering y la cascada de inferencia."""
    # 2. Correr Extracción y Agregación
    print("--- Ejecutando Feature Engineering (Capa Rápida) ---")
    extractor = FeatureExtractor()
    df_msg = extractor.extract_message_features(df_raw)
    df_msg = extractor.extract_bot_signals(df_msg)
    df_msg = extractor.compute_semantic_coherence(df_msg)
    
    aggregator = FeatureAggregator()
    df_features = aggregator.aggregate_conversation_features(df_msg)
    
    # 3. Generar Historiales completos en texto plano
    histories = {}
    for cid, group in df_raw.groupby("id_conv"):
        hist = "\n".join([f"{row['rol'].upper()}: {row['mensaje']}" for _, row in group.sort_values('turno').iterrows()])
        histories[cid] = hist
        
    # 4. Inferencia en Cascada
    print("--- Ejecutando Inferencia en Cascada (LightGBM + LLM Twin-Pass) ---")
    orchestrator = CascadeOrchestrator(tau_low=0.45, tau_high=0.75, llm_provider="gemini")
    
    results = orchestrator.run_inference(df_features, histories)
    
    # 5. Exportar Resultados
    out_dir = "data/processed"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_name)
    
    results.to_parquet(out_path, index=False)
    print(f"Pipeline finalizado con éxito. Resultados exportados a: {out_path}")
    print("\nMuestra de resultados:")
    cols_to_show = ['id_conv', 'frustration_probability', 'final_is_frustrated', 'layer_used']
    print(results[cols_to_show].head(5))

if __name__ == "__main__":
    main()
