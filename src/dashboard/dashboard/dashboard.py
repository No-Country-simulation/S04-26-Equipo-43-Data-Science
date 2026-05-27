import reflex as rx
import pandas as pd
from typing import List, Dict, Any
from reflex_echarts import echarts

import os

# Load dataset once globally for performance
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed", "features_S1.parquet"))
try:
    df_global = pd.read_parquet(DATA_PATH)
    # Synthetic frustration score based on signals for demo purposes
    df_global['frustration_score'] = (
        df_global['bot_fallback_count'] * 20 + 
        df_global['user_repetition_ratio'] * 50 + 
        df_global['escalation_requested'].astype(int) * 30
    ).clip(0, 100)
except Exception as e:
    # Fallback to empty df if not found
    df_global = pd.DataFrame({'frustration_score': [], 'bot_fallback_count': []})

class DashboardState(rx.State):
    """El estado global de la aplicación Reflex."""
    
    # Navegación
    current_view: str = "Dashboard"
    
    # Filtros
    idioma: str = "ES/EN"
    fecha: str = "Todas"
    umbral_frustracion: float = 50.0
    
    @rx.var
    def metrics(self) -> Dict[str, str]:
        if df_global.empty:
            return {"avg_frustration": "0%", "gray_zone_vol": "0%", "response_time": "0s"}
            
        # Filtrar por umbral
        df_filtered = df_global[df_global['frustration_score'] >= self.umbral_frustracion]
        
        if df_filtered.empty:
            return {"avg_frustration": "0%", "gray_zone_vol": "0%", "response_time": "1.2s"}
            
        avg_frust = df_filtered['frustration_score'].mean()
        # Gray zone (casos entre 45 y 75)
        gray_zone = len(df_global[(df_global['frustration_score'] >= 45) & (df_global['frustration_score'] <= 75)])
        gray_vol = (gray_zone / len(df_global)) * 100 if len(df_global) > 0 else 0
        
        # Simulando F1 y Kappa dinámicos que se degradan si el umbral es muy extremo
        f1_sim = 0.85 - (abs(self.umbral_frustracion - 50) * 0.005)
        kappa_sim = 0.70 - (abs(self.umbral_frustracion - 50) * 0.006)
        
        return {
            "avg_frustration": f"{avg_frust:.1f}%",
            "gray_zone_vol": f"{gray_vol:.1f}%",
            "response_time": "1.2s", # static mock for now
            "f1_score": f"{max(0, f1_sim):.2f}",
            "kappa": f"{max(0, kappa_sim):.2f}",
            "total_records": f"{len(df_filtered):,}"
        }

    def set_umbral(self, value: list[float]):
        if isinstance(value, list) and len(value) > 0:
            self.umbral_frustracion = value[0]

    def set_view(self, view: str):
        self.current_view = view

def render_sparkline(title: str, color: str, data: List[int]) -> rx.Component:
    """Genera un sparkline minimalista usando ECharts, sin ejes (Gestalt)."""
    option = {
        "xAxis": {"type": "category", "show": False, "boundaryGap": False},
        "yAxis": {"type": "value", "show": False, "min": "dataMin", "max": "dataMax"},
        "series": [{
            "data": data, "type": "line", "smooth": True, "symbol": "none",
            "lineStyle": {"color": color, "width": 2},
            "areaStyle": {
                "color": {
                    "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [{"offset": 0, "color": f"{color}80"}, {"offset": 1, "color": f"{color}00"}]
                }
            }
        }],
        "grid": {"left": 0, "right": 0, "top": 0, "bottom": 0},
        "tooltip": {"show": False}
    }
    return rx.vstack(
        rx.text(title, font_weight="500", color="gray.11"),
        rx.box(echarts(option=option), width="100%", height="80px"),
        align_items="flex-start", width="100%"
    )

def render_bullet_chart_mock(title: str, value: str) -> rx.Component:
    return rx.vstack(
        rx.text(title, font_size="lg", font_weight="medium"),
        rx.box(
            rx.box(width=value, height="100%", bg="gray.10", position="absolute", left="0", top="0"),
            rx.box(width="2px", height="120%", bg="black", position="absolute", left="75%", top="-10%"),
            width="100%", height="24px", bg="gray.4", position="relative", border="1px solid", border_color="gray.6"
        ),
        rx.hstack(
            rx.text("Target", font_size="xs", color="gray.9"),
            rx.spacer(),
            rx.text(value, font_size="xs", color="gray.11", font_weight="bold"),
            width="100%"
        ),
        width="100%", padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white"
    )

def render_kpi_card(title: str, value: str, target: str) -> rx.Component:
    return rx.vstack(
        rx.text(title, font_size="sm", color="gray.11", font_weight="500"),
        rx.text(value, font_size="2xl", font_weight="bold"),
        rx.text(f"Target: {target}", font_size="xs", color="gray.9"),
        padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white", width="100%"
    )

