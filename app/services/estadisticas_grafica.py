"""
Módulo de Servicios de Estadísticas.
Procesa datos crudos y genera gráficas interactivas usando Plotly.
"""
from datetime import date, timedelta
import plotly.express as px


class EstadisticasService:

    @staticmethod
    def generar_grafica_ultimos_dias(registros, dias=30):
        """Genera una gráfica de barras mostrando el progreso de los últimos 'X' o '15' días."""
        hoy = date.today() # ej. yyyy-mm-dd

        # 1. Crear lista de los últimos 14 días (del más antiguo al de hoy)
        # range(inicio, fin, salto) - timedelta es una función matemática para fechas.
        ultimos_dias = [hoy - timedelta(days=i) for i in range(dias - 1, -1, -1)]

        # 2. Extraer solo las fechas en las que el hábito sí se completó
        fechas_completadas = {registro.fecha for registro in registros if registro.completado}

        # 3. Construir Eje X (Días) y Eje Y (1 si completó, 0 si falló)
        eje_x = [d.strftime("%d/%m") for d in ultimos_dias]
        eje_y = [1 if d in fechas_completadas else 0 for d in ultimos_dias]

        # 4. Crear la gráfica interactiva con Plotly Express
        fig = px.line(
            x=eje_x,
            y=eje_y,
            title=f"Progreso de los últimos {dias} días",
            markers=True,
            color_discrete_sequence=['#235336']
        )

        # 5. Personalizar el diseño para que luzca limpio y combine con tu CSS
        fig.update_layout(
            yaxis=dict(tickvals=[0, 1], ticktext=['Fallado', 'Completado']),
            coloraxis_showscale=False,  # Ocultar la barra lateral de colores
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )

        # 6. Convertir a HTML crudo (incluyendo el código JS de Plotly automáticamente)
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
