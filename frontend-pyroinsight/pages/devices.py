
from dash import Dash, html, dcc, register_page, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import requests
from components.device_table import *
from components.statistic_card import get_statistic_card
from components.other import *

register_page(__name__)

def failure():
    try:
        # Fetch data from an API
        response = requests.get("http://127.0.0.1:8000/failure/0/")
        data = response.json()

        return str(data)
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def average_obscuration():
    try:
        # Fetch data from an API
        response = requests.get("http://127.0.0.1:8000/average-obscuration/0/")
        data = response.json()

        return str(data)
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

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
                    # dcc.Interval(id='interval', interval=1000 * 10, n_intervals=0),
                    dbc.Col([get_statistic_card("Failed devices", failure())], width=4),
                    dbc.Col([get_statistic_card("Average Obscuration", average_obscuration())], width=4),
                    dbc.Col([get_statistic_card("Devices disabled this year", "10")], width=4),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([panel_status_line_graph()], width=4),
                    dbc.Col([dfgraph()], width=4),
                    dbc.Col([dfgraph()], width=4),
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