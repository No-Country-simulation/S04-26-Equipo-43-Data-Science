import lightgbm as lgb
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, f1_score, accuracy_score, roc_auc_score
from src.utils.logger import logger
from typing import Tuple, Dict, Any

class FrustrationClassifier:
    """
    Clasificador de la Capa Rápida usando LightGBM.
    Diseñado para alta velocidad en CPU y manejo de clases desbalanceadas.
    """
    
    def __init__(self, model_path: str = "models/lgbm_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.features_cols = None
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Hiperparámetros optimizados para CPU y prevención de overfitting
        self.params = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'boosting_type': 'gbdt',
            'learning_rate': 0.05,
            'num_leaves': 31,
            'max_depth': -1,
            'is_unbalance': True,  # Clave para frustración (clase minoritaria)
            'feature_fraction': 0.8,
            'verbose': -1,
            'n_jobs': -1  # Usar todos los cores
        }

    def _prepare_data(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepara X e y, convirtiendo booleanos a enteros si es necesario."""
        # Filtrar columnas que no son features (ej. metadatos)
        exclude_cols = ['id_conv', target_col, 'ingestion_timestamp', 'error_reason']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        self.features_cols = feature_cols
        
        X = df[feature_cols].copy()
        
        # Convertir booleanos a 0/1 para LightGBM
        for col in X.select_dtypes(include=['bool']).columns:
            X[col] = X[col].astype(int)
            
        y = df[target_col].astype(int)
        return X, y

    def train(self, df: pd.DataFrame, target_col: str = 'is_frustrated', cv: int = 5) -> Dict[str, float]:
        """
        Entrena el modelo LightGBM con validación cruzada.
        """
        logger.info(f"Iniciando entrenamiento del clasificador (target: {target_col})")
        
        if target_col not in df.columns:
            logger.error(f"La columna objetivo '{target_col}' no se encuentra en el DataFrame.")
            raise ValueError(f"Target column '{target_col}' missing.")

        X, y = self._prepare_data(df, target_col)
        
        logger.info(f"Features seleccionadas ({len(self.features_cols)}): {self.features_cols}")
        logger.info(f"Distribución de clases:\n{y.value_counts(normalize=True)}")

        # Cross Validation
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        cv_scores = {'f1': [], 'auc': [], 'accuracy': []}
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            lgb_train = lgb.Dataset(X_train, y_train)
            lgb_eval = lgb.Dataset(X_val, y_val, reference=lgb_train)
            
            # Entrenamiento con early stopping
            fold_model = lgb.train(
                self.params,
                lgb_train,
                num_boost_round=1000,
                valid_sets=[lgb_train, lgb_eval],
                valid_names=['train', 'valid'],
                callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
            )
            
            # Predicciones de validación
            y_pred_prob = fold_model.predict(X_val, num_iteration=fold_model.best_iteration)
            y_pred = (y_pred_prob > 0.5).astype(int)
            
            cv_scores['f1'].append(f1_score(y_val, y_pred))
            cv_scores['auc'].append(roc_auc_score(y_val, y_pred_prob))
            cv_scores['accuracy'].append(accuracy_score(y_val, y_pred))
            
            logger.info(f"Fold {fold} - F1: {cv_scores['f1'][-1]:.4f}, AUC: {cv_scores['auc'][-1]:.4f}")

        # Métricas promedio
        avg_metrics = {k: np.mean(v) for k, v in cv_scores.items()}
        logger.info(f"Métricas CV ({cv} folds): F1={avg_metrics['f1']:.4f}, AUC={avg_metrics['auc']:.4f}")

        # Entrenar modelo final con todos los datos
        logger.info("Entrenando modelo final con el dataset completo...")
        lgb_full = lgb.Dataset(X, y)
        # Usamos un número de iteraciones conservador basado en CV (ej. 200) o un valid set si tenemos datos suficientes
        self.model = lgb.train(self.params, lgb_full, num_boost_round=200)
        
        self.save_model()
        return avg_metrics

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza predicciones sobre nuevos datos y devuelve las probabilidades.
        """
        if self.model is None:
            self.load_model()
            
        logger.info("Generando predicciones de probabilidad...")
        
        # Preparar datos usando las mismas columnas que en el entrenamiento
        X = df.copy()
        
        # Añadir columnas faltantes con 0 (manejo de esquemas dinámicos)
        for col in self.features_cols:
            if col not in X.columns:
                X[col] = 0
                
        # Asegurar el orden de las columnas
        X = X[self.features_cols]
        
        # Convertir booleanos
        for col in X.select_dtypes(include=['bool']).columns:
            X[col] = X[col].astype(int)
            
        probabilities = self.model.predict(X)
        
        # Añadir probabilidades al dataframe original
        results = df.copy()
        results['frustration_probability'] = probabilities
        
        return results

    def save_model(self):
        """Guarda el modelo entrenado y los nombres de las features."""
        if self.model:
            model_data = {
                'model': self.model,
                'features': self.features_cols
            }
            joblib.dump(model_data, self.model_path)
            logger.info(f"Modelo guardado en {self.model_path}")
        else:
            logger.warning("No hay modelo para guardar.")

    def load_model(self):
        """Carga el modelo y la configuración desde disco."""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.features_cols = model_data['features']
            logger.info(f"Modelo cargado desde {self.model_path}")
        else:
            logger.error(f"No se encontró el modelo en {self.model_path}")
            raise FileNotFoundError(f"Model file {self.model_path} not found.")
