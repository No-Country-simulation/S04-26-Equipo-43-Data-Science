import os
from google import genai
from dotenv import load_dotenv


def list_and_check_gemini_models():
    # Cargar variables de entorno
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ Error: GEMINI_API_KEY no encontrada.")
        return

    # Crear cliente
    client = genai.Client(api_key=api_key)

    print("\n🔍 LISTANDO MODELOS GEMINI DISPONIBLES\n")

    try:
        # Obtener modelos
        models = client.models.list()

        for m in models:

            # Filtrar solo modelos Gemini
            if "gemini" not in m.name.lower():
                continue

            print("=" * 80)
            print(f"🧠 Modelo: {m.name}")

            try:
                # Probar generación
                response = client.models.generate_content(
                    model=m.name,
                    contents="Di exactamente: OK",
                    config={
                        "temperature": 0,
                        "max_output_tokens": 10
                    }
                )

                print("✅ ACTIVO")

                # Mostrar respuesta
                if response.text:
                    print("💬 Respuesta:", response.text)
                else:
                    print("⚠️ El modelo no devolvió texto.")

            except Exception as e:
                print(f"❌ ERROR: {e}")

            print()

    except Exception as e:
        print(f"❌ Error al listar modelos: {e}")


if __name__ == "__main__":
    list_and_check_gemini_models()