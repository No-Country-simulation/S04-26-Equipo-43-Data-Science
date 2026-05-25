import pandas as pd
import re
import numpy as np
from typing import List, Dict, Any
from src.core.signal_dictionaries import SIGNALS
from src.utils.logger import logger
from sentence_transformers import SentenceTransformer, util

class FeatureExtractor:
    """
    Motor de extracción de características determinísticas (Heurísticas).
    Extrae señales a nivel de mensaje y calcula coherencia semántica.
    """

    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        logger.info(f"Cargando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.signals = SIGNALS

    def detect_language(self, text: str) -> str:
        """Detecta si el texto está en español (es) o portugués (pt)."""
        text = text.lower()
        # Heurística simple basada en palabras clave únicas
        es_keywords = [' el ', ' la ', ' los ', ' las ', ' que ', ' y ', ' con ']
        pt_keywords = [' o ', ' a ', ' os ', ' as ', ' que ', ' e ', ' com ']
        
        es_count = sum(1 for k in es_keywords if k in text)
        pt_count = sum(1 for k in pt_keywords if k in text)
        
        return "pt" if pt_count > es_count else "es"

    def has_char_elongation(self, text: str) -> bool:
        """Detecta repetición anómala de caracteres (ej: 'noooooo', 'taaaaan')."""
        return bool(re.search(r'(.)\1{3,}', text))

    def _match_signals(self, text: str, lang: str, category: str) -> bool:
        """Verifica si un texto coincide con patrones de una categoría y lenguaje."""
        patterns = self.signals.get(lang, {}).get(category, [])
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def extract_message_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrae features por mensaje individual."""
        logger.info("Extrayendo features por mensaje...")
        
        df = df.copy()
        
        # Features básicas de texto
        df['message_length'] = df['mensaje'].str.len()
        df['word_count'] = df['mensaje'].str.split().str.len()
        
        # Uppercase ratio (solo si tiene letras)
        def get_upper_ratio(text):
            letters = [c for c in text if c.isalpha()]
            if not letters: return 0.0
            return sum(1 for c in letters if c.isupper()) / len(letters)
        
        df['uppercase_ratio'] = df['mensaje'].apply(get_upper_ratio)
        
        # Conteos de puntuación
        df['exclamation_count'] = df['mensaje'].str.count('!')
        df['question_mark_count'] = df['mensaje'].str.count(r'\?')
        df['ellipsis_count'] = df['mensaje'].str.count(r'\.\.\.')
        
        # Heurísticas avanzadas
        df['has_char_elongation'] = df['mensaje'].apply(self.has_char_elongation)
        
        # Idioma (por mensaje, o podrías hacerlo por conversación)
        df['language'] = df['mensaje'].apply(self.detect_language)
        
        # Señales por lenguaje
        for cat in ["negation", "profanity", "escalation"]:
            df[f'has_{cat}'] = df.apply(
                lambda row: self._match_signals(row['mensaje'], row['language'], cat), axis=1
            )
            
        return df

    def extract_bot_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrae señales específicas del comportamiento del bot."""
        logger.info("Extrayendo señales de comportamiento del bot...")
        
        df = df.copy()
        bot_mask = df['rol'] == 'bot'
        
        # Inicializar columnas
        for cat in ["fallback", "apology", "reboot", "capability_error"]:
            df[f'is_{cat}'] = False
            df.loc[bot_mask, f'is_{cat}'] = df[bot_mask].apply(
                lambda row: self._match_signals(row['mensaje'], row['language'], cat), axis=1
            )
            
        return df

    def compute_semantic_coherence(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula la similitud semántica entre el mensaje del usuario y la respuesta del bot."""
        logger.info("Calculando coherencia semántica...")
        
        df = df.copy()
        df['cosine_similarity'] = np.nan
        
        # Agrupar por conversación para procesar pares
        for conv_id, group in df.groupby('id_conv'):
            group = group.sort_values('turno')
            user_msgs = group[group['rol'] == 'user']
            
            for _, user_row in user_msgs.iterrows():
                # Buscar el siguiente mensaje del bot
                next_bot = group[(group['rol'] == 'bot') & (group['turno'] > user_row['turno'])].head(1)
                
                if not next_bot.empty:
                    u_emb = self.model.encode(user_row['mensaje'], convert_to_tensor=True)
                    b_emb = self.model.encode(next_bot['mensaje'].values[0], convert_to_tensor=True)
                    sim = util.cos_sim(u_emb, b_emb).item()
                    
                    # Guardamos la similitud en la fila del usuario (o del bot, o ambas)
                    # Aquí la pondremos en la fila del bot para indicar qué tan bien respondió
                    df.loc[next_bot.index, 'cosine_similarity'] = sim
                    
        return df
