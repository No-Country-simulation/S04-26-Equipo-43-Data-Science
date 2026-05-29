import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from src.utils.logger import logger
from typing import Dict, Any, List, Tuple

# Diccionario de traducción de características al español para la visualización (SHAP y UI)
FEATURE_TRANSLATIONS = {
    'total_turns': 'Total de Turnos',
    'user_message_count': 'Mensajes del Usuario',
    'bot_fallback_count': 'Fallbacks del Bot (No Entendió)',
    'bot_reboot_count': 'Reboots del Bot',
    'bot_apology_count': 'Disculpas del Bot',
    'bot_capability_error_count': 'Errores de Capacidad del Bot',
    'user_repetition_count': 'Repeticiones del Usuario',
    'user_repetition_ratio': 'Ratio de Repetición',
    'uppercase_messages_count': 'Mensajes en Mayúsculas',
    'max_consecutive_user_msgs': 'Máx Mensajes Seguidos de Usuario',
    'avg_user_message_length': 'Longitud Promedio Mensajes',
    'message_length_variance': 'Variabilidad de Longitud de Mensajes',
    'negation_count': 'Cantidad de Negaciones / Fricción',
    'profanity_present': 'Groserías Presentes',
    'escalation_requested': 'Solicitud de Agente Humano',
    'resolution_achieved': 'Resolución Lograda',
    'typing_vs_button_ratio': 'Ratio Escritura vs Botones',
    'avg_bot_response_time': 'Tiempo Respuesta Promedio del Bot',
    'frustration_acceleration': 'Aceleración de Frustración',
    'first_frustration_turn': 'Turno de Primera Frustración',
    'avg_cosine_similarity': 'Coherencia Semántica Promedio',
    'min_cosine_similarity': 'Coherencia Semántica Mínima',
    'dst_deviation_count': 'Desvíos de Intención (DST)',
    'char_elongation_count': 'Elongación de Caracteres (Repetición letras)'
}

class SHAPExplainer:
    """
    Motor de explicabilidad usando SHAP (SHapley Additive exPlanations).
    Proporciona transparencia determinística sobre las decisiones del modelo LightGBM.
    """
    
    def __init__(self, model, feature_cols: List[str]):
        """
        Inicializa el explainer.
        Args:
            model: Modelo entrenado (ej. LightGBM Booster)
            feature_cols: Lista de nombres de las características en el orden esperado.
        """
        self.model = model
        self.feature_cols = feature_cols
        # TreeExplainer es ultra-rápido para modelos basados en árboles como LightGBM
        self.explainer = shap.TreeExplainer(self.model)
        logger.info("SHAP TreeExplainer inicializado.")

    def explain_predictions(self, df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Calcula los valores SHAP para un conjunto de datos.
        
        Returns:
            shap_values: Matriz NumPy con los valores SHAP.
            X: DataFrame alineado usado para el cálculo.
        """
        logger.info("Calculando valores SHAP...")
        
        # Preparar X igual que en predicción
        X = df.copy()
        for col in self.feature_cols:
            if col not in X.columns:
                X[col] = 0
        X = X[self.feature_cols]
        
        for col in X.select_dtypes(include=['bool']).columns:
            X[col] = X[col].astype(int)

        # shap_values será una matriz de (n_samples, n_features)
        shap_values = self.explainer.shap_values(X)
        
        # En clasificación binaria con LightGBM, shap_values puede ser una lista de arrays 
        # (uno por clase) o un solo array. Depende de la versión y objective.
        # Para objective='binary', suele retornar la explicación de la clase 1 (probabilidad).
        if isinstance(shap_values, list):
            shap_values = shap_values[1] # Tomar la clase positiva (frustración)

        return shap_values, X

    def get_top_n_reasons(self, shap_values: np.ndarray, row_idx: int, n: int = 3) -> Dict[str, float]:
        """
        Extrae las Top N razones (features) que más empujaron la predicción hacia la frustración en español.
        """
        instance_shap = shap_values[row_idx]
        
        # Filtrar solo valores positivos (los que contribuyen a predecir "frustrado")
        positive_indices = np.where(instance_shap > 0)[0]
        
        if len(positive_indices) == 0:
            return {}

        # Ordenar por magnitud de contribución
        sorted_indices = positive_indices[np.argsort(instance_shap[positive_indices])[::-1]]
        top_indices = sorted_indices[:n]
        
        # Traducir los nombres de las llaves (características) a español para el visor
        reasons = {
            FEATURE_TRANSLATIONS.get(self.feature_cols[i], self.feature_cols[i]): float(instance_shap[i]) 
            for i in top_indices
        }
        return reasons

    def enrich_with_explanations(self, df: pd.DataFrame, n_reasons: int = 3) -> pd.DataFrame:
        """
        Añade las top razones SHAP al DataFrame original para su uso en el Dashboard o Second Pass.
        """
        shap_values, _ = self.explain_predictions(df)
        df_enriched = df.copy()
        
        top_reasons_list = []
        for i in range(len(df_enriched)):
            reasons = self.get_top_n_reasons(shap_values, i, n=n_reasons)
            # Guardamos las razones como string JSON/Dict para fácil visualización
            top_reasons_list.append(str(reasons) if reasons else "No clear frustration drivers")
            
        df_enriched['top_frustration_reasons'] = top_reasons_list
        return df_enriched

    def generate_summary_plot(self, df: pd.DataFrame, output_path: str = "data/processed/shap_summary.png"):
        """
        Genera y guarda el gráfico SHAP Summary (Bee swarm plot) global con etiquetas traducidas al español.
        """
        logger.info(f"Generando gráfico SHAP summary en {output_path}")
        shap_values, X = self.explain_predictions(df)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Renombrar columnas a español únicamente para el renderizado del gráfico de SHAP
        X_translated = X.rename(columns=FEATURE_TRANSLATIONS)
        
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_translated, show=False)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("Gráfico generado con éxito.")
