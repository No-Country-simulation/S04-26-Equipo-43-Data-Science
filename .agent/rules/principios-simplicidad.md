---
trigger: when_writing_code
---

# 🔪 Principios de Simplicidad Absoluta

## 1. Patrones Directos sobre Complejidad
Usa el patrón más simple que resuelva el problema actual.
No introduzcas abstracciones "por si acaso" en el futuro.

```python
# MAL ❌ (Sobreingeniería)
class ConversationRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    def get_by_id(self, id_conv):
        result = self.db.query("SELECT * FROM convs WHERE id = ?", id_conv)
        return ConversationEntity(result)

# BIEN ✅ (Directo y simple)
def get_conversation(df: pd.DataFrame, id_conv: str) -> pd.DataFrame:
    logger.log_sequence('Buscando conversación', id_conv)
    return df[df['id_conv'] == id_conv]
```

## 2. Separación de Responsabilidades (Básica)
Agrupa código por componente, no por tipo técnico.

```text
# MAL ❌ (Agrupación técnica)
├── scripts/
│   ├── extract_features.py
│   └── aggregate.py
└── data/
    ├── features.csv
    └── agg.csv

# BIEN ✅ (Agrupación por componente/dominio)
├── src/core/
│   ├── feature_extractor.py
│   └── feature_aggregator.py
```

## 3. Manejo de Errores Pragmático
Evita estructuras de try/catch masivas y anidadas.
Falla rápido y usa el DLQ (Dead Letter Queue) o retorna explícitamente en lugar de tragar errores en silencio.

```python
# MAL ❌
def process_message(msg):
    try:
        # 100 líneas de código
        pass
    except Exception as e:
        pass # Silencio fatal

# BIEN ✅
def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    try:
        return ConversationSchema.validate(df)
    except pa.errors.SchemaErrors as err:
        save_to_dlq(df, str(err))
        return pd.DataFrame()
```
