from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from components.sidebar import get_sidebar

# def statistic_card():
#     return html.Div(
#         dbc.Card(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     html.I(className="bi bi-slash-circle col-md-4")
#                 ),
#                 dbc.Col(
#                     dbc.CardBody(
#                         [
#                             html.H4("Card title", className="card-title"),
#                             html.P(
#                                 "This is a wider card with supporting text "
#                                 "below as a natural lead-in to additional "
#                                 "content. This content is a bit longer.",
#                                 className="card-text",
#                             ),
#                             html.Small(
#                                 "Last updated 3 mins ago",
#                                 className="card-text text-muted",
#                             ),
#                         ]
#                     ),
#                     className="col-md-8",
#                 ),
#             ],
#             className="g-0 d-flex align-items-center",
#         )
#     ],
#     # className="mb-3",
#     # style={"maxWidth": "540px"},

#     )
#         )

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

def statistic_card():
    return html.Div(
        dbc.CardGroup(
            [
                dbc.Card(
                    html.Div(className="bi bi-slash-circle", style=card_icon),
                    className="bg-primary",
                    style={"maxWidth": 75},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P("Devices disabled this year"),
                            html.H3("10"),
                        ]
                    )
                ),
            ],
        )
    )


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

icons = ["bi bi-house-fill", "bi bi-motherboard-fill", "bi bi-person-lines-fill", "bi bi-box-arrow-right"]
descriptions = ["Main Dashboard", "Device Dashboard", "Profile", "Logout"]

# Data
df = px.data.iris()

# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

app.title = 'PyroInsight'
# app._favicon = ('logo.ico')
descriptions = ["Main Dashboard", "Device Dashboard", "Profile", "Logout"]
main = dbc.Card(
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
                    dbc.Col([panel_status_line_graph()], width=6),
                    dbc.Col([dfgraph()], width=6),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([statistic_card()], width=4),
                    dbc.Col([statistic_card()], width=4),
                    dbc.Col([statistic_card()], width=4),
                ],
                align="center",    
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([statistic_card()], width=4),
                    dbc.Col([statistic_card()], width=4),
                    dbc.Col([statistic_card()], width=4),
                ],
                align="center",    
            ),
            
        ]
    )
)

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(get_sidebar(), width=1),
                dbc.Col(main, width=11),
            ],
            class_name="g-0"
        ),
    ]
)

# Run app and display result inline in the notebook
if __name__ == "__main__":
    app.run_server(debug=True, port=8075)
