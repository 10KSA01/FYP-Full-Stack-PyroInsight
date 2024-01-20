from dash import Dash, html, dcc, register_page
import dash_bootstrap_components as dbc
from components.sidebar import get_sidebar
from components.statistic_card import get_statistic_card
from components.graphs import *
from apis import average_measurement, get_latest_faulty_devices_panel, get_latest_disabled_devices_panel, get_latest_healthy_devices_panel

register_page(__name__, path='/')

layout = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                dbc.Breadcrumb(
                    items=[
                        {"label": "Site 1", "active": True},
                        {"label": "Main Dashboard", "active": True},
                    ],
                )
            ),
            dbc.Row(
                [
                    dbc.Col([panel_measurement_line_graph(0, "dirtiness")], width=6),
                    dbc.Col([panel_measurement_line_graph(0, "smoke")], width=6),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([panel_measurement_line_graph(0, "heat")], width=6),
                    dbc.Col([panel_measurement_line_graph(0, "co")], width=6),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_statistic_card("Current disabled devices", get_latest_disabled_devices_panel(0), "bi bi-slash-circle")], width=4),
                    dbc.Col([get_statistic_card("Current faulty devices", get_latest_faulty_devices_panel(0), "bi bi-bug")], width=4),
                    dbc.Col([get_statistic_card("Current healthy devices", get_latest_healthy_devices_panel(0), "bi bi-heart-pulse")], width=4),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_statistic_card("Average Obscuration", average_measurement(0, "smoke"), "bi bi-cloud-haze")], width=3),
                    dbc.Col([get_statistic_card("Average Temperature", average_measurement(0, "heat"), "bi bi-thermometer-half")], width=3),
                    dbc.Col([get_statistic_card("Average Carbon Monoxide", average_measurement(0, "co"), "bi bi-wind")], width=3),
                    dbc.Col([get_statistic_card("Average Dirtiness", average_measurement(0, "dirtiness"), "bi bi-trash")], width=3),
                ],
                align="center",    
            ),
            
        ]
    )
)