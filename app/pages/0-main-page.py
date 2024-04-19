import dash
from dash import (
    Dash,
    dcc,
    html,
    Input,
    State,
    Output,
    callback,
)
import dash_bootstrap_components as dbc

dash.register_page(__name__, name="Home", path="/")

dropdown = html.Div(
    [
        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {
                    "label": f"{i}",
                    "value": i,
                }
                for i in range(5)
            ],
            value=2,
        ),
        html.Div(id="output"),
    ],
    className="radio-group",
)

layout = html.Div(
    [
        html.H1("This is our Home page"),
        html.Div("This is our Home page content."),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        type="text",
                                        placeholder="Username",
                                        id="username-input",
                                    )
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Add User",
                                        id="add-user-button",
                                    )
                                ),
                            ],
                        ),
                    ],
                    style={"height": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        type="text",
                                        placeholder="Topic",
                                        id="topic-input",
                                    )
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Add Topic",
                                        id="add-topic-button",
                                    )
                                ),
                            ],
                        ),
                    ],
                    style={"height": "49%", "display": "inline-block"},
                ),
            ],
            style={"padding": "15px"},
        ),
        html.Div(
            [],
            id="table-output",
        ),
    ]
)


@callback(
    Output("table-output", "children"),
    [
        Input("add-user-button", "n_clicks"),
        Input("add-topic-button", "n_clicks"),
    ],
    [
        State("username-input", "value"),
        State("topic-input", "value"),
    ],
    prevent_initial_call=True,
)
def on_preference_changed(
    add_user_button_n_clicks,
    add_topic_button_n_clicks,
    username_input_value,
    topic_input_value,
):

    table_header = [html.Thead(html.Tr([html.Th("Name"), html.Th("Topic")]))]
    row1 = html.Tr([html.Td("Arthur"), dropdown])
    row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
    row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
    row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

    table_body = [html.Tbody([row1, row2, row3, row4])]

    return dbc.Table(table_header + table_body, bordered=True)
