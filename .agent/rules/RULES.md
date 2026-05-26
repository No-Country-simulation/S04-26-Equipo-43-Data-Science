---
trigger: always_on
---

# 📚 Índice de Reglas del Proyecto

Este archivo sirve como índice. Las reglas principales están en `.agent/rules/`.

---

## Archivos de Rules

| Archivo | Trigger | Descripción |
|---------|---------|-------------|
| [topologia-agentes.md](topologia-agentes.md) | `always_on` | 🎭 Roles del proyecto |
| [instrucciones-comportamiento.md](instrucciones-comportamiento.md) | `always_on` | 📜 Patrones de trabajo |
| [principios-simplicidad.md](principios-simplicidad.md) | `always_on` | 🔧 Reglas de código |
| [principios-responsive.md](principios-responsive.md) | `always_on` | 📱 Diseño responsive |
| [stack-tecnologico.md](stack-tecnologico.md) | `always_on` | 📦 Stack tecnológico |
| [decisiones-pendientes.md](decisiones-pendientes.md) | `always_on` | 📋 Decisiones por tomar |
| [detector-tecnologias.md](detector-tecnologias.md) | `always_on` | 🔍 Detecta tecnologías y sugiere workflows |

---

## Rules por Skill

Cada skill tiene sus reglas específicas:

| Skill | Rules |
|-------|-------|
| creador-skills | `resources/rules.md` |
| gestor-rules | `resources/rules.md` |
| monitor-skills | `resources/rules.md` |

---

## Cómo Funcionan los Triggers

- `trigger: always_on` -> Se aplica siempre en cada interacción
- Sin trigger -> Se aplica cuando es relevante al contexto

---

## Historial de Sincronización de Contexto

- **2026-05-25**: Ejecución de `/alinear-contexto`. Se limpiaron residuos de la plantilla "Flashcard/React" en `principios-simplicidad.md` y se alineó el stack a Python/Pandas/LightGBM para ConversaSense AI.

