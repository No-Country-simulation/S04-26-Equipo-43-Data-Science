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
        strict = "filter"  # Descarta automáticamente columnas irrelevantes
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
        """Guarda registros fallidos en la cola de mensajes muertos de forma resiliente."""
        df = df.copy()
        
        # Forzar a string todas las columnas para evitar conflictos de tipo en PyArrow
        for col in df.columns:
            df[col] = df[col].astype(str)
            
        df["error_reason"] = str(reason)
        df["ingestion_timestamp"] = str(pd.Timestamp.now())
        
        if os.path.exists(self.dlq_path):
            try:
                existing_dlq = pd.read_parquet(self.dlq_path)
                for col in existing_dlq.columns:
                    existing_dlq[col] = existing_dlq[col].astype(str)
                df = pd.concat([existing_dlq, df], ignore_index=True)
            except Exception as e:
                logger.warning(f"Error concatenando con DLQ existente: {e}. Recreando archivo.")
                
        df.to_parquet(self.dlq_path, index=False)
        logger.warning(f"Se han enviado {len(df)} registros al DLQ: {reason}")

    def _apply_heuristics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica heurísticas para normalizar nombres de columnas, roles y mensajes de forma agnóstica."""
        df = df.copy()
        
        # 1. Normalizar nombres de columnas a minúsculas y sin espacios
        df.columns = df.columns.str.strip().str.lower()
        
        # 2. Mapear columnas alternativas a las del estándar
        col_mappings = {
            'id_conversacion': 'id_conv', 'conversation_id': 'id_conv', 'id_charla': 'id_conv', 'session_id': 'id_conv',
            'turn': 'turno', 'secuencia': 'turno', 'sequence': 'turno', 'msg_order': 'turno',
            'role': 'rol', 'sender': 'rol', 'speaker': 'rol', 'tipo_usuario': 'rol',
            'message': 'mensaje', 'text': 'mensaje', 'texto': 'mensaje', 'content': 'mensaje', 'msg': 'mensaje'
        }
        rename_dict = {col: col_mappings[col] for col in df.columns if col in col_mappings}
        if rename_dict:
            df = df.rename(columns=rename_dict)
            logger.info(f"Columnas mapeadas heurísticamente: {rename_dict}")
            
        # 3. Detección y normalización de roles
        if 'rol' in df.columns:
            role_map = {
                'usuario': 'user', 'customer': 'user', 'client': 'user',
                'asistente': 'bot', 'assistant': 'bot', 'agent': 'bot'
            }
            df['rol'] = df['rol'].astype(str).str.lower().str.strip().replace(role_map)
        else:
            logger.error("Columna 'rol' ausente en el archivo cargado.")
        
        # 4. Sanitizar y limpiar mensajes
        if 'mensaje' in df.columns:
            df['mensaje'] = df['mensaje'].fillna("").astype(str).str.strip()
            
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
