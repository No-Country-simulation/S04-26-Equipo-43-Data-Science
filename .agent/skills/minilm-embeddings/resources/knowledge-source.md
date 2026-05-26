# Knowledge Source: paraphrase-multilingual-MiniLM-L12-v2

**URL:** https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
**Fecha de Captura:** 2026-05-26

## Contenido Procesado

### Resumen Técnico
El modelo `paraphrase-multilingual-MiniLM-L12-v2` es un transformer ligero (MiniLM) optimizado para la generación de embeddings de oraciones multilingües. Es parte de la familia `sentence-transformers` y se destaca por su equilibrio entre **velocidad y precisión**.

### Especificaciones Clave
- **Dimensiones:** 384
- **Parámetros:** ~118 millones
- **Idiomas:** 50+ (incluyendo ES, PT, EN, FR, DE, ZH, etc.)
- **Arquitectura:** MiniLM-L12 (12 capas, pooling de media por defecto)
- **Tamaño en disco:** ~420MB (Float32)

### Comparativa de Rendimiento
- **Velocidad:** Es entre 2x y 3x más rápido que modelos basados en MPNet o RoBERTa.
- **Latencia:** Ideal para aplicaciones en tiempo real (inferencia en CPU < 15ms por frase).
- **Precisión:** Ligeramente inferior (3-5%) a modelos "Base" más grandes, pero suficiente para la mayoría de tareas de clasificación y búsqueda semántica.

### Casos de Uso en este Proyecto
En **ConversaSense AI**, este modelo se utiliza para:
1. Calcular el `cosine_similarity` entre los mensajes del usuario y el bot.
2. Identificar la coherencia semántica en tiempo real sin penalizar la experiencia de usuario (SLA < 3 min para 20k conversaciones).
3. Servir como "señal rápida" para el clasificador LightGBM.

### Código de Implementación (Exacto)
```python
from sentence_transformers import SentenceTransformer, util

# Carga del modelo
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Generación de embeddings
sentences = ["Hola, tengo un problema", "Oi, eu tenho um problema"]
embeddings = model.encode(sentences, convert_to_tensor=True)

# Cálculo de similitud
sim = util.cos_sim(embeddings[0], embeddings[1])
print(f"Similitud: {sim.item()}")
```
