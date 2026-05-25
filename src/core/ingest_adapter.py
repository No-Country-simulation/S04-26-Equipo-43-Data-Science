import pandas as pd
import pandera.pandas as pa
from pandera.typing import DataFrame, Series
from typing import Optional, Union, List
import json
import os
from src.utils.logger import logger

# Esquema de validación con Pandera
class ConversationSchema(pa.DataFrameModel):
    id_conv: Series[str] = pa.Field(coerce=True)
    turno: Series[int] = pa.Field(ge=0, coerce=True)
    rol: Series[str] = pa.Field(isin=["user", "bot", "system"], coerce=True)
    mensaje: Series[str] = pa.Field(nullable=True, coerce=True)

    class Config:
        strict = True
        coerce = True

class IngestAdapter:
    """
    Adaptador de ingesta resiliente para ConversaSense AI.
    Maneja validación de esquemas, codificación UTF-8 y Dead Letter Queue (DLQ).
    """

    def __init__(self, dlq_path: str = "data/dlq/errores_ingesta.parquet"):
        self.dlq_path = dlq_path
        self.schema = ConversationSchema
        
        # Asegurar que el directorio de DLQ existe
        os.makedirs(os.path.dirname(self.dlq_path), exist_ok=True)

    def _save_to_dlq(self, df: pd.DataFrame, reason: str):
        """Guarda registros fallidos en la cola de mensajes muertos."""
        df = df.copy()
        df["error_reason"] = reason
        df["ingestion_timestamp"] = pd.Timestamp.now()
        
        if os.path.exists(self.dlq_path):
            existing_dlq = pd.read_parquet(self.dlq_path)
            df = pd.concat([existing_dlq, df], ignore_index=True)
        
        df.to_parquet(self.dlq_path, index=False)
        logger.warning(f"Se han enviado {len(df)} registros al DLQ: {reason}")

    def _apply_heuristics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica heurísticas para normalizar roles y mensajes."""
        # Detección de roles si no están claros (ejemplo: 'usuario' -> 'user', 'asistente' -> 'bot')
        if 'rol' in df.columns:
            role_map = {
                'usuario': 'user', 'customer': 'user', 'client': 'user',
                'asistente': 'bot', 'assistant': 'bot', 'agent': 'bot'
            }
            df['rol'] = df['rol'].str.lower().replace(role_map)
        else:
            # Heurística simple: si no hay columna rol, pero hay id_conv y turno,
            # podríamos intentar inferir, pero por ahora marcamos como error si falta.
            logger.error("Columna 'rol' ausente y no se puede inferir con seguridad.")
        
        # Forzar UTF-8 y limpiar strings
        if 'mensaje' in df.columns:
            df['mensaje'] = df['mensaje'].astype(str).str.strip()
            
        return df

    def load_csv(self, file_path: str, sep: str = ",") -> pd.DataFrame:
        """Carga y valida un archivo CSV."""
        logger.info(f"Cargando CSV: {file_path}")
        try:
            # RF-01: Forzar codificación UTF-8
            df = pd.read_csv(file_path, sep=sep, encoding="utf-8")
        except UnicodeDecodeError:
            logger.warning("Fallo UTF-8, intentando latin-1")
            df = pd.read_csv(file_path, sep=sep, encoding="latin-1")
        except Exception as e:
            logger.error(f"Error fatal leyendo CSV: {e}")
            return pd.DataFrame()

        return self._process_and_validate(df)

    def load_json(self, file_path: str) -> pd.DataFrame:
        """Carga y valida un archivo JSON."""
        logger.info(f"Cargando JSON: {file_path}")
        try:
            df = pd.read_json(file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Error fatal leyendo JSON: {e}")
            return pd.DataFrame()

        return self._process_and_validate(df)

    def _process_and_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica heurísticas y valida contra el esquema."""
        df = self._apply_heuristics(df)
        
        try:
            validated_df = self.schema.validate(df)
            logger.info(f"Validación exitosa: {len(validated_df)} registros.")
            return validated_df
        except pa.errors.SchemaErrors as err:
            # Captura errores de esquema y envía los registros fallidos al DLQ
            logger.warning(f"Errores de validación detectados. Enviando al DLQ.")
            # En una implementación real, separaríamos solo las filas con error
            # Aquí por simplicidad enviamos el bloque si falla la validación estricta
            self._save_to_dlq(df, str(err))
            # Retornamos solo las filas que pasaron si es posible, o vacío
            return err.valid_data if hasattr(err, 'valid_data') else pd.DataFrame()
        except Exception as e:
            logger.error(f"Error inesperado en validación: {e}")
            self._save_to_dlq(df, str(e))
            return pd.DataFrame()
