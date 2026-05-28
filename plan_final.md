# Rediseño Enterprise Dark Mode + Carga Dinámica Nativa

Refactorización completa del frontend de ConversaSense AI para adoptar la estética "Rendimiento Minimalista" de modo oscuro empresarial con datos 100% dinámicos, según los mockups de alta fidelidad.

---

## User Review Required

> [!IMPORTANT]
> **Cambio destructivo**: Se reescribirá por completo la capa de presentación (funciones `sidebar()`, `view_dashboard()`, `view_diagnostico()`, `view_intenciones()`, `nav_button()`, `render_*`) y los estilos de todos los componentes. La lógica de backend (`DashboardState`, `handle_upload`, `df_data`, computed vars) se **conserva y extiende** — no se borra.

> [!WARNING]
> **Heatmap estático eliminado**: El heatmap actual tiene datos hardcodeados (`[[8, 0, 9], [8, 1, 8], ...]`). Se reemplazará por un `@rx.var` que computa la matriz Intención×Frustración dinámicamente desde el parquet activo. Si no hay datos, se mostrará un estado vacío elegante.

---

## Proposed Changes

### Paleta de Diseño (Token System)

Colores extraídos de los mockups `interfaz_moderna1-3.png`:

| Token | Hex | Uso |
|-------|-----|-----|
| `bg_base` | `#0f1923` | Fondo principal del contenido |
| `bg_sidebar` | `#152232` | Fondo del sidebar |
| `bg_card` | `#1a2d42` | Tarjetas de datos |
| `bg_card_alt` | `#1e3448` | Tarjetas secundarias/hover |
| `accent_cyan` | `#00e5ff` | Links activos, bordes de selección, títulos destacados |
| `accent_lime` | `#76ff03` | Slider, valores positivos, tendencias up |
| `accent_orange` | `#ff6d00` | Alertas, frustración alta, sparkline frustración |
| `accent_red` | `#ff1744` | Fallas críticas (FALLA - Zona Gris) |
| `text_primary` | `#e0e6ed` | Texto principal |
| `text_secondary` | `#8899aa` | Texto secundario, labels |
| `border_subtle` | `#2a3f55` | Bordes de tarjetas |

---

### Componente 1: DashboardState (Extensión)

#### [MODIFY] [dashboard.py](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)

**Nuevos `@rx.var` computed:**

1. **`heatmap_data`** → `List[List[Any]]`: Computa dinámicamente la matriz Intención × rango de frustración desde `df_data`. Genera la estructura `[[x_idx, y_idx, value], ...]` que ECharts necesita para el heatmap. Las intenciones (eje Y) y los rangos de frustración de 0-10 (eje X) se derivan del archivo activo.

2. **`heatmap_intentions`** → `List[str]`: Lista de intenciones únicas detectadas en el parquet activo (eje Y del heatmap).

3. **`selected_confidence`** → `str`: Extrae el `confidence_score` del caso seleccionado para el medidor visual en la vista Diagnóstico.

4. **`priority_summary`** → `str`: Genera dinámicamente el texto del "Resumen de Prioridades (Crucial)" identificando la intención con mayor volumen × frustración.

5. **`performance_boost`** → `str`: Calcula el "Estimated Performance Boost" basado en la proporción de frustración corregible.

6. **Estado de carga (`is_uploading: bool`)**: Flag para mostrar spinner durante el procesamiento ETL.

**Cambio en `handle_upload`**: Añadir `self.is_uploading = True/False` al inicio/final del handler.

---

### Componente 2: Sidebar Empresarial

#### [MODIFY] [dashboard.py](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)

Reescribir `sidebar()` y `nav_button()`:

