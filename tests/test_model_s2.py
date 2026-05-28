import pandas as pd
import numpy as np
import os
import sys

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.frustration_classifier import FrustrationClassifier
from src.core.explainability import SHAPExplainer

def generate_synthetic_data(n_samples=500):
    """Genera datos sintéticos alineados con las 24 features reales."""
    np.random.seed(42)
    
    total_turns = np.random.randint(2, 20, n_samples)
    user_message_count = total_turns // 2 + total_turns % 2
    
    data = {
        'id_conv': [f"C{i}" for i in range(n_samples)],
        'total_turns': total_turns,
        'user_message_count': user_message_count,
        'bot_fallback_count': np.random.randint(0, 4, n_samples),
        'bot_reboot_count': np.random.randint(0, 3, n_samples),
        'bot_apology_count': np.random.randint(0, 3, n_samples),
        'bot_capability_error_count': np.random.randint(0, 2, n_samples),
        'user_repetition_count': np.random.randint(0, 3, n_samples),
        'user_repetition_ratio': np.random.uniform(0, 0.5, n_samples),
        'uppercase_messages_count': np.random.randint(0, 4, n_samples),
        'max_consecutive_user_msgs': np.random.randint(1, 4, n_samples),
        'avg_user_message_length': np.random.uniform(10, 100, n_samples),
        'message_length_variance': np.random.uniform(0, 50, n_samples),
        'negation_count': np.random.randint(0, 5, n_samples),
        'profanity_present': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'escalation_requested': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'resolution_achieved': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'typing_vs_button_ratio': np.random.uniform(0, 1, n_samples),
        'avg_bot_response_time': np.random.uniform(0.5, 5.0, n_samples),
        'frustration_acceleration': np.random.uniform(-1, 1, n_samples),
        'first_frustration_turn': np.random.randint(0, 10, n_samples),
        'avg_cosine_similarity': np.random.uniform(0.2, 0.9, n_samples),
        'min_cosine_similarity': np.random.uniform(0.1, 0.8, n_samples),
        'dst_deviation_count': np.random.randint(0, 3, n_samples),
        'char_elongation_count': np.random.randint(0, 4, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Objetivo lógico
    prob = (
        df['escalation_requested'] * 0.35 +
        df['profanity_present'] * 0.40 +
        (df['bot_fallback_count'] > 1) * 0.20 +
        (df['avg_cosine_similarity'] < 0.35) * 0.15 +
        (df['dst_deviation_count'] > 0) * 0.15 +
        (df['char_elongation_count'] > 0) * 0.10
    )
    
    prob += np.random.normal(0, 0.05, n_samples)
    df['is_frustrated'] = (prob > 0.4).astype(int)
    return df

def test_week2():
    print("--- Generando datos sintéticos ---")
    df = generate_synthetic_data(1000)
    
    print("\n--- Entrenando Modelo LightGBM ---")
    classifier = FrustrationClassifier()
    # Usamos cv=3 porque es un dataset pequeño sintético
    metrics = classifier.train(df, cv=3)
    print(f"Métricas de entrenamiento: {metrics}")
    
    print("\n--- Generando Predicciones ---")
    # Predecir sobre los primeros 5 ejemplos
    test_df = df.head(5).copy()
    results = classifier.predict(test_df)
    print(results[['id_conv', 'is_frustrated', 'frustration_probability']])
    
    print("\n--- Explicabilidad SHAP ---")
    explainer = SHAPExplainer(classifier.model, classifier.features_cols)
    
    # Enriquecer dataframe
    enriched_df = explainer.enrich_with_explanations(results)
    print("\nRazones principales de frustración:")
    for _, row in enriched_df.iterrows():
        print(f"Conv: {row['id_conv']}, Prob: {row['frustration_probability']:.2f} -> {row['top_frustration_reasons']}")
        
    # Generar plot
    plot_path = "data/processed/shap_summary.png"
    explainer.generate_summary_plot(df, plot_path)
    print(f"\nPlot SHAP generado en: {plot_path}")

if __name__ == "__main__":
    test_week2()
