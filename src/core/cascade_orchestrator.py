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

    def run_inference(self, df_conv: pd.DataFrame, full_histories: Dict[str, str]) -> pd.DataFrame:
        """
        Ejecuta el pipeline de cascada sobre un conjunto de conversaciones.
        
        Args:
            df_conv: DataFrame con las features agregadas por conversación.
            full_histories: Diccionario {id_conv: "Texto completo de la charla"}.
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
            
            # Caso A: Confianza Alta en NO-FRUSTRACIÓN (Zona Segura)
            if prob < self.tau_low:
                decision = {
                    "final_is_frustrated": False,
                    "layer_used": "fast",
                    "confidence": 1 - prob,
                    "reasoning": "Fast Layer: Low probability"
                }
            
            # Caso B: Zona Gris o Alta Probabilidad -> Escalar a LLM (Capa Profunda)
            else:
                layer = "deep" if prob > self.tau_high else "gray_zone_escalation"
                logger.info(f"Escalando caso {id_conv} (Prob: {prob:.2f}) a Capa Profunda...")
                
                history = full_histories.get(id_conv, "Historial no disponible")
                # Pasamos las señales de la Capa Rápida como contexto
                quick_signals = str({k: v for k, v in row.items() if k not in ['id_conv', 'frustration_probability']})
                
                llm_result = self.guardian.analyze_frustration(
                    history=history, 
                    reasons=quick_signals,
                    provider=self.llm_provider
                )
                
                decision = {
                    "final_is_frustrated": llm_result.get("is_frustrated"),
                    "layer_used": "deep",
                    "confidence": llm_result.get("confidence_score"),
                    "reasoning": llm_result.get("reasoning")
                }
            
            final_decisions.append(decision)
            
        # Enriquecer DataFrame con resultados finales
        results['final_is_frustrated'] = [d['final_is_frustrated'] for d in final_decisions]
        results['layer_used'] = [d['layer_used'] for d in final_decisions]
        results['final_reasoning'] = [d['reasoning'] for d in final_decisions]
        
        return results
