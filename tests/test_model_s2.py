import pandas as pd
import numpy as np
import os
from src.core.frustration_classifier import FrustrationClassifier
from src.core.explainability import SHAPExplainer

def generate_synthetic_data(n_samples=500):
    """Genera datos sintéticos para probar el modelo."""
    np.random.seed(42)
    
    data = {
        'id_conv': [f"C{i}" for i in range(n_samples)],
        'total_turns': np.random.randint(2, 20, n_samples),
        'avg_cosine_similarity': np.random.uniform(0.1, 0.9, n_samples),
        'char_elongation_count': np.random.randint(0, 3, n_samples),
        'user_message_count': np.random.randint(1, 10, n_samples),
        'avg_user_message_length': np.random.uniform(10, 100, n_samples),
        'negation_count': np.random.randint(0, 5, n_samples),
        'bot_fallback_count': np.random.randint(0, 4, n_samples),
        'escalation_requested': np.random.choice([True, False], n_samples, p=[0.1, 0.9]),
    }
    
    df = pd.DataFrame(data)
    
    # Crear variable objetivo (frustración) basada en reglas sintéticas
    # Alta probabilidad de frustración si hay escalamiento, muchos fallbacks o baja similitud
    prob = (
        df['escalation_requested'] * 0.4 + 
        (df['bot_fallback_count'] > 1) * 0.3 + 
        (df['avg_cosine_similarity'] < 0.3) * 0.2 + 
        (df['negation_count'] > 2) * 0.1
    )
    
    # Añadir algo de ruido
    prob += np.random.normal(0, 0.1, n_samples)
    
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
