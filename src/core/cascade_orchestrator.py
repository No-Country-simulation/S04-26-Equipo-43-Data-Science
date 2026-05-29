import pandas as pd
import numpy as np
from typing import List, Dict, Any
from src.core.frustration_classifier import FrustrationClassifier
from src.core.truth_guardian import TruthGuardian
from src.utils.logger import logger

class CascadeOrchestrator:
    """
    Orquestador de Cascada (Uncertainty-Driven Routing).
    Decide cuándo usar la Capa Rápida (LightGBM) y cuándo escalar a la Capa Profunda (LLM).
    """

    def __init__(self, 
                 tau_low: float = 0.45, 
                 tau_high: float = 0.75,
                 llm_provider: str = "gemini"):
        self.classifier = FrustrationClassifier()
        self.guardian = TruthGuardian()
        self.tau_low = tau_low
        self.tau_high = tau_high
        self.llm_provider = llm_provider
        
        # Intentar cargar el modelo rápido
        try:
            self.classifier.load_model()
        except:
            logger.warning("Modelo LightGBM no encontrado. El orquestador requerirá entrenamiento previo.")

    def run_inference(self, df_conv: pd.DataFrame, full_histories: Dict[str, str], model: str = None, api_key: str = None) -> pd.DataFrame:
        """
        Ejecuta el pipeline de cascada sobre un conjunto de conversaciones.
        
        Args:
            df_conv: DataFrame con las features agregadas por conversación.
            full_histories: Diccionario {id_conv: "Texto completo de la charla"}.
            model: Nombre dinámico del modelo de lenguaje para la Capa Profunda.
            api_key: Llave API dinámica del proveedor de LLM.
        """
        logger.info(f"Iniciando inferencia en cascada para {len(df_conv)} casos.")
        
        # 1. Capa Rápida: Predicción con LightGBM
        results = self.classifier.predict(df_conv)
        
        # 2. Routing Logic
        final_decisions = []
        routing_metadata = []
        
        for idx, row in results.iterrows():
            prob = row['frustration_probability']
            # id_conv podría estar en el índice o en una columna
            id_conv = idx if 'id_conv' not in row else row['id_conv']
            history = full_histories.get(id_conv, "Historial no disponible")
            
            # Rescate Heurístico (Safety Guardrails): forzar escalamiento a LLM si hay fallas obvias del bot
            bot_fallbacks = row.get('bot_fallback_count', 0)
            dst_deviations = row.get('dst_deviation_count', 0)
            bot_reboots = row.get('bot_reboot_count', 0)
            
            # Condición de rescate: bot falla >= 2 veces, o hay desvío de DST, o reinicios del bot >= 2
            has_heuristic_friction = (bot_fallbacks >= 2) or (dst_deviations >= 1) or (bot_reboots >= 2)
            
            # Caso A: Confianza Alta en NO-FRUSTRACIÓN y sin fricciones obvias detectadas
            if prob < self.tau_low and not has_heuristic_friction:
                decision = {
                    "final_is_frustrated": False,
                    "layer_used": "fast",
                    "confidence": float(1 - prob),
                    "reasoning": "Fast Layer: Low probability",
                    "history": history
                }
            
            # Caso B: Zona Gris, Alta Probabilidad, o Rescate Heurístico -> Escalar a LLM (Capa Profunda)
            else:
                if prob < self.tau_low and has_heuristic_friction:
                    logger.info(f"[Heuristic Rescue] Caso {id_conv} forzado a Capa Profunda por fallos reiterados del bot.")
                    reason_ctx = f"Rescue: Fallbacks={bot_fallbacks}, DST-Deviations={dst_deviations}, Reboots={bot_reboots}"
                else:
                    reason_ctx = f"Prob: {prob:.2f}"
                    
                logger.info(f"Escalando caso {id_conv} ({reason_ctx}) a Capa Profunda...")
                
                # Pasamos las señales de la Capa Rápida como contexto
                quick_signals = str({k: v for k, v in row.items() if k not in ['id_conv', 'frustration_probability']})
                
                llm_result = self.guardian.analyze_frustration(
                    history=history, 
                    reasons=quick_signals,
                    provider=self.llm_provider,
                    model=model,
                    api_key=api_key
                )
                
                # Enriquecer la explicación si fue rescatado heurísticamente
                final_reasoning = llm_result.get("reasoning")
                if prob < self.tau_low and has_heuristic_friction:
                    final_reasoning = f"[Heuristic Rescue Escalated] {final_reasoning}"
                
                decision = {
                    "final_is_frustrated": llm_result.get("is_frustrated"),
                    "layer_used": "deep",
                    "confidence": llm_result.get("confidence_score"),
                    "reasoning": final_reasoning,
                    "history": history
                }
            
            final_decisions.append(decision)
            
        # Enriquecer DataFrame con resultados finales
        results['final_is_frustrated'] = [d['final_is_frustrated'] for d in final_decisions]
        results['layer_used'] = [d['layer_used'] for d in final_decisions]
        results['final_reasoning'] = [d['reasoning'] for d in final_decisions]
        results['conversation_history'] = [d['history'] for d in final_decisions]
        
        return results
