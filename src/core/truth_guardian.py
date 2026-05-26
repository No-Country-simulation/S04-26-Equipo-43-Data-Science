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

    def analyze_frustration(self, history: str, reasons: str, provider: str = "gemini") -> Dict[str, Any]:
        """
        Ejecuta el análisis de frustración con el LLM.
        """
        prompt = f"""
        ACTÚA COMO UN EXPERTO EN ANÁLISIS DE UX. 
        DETERMINA SI HAY FRUSTRACIÓN REAL EN ESTA CHARLA:
        
        {history}
        
        SEÑALES PREVIAS DETECTADAS POR MODELO RÁPIDO: {reasons}
        
        TU TAREA:
        1. Evalúa el historial completo.
        2. Genera un razonamiento breve.
        3. Clasifica si hay frustración real.
        4. Lista las emociones predominantes.
        """
        
        raw_response = ""
        try:
            logger.info(f"Llamando a Capa Profunda ({provider}) para análisis CoT...")
            
            if provider == "gemini":
                raw_response = self._call_gemini(prompt)
            else:
                raw_response = self._call_openrouter(prompt)
            
            # Limpieza básica por seguridad
            clean_json = raw_response.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()
            
            return json.loads(clean_json)
            
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
