from dash import html
import dash_bootstrap_components as dbc

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

def get_statistic_card():
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