- **Fondo**: `bg_sidebar` (#152232), borde derecho `border_subtle`
- **Logo**: "ConversaSense" en blanco con accent cian
- **Nav activo**: Barra lateral izquierda cyan brillante (`border_left="3px solid #00e5ff"`), texto cyan
- **Nav inactivo**: Texto `text_secondary`, hover → `text_primary`
- **Slider Umbral**: Track en `accent_lime`, thumb con glow, valor digital en lime (`19.81`)
- **Selector de Archivo**: `rx.select` con fondo oscuro y bordes sutiles
- **Performance Stats Ticker** (nuevo): Card inferior mostrando "System real-time: Ingestion: X Mbps/s system/s" con valores dinámicos del conteo de registros
- **Botón "Cargar CSV/JSON"** (nuevo): Abre `rx.dialog.root` con `rx.upload` drag-and-drop para el pipeline ETL

---

### Componente 3: Vista Dashboard (Vista General)

#### [MODIFY] [dashboard.py](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)

Reescribir `view_dashboard()`, `render_kpi_card()`, `render_bullet_chart_mock()`, `render_sparkline()`:

1. **KPI Bullet Charts (3 tarjetas superiores)**:
   - Fondo `bg_card` con bordes `border_subtle` y `border_radius="12px"`
   - Barras horizontales con gradientes cyan→lime
   - Valor numérico dinámico + flecha de tendencia (↑ verde / ↓ rojo)
   - Labels en `text_secondary`

2. **Sparklines Panel**:
   - Fondo `bg_card`, título "Tendencias de Sentimiento (Sparklines)"
   - Badge "PRÓXIMO OBJETIVO: X.XX" en `accent_lime` (arriba-derecha)
   - Sparkline Positivo: gradiente cyan
   - Sparkline Neutral: gradiente amarillo/ámbar
   - Sparkline Frustración: gradiente naranja
   - Datos dinámicos generados desde `df_data`

3. **SHAP Global Bar Chart**:
   - Fondo `bg_card`
   - Barras horizontales con gradiente cyan→lime
   - Overlay tooltip "Ver Detalle AI" al hover
   - Datos dinámicos: leer feature importances del modelo si existe, sino mostrar las columnas de features con mayor varianza

---

### Componente 4: Vista Diagnóstico

#### [MODIFY] [dashboard.py](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)

Reescribir `view_diagnostico()` y `render_chat_message()`:

1. **Selector de Interacción**: `rx.select` con fondo oscuro, texto cyan
2. **Confidence Score Meter** (nuevo): Barra visual horizontal cyan con valor numérico (ej. "85%")
3. **Card Chain-of-Thought**:
   - Fondo `bg_card` con borde gradiente sutil cyan
   - Título "Razonamiento de Texto Profundo (Chain-of-Thought)" con iconos libro/engranaje en cyan
   - Texto principal con keywords resaltados en cyan (via parsing simple)
4. **Línea de Tiempo de Interacción**: 
   - Iconos User (persona cyan) y Bot (robot gris) alternados
   - Línea horizontal naranja conectando los nodos
   - Nodo final "FALLA - Zona Gris" en naranja/rojo con X
5. **Recomendación de Acción**:
   - Card con fondo `bg_card` ligeramente más claro
   - Badge "Expected F1 Improvement: +0.05" en `accent_lime`

---

### Componente 5: Vista Intenciones (Datos Cruciales)

#### [MODIFY] [dashboard.py](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)

Reescribir `view_intenciones()`:

1. **Heatmap Dinámico** (cambio crítico):
   - Datos computados por `heatmap_data` @rx.var
   - Gradiente de celdas: cian frío → naranja/rojo cálido (`["#0a3d5c", "#00897b", "#ffb300", "#ff6d00", "#d50000"]`)
   - Filas de alta frustración con bordes brillantes cyan
   - Micro-sparklines integradas en celdas del extremo derecho
   - Eje Y: intenciones dinámicas del parquet
   - Eje X: rangos 0-10

2. **Tabla de Flujos Críticos**:
   - Headers con gradiente `bg_card_alt`
   - Mini barras de progreso inline para Frustración
   - Iconos de tendencia (sparklines miniatura)
   - Filas de alta prioridad en negrita con accent
   - Datos 100% dinámicos de `intention_metrics`

3. **Resumen de Prioridades**:
   - Card sleek con borde cyan
   - Texto generado dinámicamente por `priority_summary`
   - Badge "Estimated Performance Boost: +0.07" en `accent_lime`

---

### Componente 6: Layout y App Global

#### [MODIFY] [dashboard.py](file:///C:/Users/opaye/Proyectos/SC/src/dashboard/dashboard/dashboard.py)

- `main_content()`: Fondo `bg_base` (#0f1923)
- `index()`: Layout horizontal sidebar + main sin spacing
- Google Font "Inter" via `rx.App(style={...})`
- Logo sparkle decorativo en esquina inferior derecha

---

## Verificación

### Compilación
```bash
cd src/dashboard && ..\..\venv\Scripts\reflex.exe compile --dry
```

### Manual
1. Abrir el navegador → verificar que las 3 vistas reflejan los mockups
2. Cargar un CSV de prueba via el botón → verificar procesamiento en tiempo real
3. Cambiar el archivo de inferencia activo → verificar que heatmap, métricas y tabla se actualizan
4. Verificar slider de umbral con valor digital en lima
5. Verificar que el "Resumen de Prioridades" cambia dinámicamente según los datos
