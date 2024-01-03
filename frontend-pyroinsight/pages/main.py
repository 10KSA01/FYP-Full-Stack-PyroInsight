from dash import Dash, html, dcc, register_page
import dash_bootstrap_components as dbc
from components.sidebar import get_sidebar
from components.statistic_card import get_statistic_card
from components.other import *

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
                    dbc.Col([panel_obscuration_line_graph()], width=6),
                    dbc.Col([dfgraph()], width=6),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_statistic_card("Devices disabled this year", "10")], width=4),
                    dbc.Col([get_statistic_card("Devices disabled this year", "15")], width=4),
                    dbc.Col([get_statistic_card("Devices disabled this year", "20")], width=4),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_statistic_card("Devices disabled this year", "10")], width=4),
                    dbc.Col([get_statistic_card("Devices disabled this year", "10")], width=4),
                    dbc.Col([get_statistic_card("Devices disabled this year", "10")], width=4),
                ],
                align="center",    
            ),
            
        ]
    )
)