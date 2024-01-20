
from dash import Dash, html, dcc, register_page, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import requests
from components.device_table import *
from components.statistic_card import get_statistic_card
from components.graphs import *
from apis import get_disabled_devices_panel, average_measurement, get_average_measurement_device

register_page(__name__)

layout = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                dbc.Breadcrumb(
                    items=[
                        {"label": "Site 1", "active": True},
                        {"label": "Devices Dashboard", "active": True},
                    ],
                )
            ),
            dbc.Row(
                [
                    dbc.Col([device_table_card()], width=8),
                    dbc.Col([device_property_card()], width=4),
                ],
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dcc.Interval(id='interval', interval=1000 * 10, n_intervals=0),
                    dbc.Col([measurement_card("Obscuration", "latest-smoke", "bi bi-cloud-haze")], width=3),
                    dbc.Col([measurement_card("Temperature", "latest-heat", "bi bi-thermometer-half")], width=3),
                    dbc.Col([measurement_card("Carbon Monoxide", "latest-co", "bi bi-wind")], width=3),
                    dbc.Col([measurement_card("Dirtiness", "latest-dirtiness", "bi bi-trash")], width=3),
                ],
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dcc.Interval(id='interval', interval=1000 * 10, n_intervals=0),
                    dbc.Col([predict_dirtiness_card()], width=3),
                    dbc.Col([fault_card("Instantaneous Fault", "instantaneous_fault_state", "bi bi-x-circle")], width=3),
                    dbc.Col([fault_card("Confirmed Fault", "confirmed_fault_state", "bi bi-x-square")], width=3),
                    dbc.Col([fault_card("Acknowledged Fault", "acknowledged_fault_state", "bi bi-x-octagon")], width=3),
                ],
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([device_measurement_line_graph("period-dirtiness")], width=6),
                    dbc.Col([device_measurement_line_graph("period-smoke")], width=6),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([device_measurement_line_graph("period-heat")], width=6),
                    dbc.Col([device_measurement_line_graph("period-co")], width=6),
                ],
                align="center",    
            ),
        ]
    )
)
# # Callback to update the DataTable with data from the FastAPI backend
# @callback(
#     Output('data-table', 'data'),
#     Input('interval', 'n_intervals')
# )
# def update_data_table(n_intervals):
#     response = requests.get('http://127.0.0.1:8000/latest-panel/1/')
#     data = response.json()

#     # return data
#     selected_columns = ['id', 'device_type', 'units_of_measure1', 'converted_value1', 'units_of_measure2', 'converted_value2', 'units_of_measure3', 'converted_value3']
#     filtered_data = [{key: entry[key] for key in selected_columns} for entry in data]

#     return filtered_data