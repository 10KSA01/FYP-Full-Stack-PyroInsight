from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import requests
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd
from apis import get_latest_panel_data, get_latest_device_data
from apis import get_average_measurement_device
from components.statistic_card import get_statistic_card

selected_columns = ['id', 'datetime', 'device_type', 'units_of_measure1', 'converted_value1', 'units_of_measure2', 'converted_value2', 'units_of_measure3', 'converted_value3']
current_selected_row = ""

def device_table_card():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Panel 1 Devices"),
                    dbc.CardBody(
                        [
                            dcc.Interval(id='interval', interval=1000 * 100, n_intervals=0),  # Refresh every 10 seconds
                            dag.AgGrid(
                                id="device-table",
                                columnDefs=[{"field": i} for i in selected_columns],
                                # rowModelType="infinite",
                                columnSize="autoSize",
                                defaultColDef=dict(
                                    resizable=True, sortable=True, filter=True, minWidth=100
                                ),
                                dashGridOptions={"pagination": True, "rowSelection": "single"},
                                style={'height': '600px'}
                            ),
                        ]
                    )
                ]
            ),
        ]
    )

def device_property_card():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Row(
                            [
                                dbc.Col("Device Properties"),
                            ],
                        )
                    ),
                    dbc.CardBody(
                        [
                            dash_table.DataTable(id='data-table', columns=[], data=[], style_table={'height': '600px'}),
                        ]
                    )            
                ]
            ),
        ]
    )

# Device Properties Table
# Callback to update the device statistic card when a new row is selected in the device table
# @callback(
#     Output('device-statistic-card', 'children'),
#     Input('device-table', 'selectedRows'),
#     prevent_initial_call=True,
# )
# def update_device_statistic_card(selectedRows, title, type):
#     if selectedRows:
#         id = selectedRows[0]['id']
#         return id
#     else:
#         return "NaN"

# def device_statistic_card(text, type):
#     value = update_device_statistic_card()
#     if value != "NaN":
#         value = get_average_measurement_device(update_device_statistic_card, type)
#     return get_statistic_card(text, value)

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

def measurement_card(title, type):
    return html.Div(
        dbc.CardGroup(
            [
                dbc.Card(
                    html.Div(className="bi bi-slash-circle", style=card_icon),
                    className="bg-primary",
                    style={"maxWidth": 75, "maxHeight": 90},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(title, style={"margin": "0"}),
                            html.H4(children="NaN", id=type, style={"margin": "0"}),
                        ]
                    ), 
                    style={"maxHeight": 90}
                ),
            ],
        )
    )

@callback(
    Output('smoke', 'children'),
    Output('heat', 'children'),
    Output('co', 'children'),
    Output('dirtiness', 'children'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_measurement_cards(selectedRows):
    if selectedRows:   
        current_selected_row = selectedRows[0]['id']
        smoke_data = get_average_measurement_device(current_selected_row, "smoke")
        heat_data = get_average_measurement_device(current_selected_row, "heat")
        co_data = get_average_measurement_device(current_selected_row, "co")
        dirtiness_data = get_average_measurement_device(current_selected_row, "dirtiness")

        return smoke_data or "NaN", heat_data or "NaN", co_data or "NaN", dirtiness_data or "NaN"
    else:
        return "NaN", "NaN", "NaN", "NaN" 


# Callback to update the AgGrid table with filtered data from the backend
@callback(
    Output('device-table', 'rowData'),
    Input('interval', 'n_intervals')
)
def update_device_table(n_intervals):
    # selected_columns = ['id', 'datetime', 'device_type', 'units_of_measure1', 'converted_value1', 'units_of_measure2', 'converted_value2', 'units_of_measure3', 'converted_value3']
    filtered_data = [{key: entry[key] for key in selected_columns} for entry in get_latest_panel_data(0)]
    
    return filtered_data

# Device Properties Table
@callback(
    Output('data-table', 'columns'),
    Output('data-table', 'data'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_data_table(selectedRows):
    if selectedRows:   
        current_selected_row = selectedRows[0]['id']
        data = get_latest_device_data(current_selected_row)

        if not data:
            return [], []  # No data available

        # Transpose the data to swap rows and columns
        transposed_data = [{'Header': key, 'Data': value} for key, value in data[0].items()]

        return [{'name': 'Header', 'id': 'Header'}, {'name': 'Data', 'id': 'Data'}], transposed_data
    else:
        return [], []