def view_dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Interface 1: Visión General y Métricas Científicas", size="5", margin_bottom="4"),
        
        rx.grid(
            render_kpi_card("F1-Score (Híbrido)", DashboardState.metrics["f1_score"], "≥ 0.80"),
            render_kpi_card("Cohen's Kappa", DashboardState.metrics["kappa"], "0.50 - 0.60"),
            render_kpi_card("Mensajes Procesados", DashboardState.metrics["total_records"], "Volumen Actual"),
            columns="3", spacing="4", width="100%", margin_bottom="4"
        ),

        rx.grid(
            render_bullet_chart_mock("Promedio de Frustración", DashboardState.metrics["avg_frustration"]),
            render_bullet_chart_mock("Volumen Zona Gris", DashboardState.metrics["gray_zone_vol"]),
            render_bullet_chart_mock("Velocidad de Respuesta", DashboardState.metrics["response_time"]),
            columns="3", spacing="4", width="100%"
        ),
        rx.box(
            rx.text("Tendencias de Sentimiento (Sparklines)", font_size="xl", font_weight="bold", margin_bottom="4"),
            rx.grid(
                render_sparkline("Positivo", "#9ca3af", [10, 15, 12, 18, 14, 22, 20, 25, 23]),
                render_sparkline("Neutral", "#9ca3af", [20, 22, 20, 18, 25, 22, 21, 23, 20]),
                render_sparkline("Frustración", "#4b5563", [5, 8, 15, 10, 12, 20, 18, 25, 30]),
                columns="3", spacing="6", width="100%"
            ),
            padding="6", border="1px solid", border_color="gray.5", border_radius="md", bg="white", width="100%", margin_top="6"
        ),
        width="100%", align_items="flex-start"
    )

def view_diagnostico() -> rx.Component:
    return rx.vstack(
        rx.heading("Interface 2: Vista Diagnóstico", size="5", margin_bottom="4"),
        rx.box(
            rx.text("Seleccionar Interacción (Zona Gris/Falla)", font_weight="bold"),
            rx.select(["ID 4521 - 10:30 AM", "ID 4522 - 10:35 AM"], default_value="ID 4521 - 10:30 AM", width="100%"),
            padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white", width="100%"
        ),
        rx.grid(
            rx.box(
                rx.text("Razonamiento de Texto Profundo (Chain-of-Thought)", font_weight="bold", margin_bottom="2"),
                rx.text("El usuario inició solicitando ayuda con una tarjeta bloqueada. El bot no reconoció la intención 'tarjeta bloqueada'. El usuario repitió la solicitud tres veces. El bot respondió con el menú genérico. El usuario abandonó. La causa raíz es la falta de entrenamiento en la intención específica de bloqueo de tarjeta.", color="gray.11"),
                padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white"
            ),
            rx.box(
                rx.text("Línea de Tiempo de Interacción (Visual)", font_weight="bold", margin_bottom="2"),
                rx.hstack(
                    rx.vstack(rx.icon("user", color="gray.11"), rx.text("Ayuda tarjeta", size="1"), align_items="center"),
                    rx.icon("arrow-right", color="gray.8"),
                    rx.vstack(rx.icon("bot", color="gray.11"), rx.text("Menú genérico", size="1"), align_items="center"),
                    rx.icon("arrow-right", color="gray.8"),
                    rx.vstack(rx.icon("user", color="gray.11"), rx.text("Ayuda tarjeta", size="1"), align_items="center"),
                    rx.icon("arrow-right", color="gray.8"),
                    rx.vstack(rx.icon("bot", color="gray.11"), rx.text("Menú genérico", size="1"), align_items="center"),
                    rx.icon("arrow-right", color="gray.8"),
                    rx.vstack(rx.icon("x-circle", color="red.9"), rx.text("Falla", size="1", color="red.9"), align_items="center"),
                    spacing="2", align_items="center", justify_content="center", height="100px"
                ),
                padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white"
            ),
            columns="2", spacing="4", width="100%", margin_top="4"
        ),
        rx.box(
            rx.text("Recomendación de Acción", font_weight="bold", margin_bottom="2"),
            rx.text("Entrenar intención 'Tarjeta Bloqueada' con nuevos ejemplos. Revisar flujo de escalado para evitar bucles.", color="gray.11"),
            padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white", width="100%", margin_top="4"
        ),
        width="100%", align_items="flex-start"
    )

