from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
import pandas as pd

def panel_status_line_graph():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Panel 1"),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                figure=px.line(
                                    df, x="sepal_width", y="sepal_length", color="species"
                                ).update_layout(
                                    # template="plotly_dark",
                                    plot_bgcolor="rgba(0, 0, 0, 0)",
                                    paper_bgcolor="rgba(0, 0, 0, 0)",
                                ),
                                config={"displayModeBar": True},
                            )
                        ]
                    )            
                ]
            ),
        ]
    )

def downsample_data(coordinates, max_points=100):
    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(coordinates)

    # Downsample the data by selecting a subset of max_points evenly spaced data points
    df_downsampled = df.iloc[::max(len(df) // max_points, 1)]

    # Convert the downsampled DataFrame back to a list of dictionaries
    downsampled_coordinates = df_downsampled.to_dict(orient='records')

    return downsampled_coordinates

def panel_measurement_line_graph(node, type):
    response = requests.get(f'http://127.0.0.1:8000/pannel/average/{type}/{node}/period/')
    measurement_data = response.json()
    measure_columns = {
        "smoke": ("Average Obscuration", "Obscuration (%/m)"),
        "heat": ("Average Temperature", "Temperature (°C)"),
        "co": ("Average Carbon Monoxide", "Carbon Monoxide (ppm)"),
        "dirtiness": ("Average Dirtiness", "Dirtiness")
    }
    downsampled_measurement_data = downsample_data(measurement_data)
    title, units = measure_columns[type]

    # Extract x and y values from the JSON data
    datetime = [point['datetime'] for point in downsampled_measurement_data]
    measurement = [point[type] for point in downsampled_measurement_data]
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader(f"Panel 1 - {title}"),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                figure = {
                                    'data': [
                                        {'x': datetime, 'y': measurement, 'mode': 'lines'}
                                    ],
                                    'layout': {
                                        'title': title,
                                        'xaxis': {'title': 'Date & Time'},
                                        'yaxis': {'title': units}
                                    }
                                }                                
                            )
                        ]
                    )            
                ]
            ),
        ]
    )
    
# Iris bar figure
def dfgraph():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Panel 1"),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                figure=px.bar(
                                    df, x="sepal_width", y="sepal_length", color="species"
                                ).update_layout(
                                    # template="plo",
                                    plot_bgcolor="rgba(0, 0, 0, 0)",
                                    paper_bgcolor="rgba(0, 0, 0, 0)",
                                ),
                                config={"displayModeBar": True},
                            )
                        ]
                    )            
                ]
            ),
        ]
    )


# Text field
def drawText():
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H2("Text"),
                            ],
                            style={"textAlign": "center"},
                        )
                    ]
                )
            ),
        ]
    )
    
# Data
df = px.data.iris()