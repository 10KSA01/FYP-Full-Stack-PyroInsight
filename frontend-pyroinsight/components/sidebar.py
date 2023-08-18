from dash import html
import dash_bootstrap_components as dbc
import dash


descriptions = ["Main Dashboard", "Device Dashboard", "Profile", "Logout"]
sidebar_buttons = dbc.ButtonGroup(
    [
        dbc.Button(class_name="mw-1 bi bi-house-fill", id="main", size="lg", href='/'),
        dbc.Button(class_name="bi bi-motherboard-fill", id="devices", size="lg", href='/analytics'),
        dbc.Button(class_name="bi bi-person-lines-fill", id="profile", size="lg"),
        dbc.Button(class_name="bi bi-box-arrow-right", id="logout", size="lg"),
        
        dbc.Tooltip("Main Dashboard", target="main", placement="right"),
        dbc.Tooltip("Devices", target="devices", placement="right"),
        dbc.Tooltip("Profile", target="profile", placement="right"),
        dbc.Tooltip("Logout", target="logout", placement="right"),
    ],
    vertical=True,
)
def get_sidebar():
    return html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        
                        dbc.CardImg(src="./assets/logo.png", style={"maxHeight": "150px", "width": "auto", "height": "auto"}, class_name="mx-auto"),
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Row(sidebar_buttons),
                ]   
            )
        )
    )
