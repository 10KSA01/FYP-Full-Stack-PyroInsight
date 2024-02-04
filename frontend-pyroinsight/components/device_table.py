from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import requests
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd
from apis import *
from components.statistic_card import get_statistic_card
from constants import fault_list

selected_columns = ['id', 'datetime', 'device_type', 'converted_value1', 'converted_value2', 'converted_value3', 'instantaneous_fault_state', 'confirmed_fault_state', 'acknowledged_fault_state']
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
                                    resizable=True, sortable=True, filter=True, minWidth=160
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
                            dash_table.DataTable(
                                id='data-table', 
                                columns=[], 
                                data=[], 
                                style_table={'height': '600px'},
                                style_cell={
                                    'minWidth': '50px', # minimum width of each column
                                    'width': '50px',    # width of each column
                                    'maxWidth': '50px', # maximum width of each column
                                },
                            )
                        ]
                    )            
                ]
            ),
        ]
    )

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
    
card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

def measurement_card(title, type, icon):
    return html.Div(
        dbc.CardGroup(
            [
                dbc.Card(
                    html.Div(className=icon, style=card_icon),
                    className="bg-primary",
                    style={"maxWidth": 75, "maxHeight": 90},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(f"Average {title}", style={"margin": "0"}),
                            html.H4(children="Not Applicable", id=type, style={"margin": "0"}),
                        ]
                    ), 
                    style={"maxHeight": 90}
                ),
            ],
        )
    )

@callback(
    Output('latest-smoke', 'children'),
    Output('latest-heat', 'children'),
    Output('latest-co', 'children'),
    Output('latest-dirtiness', 'children'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_measurement_cards(selectedRows):
    if selectedRows:   
        current_selected_row = selectedRows[0]['id']
        
        latest_smoke_data = get_average_measurement_device(current_selected_row, "smoke")
        latest_heat_data = get_average_measurement_device(current_selected_row, "heat")
        latest_co_data = get_average_measurement_device(current_selected_row, "co")
        latest_dirtiness_data = get_average_measurement_device(current_selected_row, "dirtiness")
        
        return latest_smoke_data or "Not Applicable", latest_heat_data or "Not Applicable", latest_co_data or "Not Applicable", latest_dirtiness_data or "Not Applicable"
    else:
        return "Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable" 

def predict_dirtiness_card():
    return html.Div(
        dbc.CardGroup(
            [
                dbc.Card(
                    html.Div(className="bi bi-calendar2-heart", style=card_icon),
                    className="bg-primary",
                    style={"maxWidth": 75, "maxHeight": 90},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(f"Needs cleaning on", style={"margin": "0"}),
                            html.H4(children="Not Applicable", id="predict_dirtiness", style={"margin": "0"}),
                        ]
                    ), 
                    style={"maxHeight": 90}
                ),
            ],
        )
    )

@callback(
    Output('predict_dirtiness', 'children'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_predict_dirtiness_card(selectedRows):
    if selectedRows:   
        current_selected_row = selectedRows[0]['id']
        predict_dirtiness = get_predict_dirtiness_device(current_selected_row)

        return predict_dirtiness or "Not Applicable"
    else:
        return "Not Applicable"

def fault_card(title, fault, icon):
    return html.Div(
        dbc.CardGroup(
            [
                dbc.Card(
                    html.Div(className=icon, style=card_icon),
                    className="bg-primary",
                    style={"maxWidth": 75, "maxHeight": 90},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(f"{title}", style={"margin": "0"}),
                            html.H4(children="No Faults", id=fault, style={"margin": "0"}),
                        ]
                    ), 
                    style={"maxHeight": 90}
                ),
            ],
        )
    )

@callback(
    Output('instantaneous_fault_state', 'children'),
    Output('confirmed_fault_state', 'children'),
    Output('acknowledged_fault_state', 'children'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_measurement_cards(selectedRows):
    if selectedRows:   
        current_selected_row = selectedRows[0]['id']
        instantaneous_fault = fault_list[get_latest_column_device_data(current_selected_row, "instantaneous_fault_state")["instantaneous_fault_state"]]
        confirmed_fault = fault_list[get_latest_column_device_data(current_selected_row, "confirmed_fault_state")["confirmed_fault_state"]]
        acknowledged_fault = fault_list[get_latest_column_device_data(current_selected_row, "acknowledged_fault_state")["acknowledged_fault_state"]]

        return instantaneous_fault or "No Faults", confirmed_fault or "No Faults", acknowledged_fault or "No Faults"
    else:
        return "No Faults", "No Faults", "No Faults"

def device_measurement_line_graph(type):
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(children="No", id=type)
                ]
            ),
        ]
    )

def panel_measurement_line_graph(id, data, title, units, type, predict):
    if not data:
        return html.Div(f"No data available for {id} - {title}")

    datetime = [point['datetime'] for point in data]
    measurement = [point[type] for point in data]
    
    datetime_predict = [prediction['datetime'] for prediction in predict]
    measurement_predict = [prediction[type] for prediction in predict]
    return html.Div(
        [
            dbc.CardHeader(f"{id} - {title}"),
            dbc.CardBody(
                [
                    dcc.Graph(
                        figure = {
                            'data': [
                                {'x': datetime, 'y': measurement, 'mode': 'lines', 'name': 'Real'},
                                {'x': datetime_predict, 'y': measurement_predict, 'mode': 'lines', 'name': 'Prediction'}
                            ],
                            'layout': {
                                'xaxis': {'title': 'Date & Time'},
                                'yaxis': {'title': units}
                            }
                        }
                    )
                ]
            )
        ]
    )

@callback(
    Output('period-smoke', 'children'),
    Output('period-heat', 'children'),
    Output('period-co', 'children'),
    Output('period-dirtiness', 'children'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_measurement_cards(selectedRows):
    if selectedRows:   
        id = selectedRows[0]['id']
        measure_columns = {
            "period-smoke": ("Obscuration", "Obscuration (%/m)", get_measurement_device_period(id, "smoke"), "smoke", get_measurement_device_predict(id, "smoke")),
            "period-heat": ("Temperature", "Temperature (°C)", get_measurement_device_period(id, "heat"), "heat", get_measurement_device_predict(id, "heat")),
            "period-co": ("Carbon Monoxide", "Carbon Monoxide (ppm)", get_measurement_device_period(id, "co"), "co", get_measurement_device_predict(id, "co")),
            "period-dirtiness": ("Dirtiness", "Dirtiness", get_measurement_device_period(id, "dirtiness"), "dirtiness", get_measurement_device_predict(id, "dirtiness"))
        }

        title, units, data, type, predict = measure_columns["period-smoke"]
        period_smoke_data = panel_measurement_line_graph(id, data, title, units, type, predict)
        
        title, units, data, type, predict = measure_columns["period-heat"]
        period_heat_data = panel_measurement_line_graph(id, data, title, units, type, predict)
        
        title, units, data, type, predict = measure_columns["period-co"]
        period_co_data = panel_measurement_line_graph(id, data, title, units, type, predict)
        
        title, units, data, type, predict = measure_columns["period-dirtiness"]
        period_dirtiness_data = panel_measurement_line_graph(id, data, title, units, type, predict)
        
        
        return period_smoke_data or "Not Applicable", period_heat_data or "Not Applicable", period_co_data or "Not Applicable", period_dirtiness_data or "Not Applicable"
    else:
        return "Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable" 