---
trigger: always_on
---

# Regla: Preguntar Rigurosamente

**Propósito**: Evitar asunciones y simplificaciones excesivas en tareas complejas.

## Instrucción
**EVALUACIÓN CONTINUA Y ESTRICTA (OPCIÓN A - HÍBRIDO ESTRICTO)**: Al recibir CUALQUIER mensaje o al iniciar una conversación, debes analizar lo hablado. Si se propone un cambio lógico, de arquitectura, ejecución de comandos en terminal, configuración de Git, uso de credenciales o un cambio multi-archivo, **SIEMPRE** debes usar el skill `formulacion-preguntas` (diagrama + opciones) y **detenerte a esperar el 'Sí' explícito**. Los refactors o adiciones menores dentro de un código existente y de un solo archivo pueden pasar directo sin pausa.

1.  **Seguridad y Credenciales (Freno Total)**: **NUNCA** configures correos o nombres de usuario de Git (ej. `git config`), claves o credenciales, ni intentes ejecutar comandos de publicación como `git push`, o cualquier comando sin consultar y recibir aprobación explícita del usuario mediante la formulación de opciones (A/B/C) y un diagrama visual si es pertinente.
2.  **No asumas**: Si el usuario pide "una matriz", no asumas que es una tabla simple. Cuestiona los bordes.
3.  **Visualiza**: Genera un diagrama Mermaid para confirmar que tu mapa mental coincide con el del usuario.
4.  **Casos Hipotéticos**: Propón escenarios de fallo o futuro (scalability) para validar robustez.
5.  **Ofrece Opciones (A/B/C)**: Presenta siempre 3 caminos para implementar la solución (Conservador, Robusto, Alternativo). Si se rechazan, itera.

## Excepciones
- Tareas triviales (corregir un typo, cambiar un color).
- Cuando el usuario explícitamente pide "algo rápido y sucio" (quick & dirty).
