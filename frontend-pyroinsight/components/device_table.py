from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import requests
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd

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
                                style={'height': '500px'}
                            ),
                        ]
                    )
                ]
            ),
        ]
    )
dropdown = dbc.DropdownMenu(
    label="Download",
    children=[
        dbc.DropdownMenuItem("Current data", id="current-data"),
        dcc.Download(id="download-current-data"),
        dbc.DropdownMenuItem("History of the device", id="history-data"),
        dcc.Download(id="download-history-data"),
    ],
    size="sm",
)

def device_property_card():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Row(
                            [
                                dcc.Store(id='selected-rows-store'),
                                dbc.Col("Device Properties"),
                                dbc.Col(dropdown,style={"textAlign": "right"}),
                            ],
                        )
                    ),
                    dbc.CardBody(
                        [
                            dash_table.DataTable(id='data-table', columns=[], data=[], style_table={'height': '500px'}),
                        ]
                    )            
                ]
            ),
        ]
    )
    
@callback(
    Output('selected-rows-store', 'data'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def store_selected_rows(selectedRows):
    # print("hi",selectedRows)
    return selectedRows

@callback(
    Output("download-current-data", "data"),
    Input("current-data", "n_clicks"),
    Input('selected-rows-store', 'data'),
    prevent_initial_call=True,
)
def download_current_data(n_clicks, selected_rows):
    if n_clicks is None or n_clicks == 0:
        return None  # No download
    if n_clicks == 1:
        print(n_clicks, "noo")
        if selected_rows:
            current_selected_row = selected_rows[0]['id']
            response = requests.get(f'http://127.0.0.1:8000/device/{current_selected_row}/latest')
            data = response.json()
            dataPd = pd.DataFrame(data)
            n_clicks = 0
            print(n_clicks, "ues")
            return dcc.send_data_frame(dataPd.to_csv, "selected_data.csv")
    else:
        return None
        
@callback(
    Output("download-history-data", "data"),
    Input("history-data", "n_clicks"),
    Input('selected-rows-store', 'data'),
    prevent_initial_call=True,
)
def download_history_data(n_clicks, selected_rows):
    if n_clicks:
        if selected_rows:
            current_selected_row = selected_rows[0]['id']
            response = requests.get(f'http://127.0.0.1:8000/device/{current_selected_row}')
            data = response.json()
            dataPd = pd.DataFrame(data)
            n_clicks = 0
            return dcc.send_data_frame(dataPd.to_csv, "history_data.csv")
    else:
        return None

# Callback to update the AgGrid table with filtered data from the backend
@callback(
    Output('device-table', 'rowData'),
    Input('interval', 'n_intervals')
)
def update_device_table(n_intervals):
    response = requests.get('http://127.0.0.1:8000/panel/0/latest/')
    data = response.json()
    
    # selected_columns = ['id', 'datetime', 'device_type', 'units_of_measure1', 'converted_value1', 'units_of_measure2', 'converted_value2', 'units_of_measure3', 'converted_value3']
    filtered_data = [{key: entry[key] for key in selected_columns} for entry in data]
    
    return filtered_data

@callback(
    Output('data-table', 'columns'),
    Output('data-table', 'data'),
    Input('device-table', 'selectedRows'),
    prevent_initial_call=True,
)
def update_data_table(selectedRows):
    if selectedRows:   
        current_selected_row = selectedRows[0]['id']
        response = requests.get(f'http://127.0.0.1:8000/device/{current_selected_row}/latest')
        # Fetch data from the JSON API
        # response = requests.get('http://127.0.0.1:8000/device/0_0_110_101_0/latest')
        data = response.json()

        if not data:
            return [], []  # No data available

        # Transpose the data to swap rows and columns
        transposed_data = [{'Header': key, 'Data': value} for key, value in data[0].items()]

        return [{'name': 'Header', 'id': 'Header'}, {'name': 'Data', 'id': 'Data'}], transposed_data
    else:
        return [], []