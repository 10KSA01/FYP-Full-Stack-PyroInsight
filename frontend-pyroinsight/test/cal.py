# from dash import Dash, Input, Output, dcc, html
# import dash_bootstrap_components as dbc
# import calendar
# from datetime import datetime

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = dbc.Container(
#     [
#         dbc.Row(
#             dbc.Col(
#                 dbc.Card(
#                     dbc.CardBody(
#                         [
#                             html.H4("Calendar"),
#                             dcc.DatePickerSingle(
#                                 id="calendar",
#                                 date=datetime.today().date(),
#                                 display_format="YYYY-MM-DD",
#                             ),
#                             html.Div(id="selected-date"),
#                         ]
#                     )
#                 )
#             )
#         )
#     ],
#     className="mt-4",
# )

# @app.callback(
#     Output("selected-date", "children"),
#     [Input("calendar", "date")]
# )
# def update_selected_date(selected_date):
#     if selected_date is not None:
#         year, month, day = map(int, selected_date.split("-"))
#         day_name = calendar.day_name[calendar.weekday(year, month, day)]
#         return f"Selected Date: {month}/{day}/{year} ({day_name})"
#     else:
#         return ""

# if __name__ == "__main__":
#     app.run_server(debug=True, port=8060)

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import calendar
from datetime import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H4("Calendar"),
                        dcc.DatePickerSingle(
                            id="calendar",
                            date=datetime.today().date(),
                            display_format="YYYY-MM-DD",
                        ),
                        html.Div(id="selected-date"),
                    ],
                    className="calendar-container",
                )
            )
        )
    ],
    className="mt-4",
)

@app.callback(
    Output("selected-date", "children"),
    Input("calendar", "date")
)
def update_selected_date(selected_date):
    if selected_date is not None:
        year, month, day = map(int, selected_date.split("-"))
        day_name = calendar.day_name[calendar.weekday(year, month, day)]
        return f"Selected Date: {month}/{day}/{year} ({day_name})"
    else:
        return ""

if __name__ == "__main__":
    app.run_server(debug=True, port=8060)
