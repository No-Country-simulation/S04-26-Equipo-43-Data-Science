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

    def _call_gemini(self, prompt: str) -> str:
        """Llamada nativa a Gemini SDK v2 con esquema de respuesta estricto."""
        if not self.gemini_client:
            raise ValueError("GEMINI_API_KEY no configurada.")
        
        # Esquema de respuesta estricto basado en el skill gemini-sdk-v2
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "is_frustrated": {"type": "BOOLEAN"},
                "confidence_score": {"type": "NUMBER"},
                "reasoning": {"type": "STRING"},
                "detected_emotions": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
                }
            },
            "required": ["is_frustrated", "confidence_score", "reasoning", "detected_emotions"]
        }

        response = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=1000,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return response.text

    def _call_openrouter(self, prompt: str) -> str:
        """Llamada a OpenRouter vía HTTPX (OpenAI compatible)."""
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY no configurada.")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.openrouter_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "response_format": { "type": "json_object" }
        }
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    def _call_gemini_audit(self, history: str, pass1_result: Dict[str, Any]) -> str:
        """Llamada a Gemini para auditar la consistencia del Pass 1 (Pass 2)."""
        if not self.gemini_client:
            raise ValueError("GEMINI_API_KEY no configurada.")
            
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
        """
        
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "is_consistent": {"type": "BOOLEAN"},
                "revised_is_frustrated": {"type": "BOOLEAN"},
                "veracity_score": {"type": "NUMBER"},
                "metacognitive_feedback": {"type": "STRING"}
            },
            "required": ["is_consistent", "revised_is_frustrated", "veracity_score", "metacognitive_feedback"]
        }

        response = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0, # Temperatura 0 para consistencia estricta
                max_output_tokens=1000,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return response.text

    def _call_openrouter_audit(self, history: str, pass1_result: Dict[str, Any]) -> str:
        """Llamada a OpenRouter para auditar la consistencia (Pass 2)."""
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY no configurada.")
            
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
            "metacognitive_feedback": string (detalles de la auditoría)
        }}
        """
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.openrouter_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "response_format": { "type": "json_object" }
        }
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    def _clean_json_response(self, text: str) -> str:
        """Limpia markdown de JSON si estuviera presente."""
        clean = text.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()
        return clean

    def analyze_frustration(self, history: str, reasons: str, provider: str = "gemini") -> Dict[str, Any]:
        """
        Ejecuta el análisis de frustración en cascada con Twin-Pass condicional (Capa Profunda).
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
        """
        
        raw_response = ""
        try:
            logger.info(f"[Pass 1] Generando análisis preliminar CoT ({provider})...")
            if provider == "gemini":
                raw_response = self._call_gemini(prompt_p1)
            else:
                raw_response = self._call_openrouter(prompt_p1)
                
            clean_json = self._clean_json_response(raw_response)
            pass1_result = json.loads(clean_json)
            
            # Obtener score de confianza
            confidence = pass1_result.get("confidence_score", 1.0)
            
            # Condición de Twin-Pass (Opción C): Auditar si la confianza es menor al 85% (0.85)
            if confidence < 0.85:
                logger.info(f"[Twin-Pass Alert] Confianza preliminar baja ({confidence:.2f} < 0.85). Iniciando Pass 2 (Auditoría)...")
                
                # Pequeña espera para mitigar Rate Limits
                import time
                time.sleep(1.0)
                
                if provider == "gemini":
                    raw_audit = self._call_gemini_audit(history, pass1_result)
                else:
                    raw_audit = self._call_openrouter_audit(history, pass1_result)
                    
                clean_audit = self._clean_json_response(raw_audit)
                audit_result = json.loads(clean_audit)
                
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
