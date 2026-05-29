import os
import sys
import json
import time
from typing import List, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.logger import logger
from src.core.ingest_adapter import IngestAdapter
from src.core.feature_extractor import FeatureExtractor
from src.core.feature_aggregator import FeatureAggregator

# Cargar variables de entorno
load_dotenv()

# Configuración de Modelos
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
OTHER_MODELS_STR = os.getenv("OTHER_MODELS", "")

# Compilar lista de modelos disponibles
ALL_MODELS = [PRIMARY_MODEL]
if OTHER_MODELS_STR:
    # Limpiar y separar nombres técnicos de los otros modelos
    others = [m.strip() for m in OTHER_MODELS_STR.split(",") if m.strip()]
    ALL_MODELS.extend(others)
    
# Asegurar nombres técnicos limpios (evitar repeticiones)
ALL_MODELS = list(dict.fromkeys(ALL_MODELS))
logger.info(f"Modelos de generación configurados en .env: {ALL_MODELS}")

# Definición de Escenarios Semilla (ES / PT)
SEED_SCENARIOS = [
    # --- ESPAÑOL (ES) ---
    {
        "id_base": "CONV_GEN_ES_NORMAL_01",
        "lang": "es",
        "type": "normal",
        "description": "Consulta de saldo ordinaria de cuenta corriente. Diálogo fluido, el bot comprende a la primera y el cliente agradece y se despide de forma normal."
    },
    {
        "id_base": "CONV_GEN_ES_CRITICA_02",
        "lang": "es",
        "type": "frustrated",
        "description": "Reposición de tarjeta robada. El bot no entiende y repite el menú genérico 2 veces. El usuario muestra impaciencia, escribe en mayúsculas y exige un agente humano de inmediato."
    },
    {
        "id_base": "CONV_GEN_ES_CRITICA_03",
        "lang": "es",
        "type": "frustrated",
        "description": "Reclamo por cobro duplicado de suscripción. El bot responde con un fallback genérico. El usuario se irrita fuertemente, usa ironías y sarcasmo ('gracias por nada, excelente atención') y corta el chat abruptamente."
    },
    {
        "id_base": "CONV_GEN_ES_NORMAL_04",
        "lang": "es",
        "type": "normal",
        "description": "Instrucciones de activación de token móvil. El bot guía al usuario paso a paso y el usuario completa la operación exitosamente cerrando el chat de forma cordial."
    },
    {
        "id_base": "CONV_GEN_ES_GRIS_05",
        "lang": "es",
        "type": "frustrated",
        "description": "Consulta de portabilidad bancaria. El bot da instrucciones obsoletas sobre ir a la sucursal. El usuario desiste conversacionalmente diciendo: 'deja así, no sirve para nada, olvídalo'."
    },
    
    # --- PORTUGUÉS (PT) ---
    {
        "id_base": "CONV_GEN_PT_NORMAL_06",
        "lang": "pt",
        "type": "normal",
        "description": "Consulta de limite disponível do cartão de crédito. Diálogo rápido, bot responde correto e o cliente encerra com 'muito obrigado'."
    },
    {
        "id_base": "CONV_GEN_PT_CRITICA_07",
        "lang": "pt",
        "type": "frustrated",
        "description": "Bloqueio de segurança de conta Pix. O bot entra em loop mandando ir na agência. O cliente usa vocabulário vulgar de raiva ('palhaçada', 'que merda', 'pqp') e exige falar com supervisor."
    },
    {
        "id_base": "CONV_GEN_PT_NORMAL_08",
        "lang": "pt",
        "type": "normal",
        "description": "Solicitação de segunda via de boleto. O bot fornece o PDF de imediato, o usuário agradece e o bot responde com reboot padrão."
    },
    {
        "id_base": "CONV_GEN_PT_CRITICA_09",
        "lang": "pt",
        "type": "frustrated",
        "description": "Cobrança indevida no cartão de crédito. O bot dá resposta automática irrelevante. O cliente responde com sarcasmo irônico ('obrigado por nada, ótima ajuda') e exige suporte humano especializado."
    },
    {
        "id_base": "CONV_GEN_PT_GRIS_10",
        "lang": "pt",
        "type": "frustrated",
        "description": "Atualização de dados cadastrais. O bot falha no upload de selfie de segurança e repete o comando 3 veces. O cliente desiste e sai da conversa dizendo 'esquece, deixa pra lá, não adianta'."
    }
]

