from dash import Dash, dcc, html
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from components.sidebar import get_sidebar
from components.statistic_card import get_statistic_card
from components.other import *

# To run the app:
# python -m uvicorn app:app --reload

icons = ["bi bi-house-fill", "bi bi-motherboard-fill", "bi bi-person-lines-fill", "bi bi-box-arrow-right"]
descriptions = ["Main Dashboard", "Device Dashboard", "Profile", "Logout"]


# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], use_pages=True)

app.title = 'PyroInsight'
# app._favicon = ('logo.ico')

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(get_sidebar(), style={"maxWidth": "5%"}),
                dbc.Col(dash.page_container, style={"maxWidth": "95%"}),
            ],
            class_name="g-0"
        ),
    ]
)

# Run app and display result inline in the notebook
if __name__ == "__main__":
    app.run_server(debug=True, port=8075)
