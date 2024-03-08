from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
from components.sidebar import get_sidebar
from components.graphs import *

# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], use_pages=True)

app.title = 'PyroInsight'
app._favicon = ('logo.ico')

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
    app.run_server(debug=False, port=8075)
