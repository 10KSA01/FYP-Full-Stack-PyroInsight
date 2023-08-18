from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

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