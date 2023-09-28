from dash import html
import dash_bootstrap_components as dbc

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

def get_statistic_card(text, value):
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
                            html.P(text, style={"margin": "0"}),
                            html.H4(value, style={"margin": "0"}),
                        ]
                    ), 
                    style={"maxHeight": 90}
                ),
            ],
        )
    )