def view_intenciones() -> rx.Component:
    heatmap_option = {
        "tooltip": {"position": "top"},
        "grid": {"height": "70%", "top": "10%"},
        "xAxis": {"type": "category", "data": ["0","1","2","3","4","5","6","7","8","9","10"], "splitArea": {"show": True}},
        "yAxis": {"type": "category", "data": ["Tarjeta Bloq.", "Clave", "Saldo", "Pago"], "splitArea": {"show": True}},
        "visualMap": {
            "min": 0, "max": 10, "calculable": True, "orient": "horizontal", "left": "center", "bottom": "0%",
            "inRange": {"color": ["#f3f4f6", "#9ca3af", "#4b5563"]}
        },
        "series": [{
            "name": "Frustración", "type": "heatmap",
            "data": [[8, 0, 9], [8, 1, 8], [4, 0, 8], [9, 3, 5], [10, 0, 9]],
            "label": {"show": False},
            "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}}
        }]
    }

    return rx.vstack(
        rx.heading("Interface 3: Top Intenciones Fallidas", size="5", margin_bottom="4"),
        rx.grid(
            rx.box(
                rx.text("Cruce de Datos: Intención vs. Frustración", font_weight="bold", margin_bottom="2"),
                echarts(option=heatmap_option, height="300px"),
                padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white"
            ),
            rx.box(
                rx.text("Listado de Flujos Fallidos Críticos", font_weight="bold", margin_bottom="2"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Intención Original"),
                            rx.table.column_header_cell("Volumen"),
                            rx.table.column_header_cell("Frustración"),
                            rx.table.column_header_cell("Acción"),
                        ),
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Tarjeta Bloqueada"), rx.table.cell("120"), rx.table.cell("8.5"), rx.table.cell(rx.text("Re-entrenar", font_weight="bold"))),
                        rx.table.row(rx.table.cell("Actualización Datos"), rx.table.cell("120"), rx.table.cell("8.5"), rx.table.cell("Revisar Flujo")),
                        rx.table.row(rx.table.cell("Pagar Servicio"), rx.table.cell("110"), rx.table.cell("8.5"), rx.table.cell("Ignorar")),
                    ),
                    width="100%"
                ),
                padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white"
            ),
            columns="2", spacing="4", width="100%"
        ),
        rx.box(
            rx.text("Resumen de Prioridades (Crucial)", font_weight="bold", margin_bottom="2"),
            rx.text("Prioridad Alta: Intención 'Tarjeta Bloqueada' genera 60% de la frustración en la zona gris (Vol: 120). Requiere acción inmediata.", color="gray.11"),
            padding="4", border="1px solid", border_color="gray.5", border_radius="md", bg="white", width="100%", margin_top="4"
        ),
        width="100%", align_items="flex-start"
    )

def nav_button(text: str, icon: str, view_name: str) -> rx.Component:
    return rx.button(
        rx.icon(icon, size=18),
        rx.text(text, size="3"),
        on_click=lambda: DashboardState.set_view(view_name),
        variant="ghost",
        color=rx.cond(DashboardState.current_view == view_name, "black", "gray.10"),
        bg=rx.cond(DashboardState.current_view == view_name, "gray.4", "transparent"),
        justify_content="flex-start",
        width="100%",
        margin_bottom="2"
    )

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading("ConversaSense", size="6", margin_bottom="6"),
        nav_button("Dashboard", "layout-dashboard", "Dashboard"),
        nav_button("Diagnóstico", "activity", "Diagnóstico"),
        nav_button("Intenciones", "list", "Intenciones"),
        rx.divider(margin_y="4"),
        rx.text("FILTROS", size="2", font_weight="bold", color="gray.9"),
        rx.text("Idioma", size="2"),
        rx.select(["ES/EN", "ES", "EN"], value=DashboardState.idioma, width="100%"),
        rx.text("Fecha", size="2", margin_top="4"),
        rx.select(["Todas", "Hoy", "Última Semana"], value=DashboardState.fecha, width="100%"),
        rx.text("Umbral Frustración", size="2", margin_top="4"),
        rx.slider(default_value=[50.0], min=0.0, max=100.0, on_value_commit=DashboardState.set_umbral, width="100%"),
        rx.text(f"{DashboardState.umbral_frustracion}%", size="2", color="gray.10"),
        width="250px", height="100vh", padding="6", bg="gray.2", border_right="1px solid", border_color="gray.5", align_items="flex-start"
    )

def main_content() -> rx.Component:
    return rx.box(
        rx.match(
            DashboardState.current_view,
            ("Dashboard", view_dashboard()),
            ("Diagnóstico", view_diagnostico()),
            ("Intenciones", view_intenciones()),
            view_dashboard()
        ),
        width="100%", padding="8", bg="gray.1", min_height="100vh"
    )

def index() -> rx.Component:
    return rx.hstack(sidebar(), main_content(), width="100%", spacing="0")

app = rx.App()
app.add_page(index, title="ConversaSense Dashboard")