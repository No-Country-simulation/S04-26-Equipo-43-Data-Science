import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, f1_score, confusion_matrix
from src.utils.logger import logger

class ModelEvaluator:
    """
    Módulo para evaluar la fiabilidad científica del sistema híbrido (Capa Rápida + Capa Profunda)
    contra el "Ground Truth" o etiquetado humano.
    Calcula F1-Score y Cohen's Kappa.
    """

    def __init__(self):
        pass

    def evaluate_performance(self, df_results: pd.DataFrame, ground_truth_col: str, prediction_col: str):
        """
        Calcula las métricas base del proyecto.
        
        Args:
            df_results (pd.DataFrame): DataFrame con las predicciones y las etiquetas reales.
            ground_truth_col (str): Nombre de la columna con el etiquetado humano (True/False).
            prediction_col (str): Nombre de la columna con la predicción del sistema (True/False).
            
        Returns:
            dict: Diccionario con las métricas calculadas.
        """
        if ground_truth_col not in df_results.columns or prediction_col not in df_results.columns:
            logger.error(f"Faltan columnas requeridas para la evaluación: {ground_truth_col} o {prediction_col}")
            return None

        # Asegurar booleanos o enteros para sklearn
        y_true = df_results[ground_truth_col].astype(int)
        y_pred = df_results[prediction_col].astype(int)

        logger.info(f"Calculando métricas sobre {len(y_true)} muestras estratificadas...")

        # 1. F1-Score (Objetivo >= 0.80)
        f1 = f1_score(y_true, y_pred, average='binary') # 'binary' asume clase positiva = 1
        
        # 2. Cohen's Kappa (Objetivo 0.50 - 0.60)
        kappa = cohen_kappa_score(y_true, y_pred)
        
        # 3. Matriz de Confusión
        cm = confusion_matrix(y_true, y_pred)

        metrics = {
            "F1-Score": round(f1, 4),
            "Cohen's Kappa": round(kappa, 4),
            "Confusion Matrix": cm.tolist()
        }

        logger.info(f"Resultados de la Evaluación: F1={metrics['F1-Score']}, Kappa={metrics['Cohen\'s Kappa']}")
        return metrics

if __name__ == "__main__":
    # Test rápido (simulando los datos de la Fase de Consenso)
    np.random.seed(42)
    # Generando una muestra de 500 simulada
    ground_truth = np.random.choice([0, 1], size=500, p=[0.7, 0.3]) 
    
    # Simulamos predicciones muy buenas (85% de las veces acierta)
    predictions = ground_truth.copy()
    noise_indices = np.random.choice(500, size=75, replace=False)
    predictions[noise_indices] = 1 - predictions[noise_indices]

    df_test = pd.DataFrame({
        "id_conv": [f"CONV_{i}" for i in range(500)],
        "etiqueta_humana": ground_truth,
        "prediccion_hibrida": predictions
    })

    evaluator = ModelEvaluator()
    evaluator.evaluate_performance(df_test, "etiqueta_humana", "prediccion_hibrida")
