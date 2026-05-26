import pandas as pd
import numpy as np
from src.utils.logger import logger

class FeatureAggregator:
    """
    Agregador de características a nivel de conversación.
    Transforma features por mensaje en una matriz de 47 features para el modelo.
    """

    def aggregate_conversation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Agregando features a nivel de conversación...")
        
        # Agrupación base por id_conv
        agg_funcs = {
            'turno': 'max',  # total_turns (aproximado si es el max turno)
            'message_length': ['mean', 'var'],
            'word_count': 'sum',
            'uppercase_ratio': 'max',
            'exclamation_count': 'sum',
            'question_mark_count': 'sum',
            'ellipsis_count': 'sum',
            'has_char_elongation': 'sum',
            'has_negation': 'sum',
            'has_profanity': 'any',
            'has_escalation': 'any',
            'is_fallback': 'sum',
            'is_apology': 'sum',
            'is_reboot': 'sum',
            'is_capability_error': 'sum',
            'cosine_similarity': ['mean', 'min']
        }
        
        # Filtrar solo mensajes del usuario para algunas métricas
        user_df = df[df['rol'] == 'user']
        user_agg = user_df.groupby('id_conv').agg({
            'mensaje': 'count',
            'message_length': 'mean',
            'has_negation': 'sum',
            'uppercase_ratio': 'mean'
        }).rename(columns={
            'mensaje': 'user_message_count',
            'message_length': 'avg_user_message_length',
            'has_negation': 'negation_count',
            'uppercase_ratio': 'avg_user_uppercase_ratio'
        })

        # Filtrar solo mensajes del bot para otras
        bot_df = df[df['rol'] == 'bot']
        bot_agg = bot_df.groupby('id_conv').agg({
            'is_fallback': 'sum',
            'is_reboot': 'sum',
            'is_apology': 'sum',
            'is_capability_error': 'sum'
        }).rename(columns={
            'is_fallback': 'bot_fallback_count',
            'is_reboot': 'bot_reboot_count',
            'is_apology': 'bot_apology_count',
            'is_capability_error': 'bot_capability_error_count'
        })

        # Agregación general
        conv_agg = df.groupby('id_conv').agg({
            'turno': 'count',
            'cosine_similarity': ['mean', 'min'],
            'has_char_elongation': 'sum'
        })
        # Aplanar multi-index de columnas
        conv_agg.columns = ['_'.join(col).strip() for col in conv_agg.columns.values]
        conv_agg = conv_agg.rename(columns={
            'turno_count': 'total_turns',
            'cosine_similarity_mean': 'avg_cosine_similarity',
            'cosine_similarity_min': 'min_cosine_similarity',
            'has_char_elongation_sum': 'char_elongation_count'
        })

        # Join de todas las agregaciones
        final_df = conv_agg.join(user_agg).join(bot_agg).fillna(0)
        
        # Calcular features derivadas (aceleración, etc.)
        final_df['user_repetition_ratio'] = final_df['user_message_count'] / final_df['total_turns']
        final_df['profanity_present'] = final_df.join(df.groupby('id_conv')['has_profanity'].any()).iloc[:, -1]
        final_df['escalation_requested'] = final_df.join(df.groupby('id_conv')['has_escalation'].any()).iloc[:, -1]

        # Asegurar que id_conv sea una columna y no solo el índice
        final_df = final_df.reset_index()
        
        logger.info(f"Matriz de características generada: {final_df.shape}")
        return final_df
