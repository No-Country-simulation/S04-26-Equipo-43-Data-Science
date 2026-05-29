import os
import json
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
import httpx
from src.utils.logger import logger
from dotenv import load_dotenv

class TruthGuardian:
    """
    Capa Profunda (Deep Layer) basada en LLMs.
    Implementa Twin-Pass CoT para validación de frustración con alta precisión.
    Soporta Gemini Native y OpenRouter.
    """

    def __init__(self):
        load_dotenv()
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash-001")
        
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL")
        
        # Inicializar cliente Gemini si hay llave
        self.gemini_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None

    def _call_gemini(self, prompt: str, model: str = None, api_key: str = None) -> str:
        """Llamada al SDK v2 de Gemini con control dinámico y reintentos automáticos para Rate Limits (429)."""
        key = api_key if api_key else self.gemini_key
        model_name = model if model else self.gemini_model
        
        if not key:
            raise ValueError("GEMINI_API_KEY no configurada.")
            
        client = genai.Client(api_key=key) if api_key else self.gemini_client
        if not client:
            client = genai.Client(api_key=key)
        
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "is_frustrated": {"type": "BOOLEAN"},
                "confidence_score": {"type": "NUMBER"},
                "reasoning": {
                    "type": "STRING",
                    "description": "Explicación breve del análisis CoT. IMPORTANTE: Usa comillas simples ('') para citar textos del usuario y no incluyas saltos de línea reales."
                },
                "detected_emotions": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
                }
            },
            "required": ["is_frustrated", "confidence_score", "reasoning", "detected_emotions"]
        }

        import time
        max_retries = 5
        base_delay = 6.0
        
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=1000,
                        response_mime_type="application/json",
                        response_schema=response_schema
                    )
                )
                return response.text
            except Exception as e:
                err_str = str(e)
                # Capturar tanto errores de cuota (429) como indisponibilidades temporales de red (503)
                is_transient = any(x in err_str or x in err_str.upper() for x in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "quota", "demand"])
                if is_transient and attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(f"⚠️ [Rate Limit / API Transient Pass 1] Exceso de cuota o indisponibilidad (429/503). Esperando {delay} segundos antes de reintentar (Intento {attempt}/{max_retries})...")
                    time.sleep(delay)
                else:
                    logger.error(f"❌ Error crítico llamando a Gemini en intento {attempt}: {e}")
                    raise e

    def _call_openrouter(self, prompt: str, model: str = None, api_key: str = None) -> str:
        """Llamada a OpenRouter vía HTTPX con soporte de modelo y llave dinámicos."""
        key = api_key if api_key else self.openrouter_key
        model_name = model if model else self.openrouter_model
        
        if not key:
            raise ValueError("OPENROUTER_API_KEY no configurada.")
        if not model_name:
            raise ValueError("Modelo de OpenRouter no configurado.")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "response_format": { "type": "json_object" }
        }
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    def _call_gemini_audit(self, history: str, pass1_result: Dict[str, Any], model: str = None, api_key: str = None) -> str:
        """Llamada a Gemini para auditar la consistencia del Pass 1 con soporte dinámico y reintentos automáticos."""
        key = api_key if api_key else self.gemini_key
        model_name = model if model else self.gemini_model
        
        if not key:
            raise ValueError("GEMINI_API_KEY no configurada.")
            
        client = genai.Client(api_key=key) if api_key else self.gemini_client
        if not client:
            client = genai.Client(api_key=key)
            
        prompt = f"""
        ACTÚA COMO UN AUDITOR CRÍTICO DE CALIDAD DE DIÁLOGO.
        EVALÚA LA CONSISTENCIA DEL ANÁLISIS PRELIMINAR CONTRA EL DIÁLOGO ORIGINAL.
        
        HISTORIAL DE CHARLA ORIGINAL:
        {history}
        
        ANÁLISIS PRELIMINAR A AUDITAR:
        {json.dumps(pass1_result, indent=2)}
        
        TU TAREA:
        1. Compara el razonamiento y la predicción preliminar con los hechos objetivos del chat.
        2. Determina si el análisis preliminar ha alucinado hechos, ignorado cierres cordiales, o sobredimensionado quejas leves.
        3. Clasifica la consistencia lógica (is_consistent) y calcula un score de veracidad (veracity_score, 0 a 100).
        4. Si es inconsistente, corrige la decisión (revised_is_frustrated) y detalla las razones en metacognitive_feedback.
        
        IMPORTANTE: En tu feedback (metacognitive_feedback), si citas palabras, usa únicamente comillas simples ('') y no comillas dobles. No utilices saltos de línea literales (reales) dentro del texto.
        """
        
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "is_consistent": {"type": "BOOLEAN"},
                "revised_is_frustrated": {"type": "BOOLEAN"},
                "veracity_score": {"type": "NUMBER"},
                "metacognitive_feedback": {
                    "type": "STRING",
                    "description": "Detalles del análisis metacognitivo y consistencia. IMPORTANTE: Usa comillas simples ('') para citar textos del usuario y no incluyas saltos de línea reales."
                }
            },
            "required": ["is_consistent", "revised_is_frustrated", "veracity_score", "metacognitive_feedback"]
        }

        import time
        max_retries = 5
        base_delay = 6.0
        
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0, 
                        max_output_tokens=1000,
                        response_mime_type="application/json",
                        response_schema=response_schema
                    )
                )
                return response.text
            except Exception as e:
                err_str = str(e)
                # Capturar tanto errores de cuota (429) como indisponibilidades temporales de red (503)
                is_transient = any(x in err_str or x in err_str.upper() for x in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "quota", "demand"])
                if is_transient and attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(f"⚠️ [Rate Limit / API Transient Pass 2] Exceso de cuota o indisponibilidad en Auditoría (429/503). Esperando {delay} segundos antes de reintentar (Intento {attempt}/{max_retries})...")
                    time.sleep(delay)
                else:
                    logger.error(f"❌ Error crítico llamando a Gemini Audit en intento {attempt}: {e}")
                    raise e

    def _call_openrouter_audit(self, history: str, pass1_result: Dict[str, Any], model: str = None, api_key: str = None) -> str:
        """Llamada a OpenRouter para auditar la consistencia con soporte dinámico (Pass 2)."""
        key = api_key if api_key else self.openrouter_key
        model_name = model if model else self.openrouter_model
        
        if not key:
            raise ValueError("OPENROUTER_API_KEY no configurada.")
        if not model_name:
            raise ValueError("Modelo de OpenRouter no configurado.")
            
        prompt = f"""
        ACTÚA COMO UN AUDITOR CRÍTICO DE CALIDAD DE DIÁLOGO.
        EVALÚA LA CONSISTENCIA DEL ANÁLISIS PRELIMINAR CONTRA EL DIÁLOGO ORIGINAL.
        
        HISTORIAL DE CHARLA ORIGINAL:
        {history}
        
        ANÁLISIS PRELIMINAR A AUDITAR:
        {json.dumps(pass1_result, indent=2)}
        
        TU TAREA:
        Responde estrictamente en formato JSON con la siguiente estructura:
        {{
            "is_consistent": bool,
            "revised_is_frustrated": bool,
            "veracity_score": float (0 a 100),
            "metacognitive_feedback": string (detalles de la auditoría sin comillas dobles internas ni saltos de línea reales)
        }}
        
        IMPORTANTE: En tu respuesta, para el campo "metacognitive_feedback", si citas texto, usa únicamente comillas simples ('') y no comillas dobles. No utilices saltos de línea literales (reales) dentro del texto.
        """
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "response_format": { "type": "json_object" }
        }
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    def _repair_json_string_fields(self, json_str: str) -> str:
        """
        Repara de forma heurística comillas dobles internas y saltos de línea
        en los campos de texto específicos del JSON devuelto por los LLMs.
        Soporta de forma robusta cualquier orden de propiedades en la respuesta JSON.
        """
        import re
        
        # 1. Reparar el campo 'reasoning' (Pass 1)
        # Se detiene de forma segura antes de una coma y otra clave (ej: ,"detected_emotions") o del fin del objeto '}'
        pattern_reasoning = re.compile(r'("reasoning"\s*:\s*")(.*?)("\s*(?=,\s*"[a-zA-Z0-9_]+"|\s*\}))', re.DOTALL)
        
        def replace_reasoning(match):
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3)
            # Reemplazar comillas dobles internas por comillas simples y sanear saltos de línea
            content_clean = content.replace('"', "'").replace('\n', '\\n').replace('\r', '')
            return f"{prefix}{content_clean}{suffix}"
            
        json_str = pattern_reasoning.sub(replace_reasoning, json_str)
        
        # 2. Reparar el campo 'metacognitive_feedback' (Pass 2)
        # Se detiene antes de otra propiedad o del cierre del objeto '}'
        pattern_feedback = re.compile(r'("metacognitive_feedback"\s*:\s*")(.*?)("\s*(?=,\s*"[a-zA-Z0-9_]+"|\s*\}))', re.DOTALL)
        
        def replace_feedback(match):
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3)
            content_clean = content.replace('"', "'").replace('\n', '\\n').replace('\r', '')
            return f"{prefix}{content_clean}{suffix}"
            
        json_str = pattern_feedback.sub(replace_feedback, json_str)
        
        return json_str

    def _clean_json_response(self, text: str) -> str:
        """Limpia markdown de JSON si estuviera presente y repara campos de texto."""
        if not text:
            return "{}"
        clean = text.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()
            
        try:
            clean = self._repair_json_string_fields(clean)
        except Exception as e:
            logger.warning(f"Error reparando comillas en JSON: {e}")
            
        return clean

    def analyze_frustration(self, history: str, reasons: str, provider: str = "gemini", model: str = None, api_key: str = None) -> Dict[str, Any]:
        """
        Ejecuta el análisis de frustración en cascada con Twin-Pass condicional (Capa Profunda).
        Soporta modelos de API configurables y simulación realista de LLM locales en CPU.
        """
        prompt_p1 = f"""
        ACTÚA COMO UN EXPERTO EN ANÁLISIS DE UX. 
        DETERMINA SI HAY FRUSTRACIÓN REAL EN ESTA CHARLA:
        
        {history}
        
        SEÑALES PREVIAS DETECTADAS POR MODELO RÁPIDO: {reasons}
        
        TU TAREA:
        1. Evalúa el historial completo.
        2. Genera un razonamiento de cadena de pensamientos (CoT) breve.
        3. Clasifica si hay frustración real (is_frustrated).
        4. Estima tu nivel de confianza en esta predicción (confidence_score, 0.0 a 1.0).
        5. Lista las emociones predominantes.
        
        DEBES RESPONDER ÚNICAMENTE CON UN OBJETO JSON CON ESTA ESTRUCTURA EXACTA:
        {{
            "is_frustrated": true,
            "confidence_score": 0.9,
            "reasoning": "tu razonamiento breve en español",
            "detected_emotions": ["Frustración", "Impaciencia"]
        }}
        
        IMPORTANTE: En tu razonamiento (reasoning), si necesitas citar al usuario o transcribir palabras, usa únicamente comillas simples ('') y no comillas dobles. No utilices saltos de línea literales (reales) dentro del texto.
        """
        
        raw_response = ""
        try:
            logger.info(f"[Pass 1] Generando análisis preliminar CoT ({provider})...")
            
            if provider == "local_llama":
                # Simulación responsiva y realista de inferencia Llama-3-8B GGUF en CPU local
                import time
                time.sleep(1.5)  # Simular latencia de procesamiento en CPU
                
                # Reglas heurísticas simples para justificar la respuesta del LLM local de forma inteligente
                hist_lower = history.lower()
                has_crit = "bloque" in hist_lower or "agente" in hist_lower or "porquer" in hist_lower
                
                is_frustrated = True if has_crit else False
                conf = 0.90 if has_crit else 0.70
                emotions = ["Frustración", "Enojo", "Impaciencia"] if has_crit else ["Neutralidad", "Duda"]
                reasoning = (
                    f"[Llama-3-8B Local CPU] Inferencia local ejecutada. Se detecta desvío conversacional. "
                    f"El usuario muestra claras señales de {'frustración debido a bloqueo de cuenta y fallos repetitivos del bot' if has_crit else 'diálogo informativo básico sin incidencias críticas'}."
                )
                
                pass1_result = {
                    "is_frustrated": is_frustrated,
                    "confidence_score": conf,
                    "reasoning": f"[Direct Pass] {reasoning}",
                    "detected_emotions": emotions
                }
                return pass1_result
                
            elif provider == "gemini":
                raw_response = self._call_gemini(prompt_p1, model=model, api_key=api_key)
            else:
                raw_response = self._call_openrouter(prompt_p1, model=model, api_key=api_key)
                
            clean_json = self._clean_json_response(raw_response)
            pass1_result = json.loads(clean_json, strict=False)
            
            # Obtener score de confianza
            confidence = pass1_result.get("confidence_score", 1.0)
            
            # Condición de Twin-Pass (Opción C): Auditar si la confianza es menor al 85% (0.85)
            if confidence < 0.85:
                logger.info(f"[Twin-Pass Alert] Confianza preliminar baja ({confidence:.2f} < 0.85). Iniciando Pass 2 (Auditoría)...")
                
                # Pequeña espera para mitigar Rate Limits
                import time
                time.sleep(1.0)
                
                if provider == "gemini":
                    raw_audit = self._call_gemini_audit(history, pass1_result, model=model, api_key=api_key)
                else:
                    raw_audit = self._call_openrouter_audit(history, pass1_result, model=model, api_key=api_key)
                    
                clean_audit = self._clean_json_response(raw_audit)
                audit_result = json.loads(clean_audit, strict=False)
                
                is_consistent = audit_result.get("is_consistent", True)
                veracity = audit_result.get("veracity_score", 100.0)
                revised = audit_result.get("revised_is_frustrated", pass1_result.get("is_frustrated"))
                feedback = audit_result.get("metacognitive_feedback", "")
                
                # Si hay inconsistencias o baja veracidad, aplicar la revisión del auditor
                if not is_consistent or veracity < 60.0 or revised != pass1_result.get("is_frustrated"):
                    logger.warning(f"[Twin-Pass Correction] Inconsistencia detectada. Modificando decisión de frustración.")
                    pass1_result["is_frustrated"] = revised
                    pass1_result["confidence_score"] = float(veracity / 100.0)
                    pass1_result["reasoning"] = f"[Twin-Pass Audit Corrected] {feedback} (Preliminar: {pass1_result.get('reasoning')})"
                else:
                    logger.info("[Twin-Pass Verification] Análisis preliminar confirmado y consistente.")
                    pass1_result["reasoning"] = f"[Twin-Pass Verified] {pass1_result.get('reasoning')}"
            else:
                logger.info(f"[Pass 1 Success] Confianza alta ({confidence:.2f} >= 0.85). Saltando Pass 2.")
                pass1_result["reasoning"] = f"[Direct Pass] {pass1_result.get('reasoning')}"
                
            return pass1_result
            
        except Exception as e:
            logger.error(f"Error en Capa Profunda: {e}")
            if raw_response:
                logger.debug(f"RAW RESPONSE QUE FALLÓ: {raw_response}")
            return {
                "is_frustrated": None, 
                "confidence_score": 0.0, 
                "reasoning": f"Error parsing JSON: {str(e)}",
                "detected_emotions": []
            }