def generate_conversation_from_llm(client: genai.Client, model: str, seed: Dict[str, Any], var_idx: int, profile_desc: str) -> List[Dict[str, Any]]:
    """Llama a la API de Gemini para generar un diálogo estructurado basado en un escenario semilla y un perfil de cliente específico."""
    var_id = f"{seed['id_base']}_VAR_{var_idx}"
    
    prompt = f"""
    ACTÚA COMO UN SIMULADOR LINGÜÍSTICO DE DIÁLOGOS DE SOPORTE.
    Genera un historial completo de chat para atención al cliente de banca/fintech/e-commerce.
    
    ESCENARIO SEMILLA A SIMULAR:
    - ID Conversación: {var_id}
    - Idioma: {'Español (ES)' if seed['lang'] == 'es' else 'Portugués (PT)'}
    - Tipo: {'Conversación fluida/Normal' if seed['type'] == 'normal' else 'Conversación con alta frustración/fricción del usuario'}
    - Descripción del caso: {seed['description']}
    
    PERFIL ESPECÍFICO DEL CLIENTE PARA ESTA VARIACIÓN:
    - Estilo lingüístico / Actitud: {profile_desc}
    
    TU TAREA:
    1. Genera un diálogo realista de entre 4 y 8 turnos de interacción total (incluyendo mensajes de user y bot alternados).
    2. Las respuestas del Bot deben reflejar el comportamiento indicado (si es exitoso o si comete errores/fallbacks/loops).
    3. Los mensajes del Usuario deben ser realistas al idioma, tipo y perfil específico indicado (ej: usar exclamaciones, sarcasmo, gírias brasileñas/portuguesas si corresponde, repeticiones o expresiones de descontento).
    4. La salida debe seguir ESTRICTAMENTE la estructura JSON requerida.
    """
    
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "conversations": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "id_conv": {"type": "STRING"},
                        "turno": {"type": "INTEGER"},
                        "rol": {"type": "STRING"},
                        "mensaje": {"type": "STRING"}
                    },
                    "required": ["id_conv", "turno", "rol", "mensaje"]
                }
            }
        },
        "required": ["conversations"]
    }
    
    try:
        logger.info(f"Llamando a {model} para {var_id} con perfil: {profile_desc[:40]}...")
        # Aumentamos la temperatura ligeramente para mayor variedad
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.85,
                max_output_tokens=1500,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        # Limpieza de Markdown y comillas internas
        import re
        text_clean = response.text.strip()
        if "```json" in text_clean:
            text_clean = text_clean.split("```json")[1].split("```")[0].strip()
        elif "```" in text_clean:
            text_clean = text_clean.split("```")[1].split("```")[0].strip()
            
        # Reparar de forma heurística comillas internas en el campo 'mensaje'
        pattern_msg = re.compile(r'("mensaje"\s*:\s*")(.*?)("\s*(?=\s*\}|\s*,\s*"\w+"))', re.DOTALL)
        def replace_msg(match):
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3)
            # Reemplazar comillas internas por simples y sanear saltos de línea
            content_clean = content.replace('"', "'").replace('\n', '\\n').replace('\r', '')
            return f"{prefix}{content_clean}{suffix}"
            
        text_clean = pattern_msg.sub(replace_msg, text_clean)
        
        data = json.loads(text_clean)
        
        # Estandarizar ID de conversación en el JSON resultante para asegurar coincidencia
        conversations = data.get("conversations", [])
        for msg in conversations:
            msg["id_conv"] = var_id
            
        logger.info(f"[OK] Generados {len(conversations)} turnos de chat para {var_id}.")
        return conversations
    except Exception as e:
        logger.error(f"Error generando diálogo con {model} para {var_id}: {e}")
        return []

