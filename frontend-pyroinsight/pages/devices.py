
from dash import Dash, html, dcc, register_page, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import requests

register_page(__name__)

# Define the layout
layout = html.Div([
    dcc.Interval(id='interval', interval=1000 * 10, n_intervals=0),  # Refresh every 10 seconds
    dash_table.DataTable(
        id='data-table',
    
    )
])

# Callback to update the DataTable with data from the FastAPI backend
@callback(
    Output('data-table', 'data'),
    Input('interval', 'n_intervals')
)
def update_data_table(n_intervals):
    response = requests.get('http://127.0.0.1:8000/all_device')
    data = response.json()
    return data