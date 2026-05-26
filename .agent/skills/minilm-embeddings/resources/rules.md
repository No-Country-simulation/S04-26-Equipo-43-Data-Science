# Reglas Específicas: MiniLM Embeddings

## Reglas de Implementación
1. **Carga Única**: El modelo debe cargarse una sola vez en el constructor de la clase para evitar sobrecarga de memoria.
2. **Uso de Tensores**: Siempre que se use PyTorch, utilizar `convert_to_tensor=True` en el método `encode` para acelerar el cálculo de similitud.
3. **Manejo de Longitud**: El modelo tiene un límite de 128 o 256 tokens. Truncar textos extremadamente largos antes de enviarlos al modelo para evitar errores de memoria.
4. **Normalización**: Por defecto, `util.cos_sim` maneja la normalización, pero si se usa otro método manual, recordar normalizar los vectores a norma unitaria.

## Umbrales Sugeridos para Frustración
- **Similitud > 0.8**: Alta coherencia (el bot respondió lo que el usuario pidió).
- **Similitud < 0.3**: Posible quiebre del diálogo (el bot respondió algo irrelevante o genérico).
- **Similitud < 0.1**: Ruido o fallo total de entendimiento.
