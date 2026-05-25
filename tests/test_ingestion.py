import pandas as pd
import os
from src.core.ingest_adapter import IngestAdapter

def test_ingestion():
    # 1. Crear datos sintéticos con algunos errores
    data = {
        "id_conv": ["C1", "C1", "C2", "C2", "C3"],
        "turno": [1, 2, 1, 2, "error"],  # Turno con error de tipo
        "rol": ["usuario", "asistente", "User", "Bot", "user"],
        "mensaje": ["Hola", "Hola en qué puedo ayudarte", "Tengo un problema", "Lo siento", "Mensaje con error"]
    }
    
    df_test = pd.DataFrame(data)
    test_csv = "data/raw/test_data.csv"
    os.makedirs("data/raw", exist_ok=True)
    df_test.to_csv(test_csv, index=False, encoding="utf-8")
    
    # 2. Inicializar adaptador
    adapter = IngestAdapter(dlq_path="data/dlq/test_errors.parquet")
    
    # 3. Cargar y validar
    print("\n--- Iniciando prueba de ingesta ---")
    df_valid = adapter.load_csv(test_csv)
    
    print(f"\nRegistros válidos recuperados: {len(df_valid)}")
    if not df_valid.empty:
        print(df_valid)
    
    # 4. Verificar DLQ
    if os.path.exists("data/dlq/test_errors.parquet"):
        df_dlq = pd.read_parquet("data/dlq/test_errors.parquet")
        print(f"\nRegistros en DLQ: {len(df_dlq)}")
        print(df_dlq[["id_conv", "turno", "error_reason"]])

if __name__ == "__main__":
    test_ingestion()
