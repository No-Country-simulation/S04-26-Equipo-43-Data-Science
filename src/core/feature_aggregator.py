import pandas as pd
import numpy as np
from src.utils.logger import logger

class FeatureAggregator:
    """
    Agregador de características a nivel de conversación.
    Transforma features por mensaje en una matriz de características avanzada para el modelo.
    """

    def aggregate_conversation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Agregando features a nivel de conversación...")
        
        df = df.copy()
        records = []
        
        # Procesar por id_conv
        for conv_id, group in df.groupby('id_conv'):
            group = group.sort_values('turno')
            
            # Roles
            user_msgs = group[group['rol'] == 'user']
            bot_msgs = group[group['rol'] == 'bot']
            
            # Conteos básicos
            total_turns = len(group)
            user_message_count = len(user_msgs)
            
            # Bot fallbacks, reboots, apologies, capability error
            bot_fallback_count = bot_msgs['is_fallback'].sum() if not bot_msgs.empty else 0
            bot_reboot_count = bot_msgs['is_reboot'].sum() if not bot_msgs.empty else 0
            bot_apology_count = bot_msgs['is_apology'].sum() if not bot_msgs.empty else 0
            bot_capability_error_count = bot_msgs['is_capability_error'].sum() if not bot_msgs.empty else 0
            
            # 1. user_repetition_count (solicitudes duplicadas o muy parecidas)
            user_repetition_count = 0
            user_texts = user_msgs['mensaje'].dropna().tolist()
            for i in range(1, len(user_texts)):
                t1 = set(user_texts[i-1].lower().split())
                t2 = set(user_texts[i].lower().split())
                if t1 and t2:
                    overlap = len(t1.intersection(t2)) / len(t1.union(t2))
                    if overlap > 0.8:
                        user_repetition_count += 1
            
            user_repetition_ratio = user_repetition_count / total_turns if total_turns > 0 else 0.0
            
            # 2. uppercase_messages_count
            uppercase_messages_count = (user_msgs['uppercase_ratio'] > 0.5).sum() if not user_msgs.empty else 0
            
            # 3. max_consecutive_user_msgs
            max_consecutive_user_msgs = 0
            current_consecutive = 0
            for rol in group['rol']:
                if rol == 'user':
                    current_consecutive += 1
                    if current_consecutive > max_consecutive_user_msgs:
                        max_consecutive_user_msgs = current_consecutive
                else:
                    current_consecutive = 0
            
            # 4. avg_user_message_length & message_length_variance
            avg_user_message_length = user_msgs['message_length'].mean() if not user_msgs.empty else 0.0
            message_length_variance = user_msgs['message_length'].var() if not user_msgs.empty else 0.0
            if pd.isna(message_length_variance):
                message_length_variance = 0.0
                
            # 5. negation_count, profanity_present, escalation_requested
            negation_count = user_msgs['has_negation'].sum() if not user_msgs.empty else 0
            profanity_present = user_msgs['has_profanity'].any() if not user_msgs.empty else False
            escalation_requested = user_msgs['has_escalation'].any() if not user_msgs.empty else False
            
            # 6. resolution_achieved (simplificado: sin escalamiento y sin error bot final)
            resolution_achieved = True
            if escalation_requested:
                resolution_achieved = False
            elif not bot_msgs.empty:
                last_bot_msg = bot_msgs.tail(1)
                if last_bot_msg['is_fallback'].values[0] or last_bot_msg['is_capability_error'].values[0]:
                    resolution_achieved = False
                    
            # 7. typing_vs_button_ratio
            typing_count = user_msgs['is_user_typing'].sum() if not user_msgs.empty else 0
            typing_vs_button_ratio = typing_count / user_message_count if user_message_count > 0 else 0.0
            
            # 8. avg_bot_response_time
            avg_bot_response_time = bot_msgs['response_time_seconds'].mean() if not bot_msgs.empty else 0.0
            
            # 9. frustration_acceleration
            frustration_acceleration = 0.0
            if user_message_count > 1:
                mid = user_message_count // 2
                first_half = user_msgs.iloc[:mid]
                second_half = user_msgs.iloc[mid:]
                first_neg = first_half['has_negation'].mean()
                second_neg = second_half['has_negation'].mean()
                frustration_acceleration = float(second_neg - first_neg)
                
            # 10. first_frustration_turn
            first_frustration_turn = 0
            for idx, row in user_msgs.iterrows():
                if row['has_profanity'] or row['uppercase_ratio'] > 0.5 or row['has_negation']:
                    first_frustration_turn = int(row['turno'])
                    break
                    
            # 11. avg_cosine_similarity y min_cosine_similarity
            avg_cosine_similarity = bot_msgs['cosine_similarity'].mean() if not bot_msgs.empty else 0.5
            min_cosine_similarity = bot_msgs['cosine_similarity'].min() if not bot_msgs.empty else 0.5
            if pd.isna(avg_cosine_similarity): avg_cosine_similarity = 0.5
            if pd.isna(min_cosine_similarity): min_cosine_similarity = 0.5
            
            # 12. dst_deviation_count
            dst_deviation_count = int(bot_msgs['is_irrelevant_dst'].sum() + bot_msgs['is_premature_dst_exit'].sum()) if not bot_msgs.empty else 0
            
            # 13. char_elongation_count
            char_elongation_count = user_msgs['has_char_elongation'].sum() if not user_msgs.empty else 0
            
            records.append({
                'id_conv': conv_id,
                'total_turns': total_turns,
                'user_message_count': user_message_count,
                'bot_fallback_count': bot_fallback_count,
                'bot_reboot_count': bot_reboot_count,
                'bot_apology_count': bot_apology_count,
                'bot_capability_error_count': bot_capability_error_count,
                'user_repetition_count': user_repetition_count,
                'user_repetition_ratio': user_repetition_ratio,
                'uppercase_messages_count': uppercase_messages_count,
                'max_consecutive_user_msgs': max_consecutive_user_msgs,
                'avg_user_message_length': avg_user_message_length,
                'message_length_variance': message_length_variance,
                'negation_count': negation_count,
                'profanity_present': int(profanity_present),
                'escalation_requested': int(escalation_requested),
                'resolution_achieved': int(resolution_achieved),
                'typing_vs_button_ratio': typing_vs_button_ratio,
                'avg_bot_response_time': avg_bot_response_time,
                'frustration_acceleration': frustration_acceleration,
                'first_frustration_turn': first_frustration_turn,
                'avg_cosine_similarity': avg_cosine_similarity,
                'min_cosine_similarity': min_cosine_similarity,
                'dst_deviation_count': dst_deviation_count,
                'char_elongation_count': char_elongation_count
            })
            
        final_df = pd.DataFrame(records)
        final_df = final_df.fillna(0)
        
        logger.info(f"Matriz de características agregada y corregida: {final_df.shape}")
        return final_df