def main():
    if not GEMINI_KEY:
        logger.error("No se encontró GEMINI_API_KEY en el entorno. Asegúrate de configurar tu .env.")
        return
        
    client = genai.Client(api_key=GEMINI_KEY)
    
    logger.info("--- Iniciando Generación Aumentada de Datos (MLOps) mediante LLMs ---")
    logger.info(f"Modelos disponibles: {ALL_MODELS}")
    
    # Perfiles lingüísticos para español
    profiles_es = [
        "Persona muy directa, quiere resolver rápido, no le gustan los rodeos.",
        "Persona de edad avanzada, le cuesta entender la tecnología, usa explicaciones largas.",
        "Persona impaciente, escribe con exclamaciones y en mayúsculas al primer error.",
        "Persona formal, usa ironías sutiles cuando no le solucionan (sarcasmo conversacional).",
        "Persona ansiosa, escribe frases cortas y seguidas.",
        "Persona muy cordial, saluda con amabilidad pero se frustra si el bot repite menús.",
        "Persona joven que usa muchas abreviaturas de chat (tqm, k, xq) y modismos informales.",
        "Persona desesperada, menciona que le urge porque tiene que hacer un pago ya mismo.",
        "Persona que exige hablar con un humano o soporte técnico rápidamente.",
        "Persona resignada o decepcionada que desiste rápidamente diciendo 'deja así, no sirve'."
    ]
    
    # Perfiles lingüísticos para portugués
    profiles_pt = [
        "Pessoa muito direta, quer resolver rápido, não gosta de enrolação.",
        "Pessoa mais velha, tem dificuldade com tecnologia, usa explicações longas.",
        "Pessoa impaciente, escreve com exclamações e em maiúsculas no primeiro erro.",
        "Pessoa formal, usa ironia sutil quando não resolvem o problema (sarcasmo).",
        "Pessoa ansiosa, escreve frases curtas e repetitivas.",
        "Pessoa muito cordial, cumprimenta com simpatia mas se frustra se o bot repetir menus.",
        "Pessoa jovem que usa muitas abreviações de chat (vc, tb, pq) e gírias locais.",
        "Pessoa desesperada, menciona que é urgente porque precisa fazer um pagamento agora.",
        "Pessoa que exige falar com um atendente humano ou suporte técnico rapidamente.",
        "Pessoa resignada ou desapontada que desiste rapidamente dizendo 'deixa pra lá, não adianta'."
    ]
    
    all_generated_messages = []
    
    # Total escenarios = 10. Para cada escenario generamos 10 variaciones = 100 diálogos.
    total_calls = len(SEED_SCENARIOS) * 10
    call_idx = 0
    
    for seed in SEED_SCENARIOS:
        profiles = profiles_es if seed["lang"] == "es" else profiles_pt
        
        for var_idx in range(10):
            profile_desc = profiles[var_idx]
            # Asignar modelo de forma rotativa entre los 5 modelos configurados
            model_to_use = ALL_MODELS[call_idx % len(ALL_MODELS)]
            
            # Evitar sobrecarga y rate limits espaciando las llamadas
            if call_idx > 0:
                time.sleep(1.0)
                
            conversations = generate_conversation_from_llm(client, model_to_use, seed, var_idx, profile_desc)
            all_generated_messages.extend(conversations)
            call_idx += 1
            
    if not all_generated_messages:
        logger.error("No se pudo generar ningún dato. Revisa las conexiones de API.")
        return
        
    # 1. Guardar el archivo JSON crudo generado en data/raw
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    raw_path = os.path.join(raw_dir, "conversaciones_generadas_gemini.json")
    
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(all_generated_messages, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ Dataset crudo (100+ diálogos) guardado exitosamente en: {raw_path}")
    
    # 2. Ejecutar Pipeline ETL de Extracción en memoria para generar el Parquet de Features
    logger.info("\n--- Ejecutando Pipeline de Extracción de Características ETL ---")
    
    adapter = IngestAdapter()
    extractor = FeatureExtractor()  # Usa MiniLM multilingüe local para embeddings
    aggregator = FeatureAggregator()
    
    df_raw = adapter.load_json(raw_path)
    if df_raw.empty:
        logger.error("El DataFrame cargado de conversaciones generadas está vacío.")
        return
        
    # Extraer variables
    df_msg = extractor.extract_message_features(df_raw)
    df_msg = extractor.extract_bot_signals(df_msg)
    df_msg = extractor.compute_semantic_coherence(df_msg)
    df_features = aggregator.aggregate_conversation_features(df_msg)
    
    # Asignar etiqueta real de frustración según el tipo de escenario semilla
    seed_types = {seed['id_base']: (1 if seed['type'] == 'frustrated' else 0) for seed in SEED_SCENARIOS}
    
    def get_is_frustrated(id_conv):
        base_id = id_conv.split('_VAR_')[0]
        return seed_types.get(base_id, 0)
        
    df_features['is_frustrated'] = df_features['id_conv'].apply(get_is_frustrated)
    
    # Guardar en data/processed
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    processed_path = os.path.join(processed_dir, "conversaciones_generadas_gemini.parquet")
    
    df_features.to_parquet(processed_path, index=False)
    logger.info(f"✅ Matriz de Características guardada en Parquet: {processed_path}")
    logger.info(f"Longitud del nuevo Dataset de Inferencia Generado: {len(df_features)} conversaciones.")
    logger.info(f"Distribución de clases en datos de entrenamiento:\n{df_features['is_frustrated'].value_counts()}")
    
    # Imprimir un resumen de las features agregadas
    print("\n--- Vista Resumida de las Características Generadas ---")
    print(df_features[['id_conv', 'total_turns', 'bot_fallback_count', 'negation_count', 'is_frustrated']].head(10))
    
    print("\n¡Listo! Ahora puedes ir al Dashboard y seleccionar 'conversaciones_generadas_gemini.parquet' para visualizarlo.")

if __name__ == "__main__":
    main()
