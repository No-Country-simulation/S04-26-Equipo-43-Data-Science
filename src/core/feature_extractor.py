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
    Extrae señales a nivel de mensaje y calcula coherencia semántica en lote para CPU.
    """

    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        logger.info(f"Cargando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.signals = SIGNALS

    def detect_language(self, text: str) -> str:
        """Detecta si el texto está en español (es) o portugués (pt)."""
        text = str(text).lower()
        # Heurística simple basada en palabras clave únicas
        es_keywords = [' el ', ' la ', ' los ', ' las ', ' que ', ' y ', ' con ']
        pt_keywords = [' o ', ' a ', ' os ', ' as ', ' que ', ' e ', ' com ']
        
        es_count = sum(1 for k in es_keywords if k in text)
        pt_count = sum(1 for k in pt_keywords if k in text)
        
        return "pt" if pt_count > es_count else "es"

    def has_char_elongation(self, text: str) -> bool:
        """Detecta repetición anómala de caracteres (ej: 'noooooo', 'taaaaan')."""
        return bool(re.search(r'(.)\1{3,}', str(text)))

    def _match_signals(self, text: str, lang: str, category: str) -> bool:
        """Verifica si un texto coincide con patrones de una categoría y lenguaje."""
        patterns = self.signals.get(lang, {}).get(category, [])
        text_str = str(text)
        for pattern in patterns:
            if re.search(pattern, text_str, re.IGNORECASE):
                return True
        return False

    def extract_message_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrae features por mensaje individual."""
        logger.info("Extrayendo features por mensaje...")
        
        df = df.copy()
        df['mensaje'] = df['mensaje'].fillna("").astype(str)
        
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
        
        # Idioma
        df['language'] = df['mensaje'].apply(self.detect_language)
        
        # Señales por lenguaje
        user_mask = df['rol'] == 'user'
        for cat in ["negation", "profanity", "escalation"]:
            df[f'has_{cat}'] = False
            df.loc[user_mask, f'has_{cat}'] = df[user_mask].apply(
                lambda row: self._match_signals(row['mensaje'], row['language'], cat), axis=1
            )
            
        # Nivel 1 features adicionales
        df['is_user_typing'] = False
        df.loc[user_mask, 'is_user_typing'] = df.loc[user_mask, 'word_count'] > 3
        
        df['turn_position'] = df['turno'].astype(int)
        df['response_time_seconds'] = 0.0 # Latencia simulada en ausencia de timestamps reales
            
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
            
        # Nivel 2 features adicionales
        df['offers_human_handoff'] = False
        df.loc[bot_mask, 'offers_human_handoff'] = df[bot_mask].apply(
            lambda row: self._match_signals(row['mensaje'], row['language'], "escalation"), axis=1
        )
        
        df['is_irrelevant_dst'] = False
        df['is_premature_dst_exit'] = False
            
        return df

    def compute_semantic_coherence(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula la similitud semántica y el índice de Jaccard en lote."""
        logger.info("Calculando coherencia semántica optimizada (batch)...")
        
        df = df.copy()
        df['cosine_similarity'] = np.nan
        df['jaccard_index'] = np.nan
        
        # Extraer mensajes únicos para encoding en lote
        valid_messages = df['mensaje'].dropna().astype(str).str.strip()
        unique_messages = valid_messages.unique().tolist()
        
        if not unique_messages:
            return df
            
        logger.info(f"Codificando {len(unique_messages)} mensajes únicos...")
        embeddings = self.model.encode(unique_messages, batch_size=128, show_progress_bar=False, convert_to_tensor=True)
        msg_to_emb = {msg: emb for msg, emb in zip(unique_messages, embeddings)}
        
        def get_tokens(text):
            if not isinstance(text, str):
                return set()
            return set(re.findall(r'\w+', text.lower()))

        # Procesar por conversación
        for conv_id, group in df.groupby('id_conv'):
            group = group.sort_values('turno')
            user_msgs = group[group['rol'] == 'user']
            
            for _, user_row in user_msgs.iterrows():
                # Buscar el siguiente mensaje del bot
                next_bot = group[(group['rol'] == 'bot') & (group['turno'] > user_row['turno'])].head(1)
                
                if not next_bot.empty:
                    u_msg = user_row['mensaje']
                    b_msg = next_bot['mensaje'].values[0]
                    next_bot_idx = next_bot.index[0]
                    
                    # Cosine Similarity
                    if u_msg in msg_to_emb and b_msg in msg_to_emb:
                        sim = util.cos_sim(msg_to_emb[u_msg], msg_to_emb[b_msg]).item()
                        df.loc[next_bot_idx, 'cosine_similarity'] = sim
                    
                    # Jaccard Index
                    u_tokens = get_tokens(u_msg)
                    b_tokens = get_tokens(b_msg)
                    if u_tokens or b_tokens:
                        jaccard = len(u_tokens.intersection(b_tokens)) / len(u_tokens.union(b_tokens))
                        df.loc[next_bot_idx, 'jaccard_index'] = jaccard

        # Calcular DST Deviation heurístico basado en similitud y flujos
        for conv_id, group in df.groupby('id_conv'):
            group = group.sort_values('turno')
            for idx, row in group.iterrows():
                if row['rol'] == 'bot':
                    prev_user = group[(group['rol'] == 'user') & (group['turno'] < row['turno'])].tail(1)
                    if not prev_user.empty:
                        sim = df.loc[idx, 'cosine_similarity']
                        u_len = prev_user['message_length'].values[0]
                        
                        # is_irrelevant_dst: Similitud muy baja ante consulta de usuario larga
                        if pd.notna(sim) and sim < 0.25 and u_len > 12:
                            df.loc[idx, 'is_irrelevant_dst'] = True
                        
                        # is_premature_dst_exit: Fallback/Reboot después de que el usuario intentó escalar
                        u_esc = prev_user['has_escalation'].values[0]
                        if u_esc and (row['is_fallback'] or row['is_reboot']):
                            df.loc[idx, 'is_premature_dst_exit'] = True
                            
        return df

