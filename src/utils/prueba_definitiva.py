import os
from google import genai
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno (como GEMINI_API_KEY)
    load_dotenv()
    
    # Lista de modelos a probar harcodeada según lo solicitado
    models = [
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-3-flash-preview",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash"
    ]
    
    # Inicializar cliente de Gemini
    # Por defecto usará la variable de entorno GEMINI_API_KEY
    client = genai.Client()
    
    pregunta = "¿Qué tan inteligente eres?"
    
    print(f"Iniciando prueba con la pregunta: '{pregunta}'\n")
    print("-" * 50)
    
    for model in models:
        print(f"Consultando al modelo: {model}...")
        try:
            response = client.models.generate_content(
                model=model,
                contents=pregunta,
            )
            print(f"Respuesta de {model}:\n{response.text}\n")
        except Exception as e:
            print(f"Error al consultar el modelo {model}:\n{e}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
