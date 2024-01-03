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

def panel_obscuration_line_graph():
    response = requests.get('http://127.0.0.1:8000/average-obscuration-period/0/')
    obscuration_data = response.json()

    downsampled_obscuration_data = downsample_data(obscuration_data)
    # Extract x and y values from the JSON data
    datetime = [point['datetime'] for point in downsampled_obscuration_data]
    obscuration = [point['obscuration'] for point in downsampled_obscuration_data]
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Panel 1"),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                figure = {
                                    'data': [
                                        {'x': datetime, 'y': obscuration, 'mode': 'lines+markers', 'name': 'Line Plot'}
                                    ],
                                    'layout': {
                                        'title': 'Obscuration',
                                        'xaxis': {'title': 'Datetime'},
                                        'yaxis': {'title': 'Obscuration'}
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