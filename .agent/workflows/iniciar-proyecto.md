---
description: Iniciar un nuevo proyecto web responsive
---

# Flujo: Iniciar Proyecto Web Responsive

## Pasos

### 1. Sesión de Clarificación Profunda (OBLIGATORIO)
Antes de crear cualquier archivo, se debe ejecutar el skill `formulacion-preguntas` para definir el alma del proyecto.
- **Definición del Propósito**: ¿Qué problema resuelve exactamente?
- **Casos de Uso Extremos**: ¿Qué pasará si el sistema recibe inputs inesperados?
- **Posibles Falencias**: ¿Dónde están los puntos débiles de la lógica propuesta?
- **Falta de Coherencia**: ¿Los componentes propuestos hablan el mismo idioma técnico?
- **Confirmación del Stack**: Validar con el usuario si el stack tecnológico actual en `.agent/rules/stack-tecnologico.md` es el indicado o debe cambiarse.

### 2. Actualizar el Stack y Decisiones
- Usar `gestor-rules` para reflejar cualquier cambio en `stack-tecnologico.md`.
- Documentar las decisiones de esta sesión en `.agent/rules/decisiones-pendientes.md`.

### 3. Crear Estructura de Carpetas
Crear la base técnica:
   - `src/` - Código fuente principal
   - `src/components/` - Componentes reutilizables
   - `src/pages/` - Páginas o vistas principales
   - `src/utils/` - Funciones helper y logs
   - `src/styles/` - CSS y estilos
   - `assets/` - Imágenes, iconos, fuentes
   - `docs/` - Documentación del proyecto

// turbo
4. Crear archivo `src/utils/logger.js` con sistema de logs

5. Crear archivo `src/styles/variables.css` con breakpoints responsive

6. Crear `index.html` base con meta viewport para responsive

7. Documentar decisiones finales en `.agent/rules/decisiones-pendientes.md`
