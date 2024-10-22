import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_bootstrap_components as dbc


def gen_dropdown(name, topic, rating):
    dropdown = html.Div(
        [
            dbc.RadioItems(
                id={"type": "selection-radio-item", "name": name, "topic": topic},
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {
                        "label": f"{i+1}",
                        "value": i,
                    }
                    for i in range(5)
                ],
                value=rating,
            ),
            dbc.Tooltip(
                "Rating from 1 to 5",
                target={"type": "selection-radio-item", "name": name, "topic": topic},
            ),
        ],
        className="radio-group",
    )
    return dropdown


sidebar = html.Div(
    [
        html.Div(
            [
                html.H1(
                    f"The Sorting Hat",
                ),
                html.H1(
                    className="fa-solid fa-hat-wizard",
                ),
            ],
            className="infoBox",
        ),
        html.Hr(),
        html.Div(
            [
                html.Span(
                    [
                        dbc.Button(
                            "Help!",
                            id="help-button",
                            size="sm",
                            color="primary",
                            outline=True,
                        ),
                        dbc.Popover(
                            html.Div(
                                [
                                    html.P(
                                        f"Start by adding users and topics with a specific number of seats.",
                                    ),
                                    html.P(
                                        f"Then ask the students to rate each topic on a scale from 1 to 5.",
                                    ),
                                    html.P(
                                        f"Finally, click 'Solve' and the tool will find a proper solution.",
                                    ),
                                    html.P(
                                        f"Play with the budget size if you think the solution is not optimal.",
                                    ),
                                    html.P(
                                        f"You can fix a solution for a student by clicking the solution on the right and then re-run the solver.",
                                    ),
                                    html.P(
                                        f"You can delete students or topics by clicking on their name.",
                                    ),
                                ],
                                className="infoBox",
                                id="help-info",
                            ),
                            target="help-button",
                            trigger="focus",
                            hide_arrow=True,
                            body=True,
                            offset="250,-60",
                        ),
                    ]
                ),
                html.Span(
                    [
                        dbc.Label(className="fa fa-moon", html_for="switch"),
                        dbc.Switch(
                            id="switch",
                            value=True,
                            className="d-inline-block ms-1",
                            persistence=True,
                        ),
                        dbc.Label(className="fa fa-sun", html_for="switch"),
                    ],
                    style={"float": "right", "padding-top": "2px"},
                ),
            ]
        ),
    ],
    className="sidebar",
    id="page-sidebar",
)

content = html.Div(
    [
        dcc.Store(id="student-storage-main", storage_type="session"),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="text",
                                            placeholder="Username",
                                            id="username-input",
                                        ),
                                        dbc.Tooltip(
                                            "Name of the student/ user.",
                                            target="username-input",
                                            placement="bottom",
                                        ),
                                    ]
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
                    style={"display": "inline-block"},
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="text",
                                            placeholder="Topic",
                                            id="topic-input",
                                        ),
                                        dbc.Tooltip(
                                            "Name of the topic.",
                                            target="topic-input",
                                            placement="bottom",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=0,
                                            step=1,
                                            value=1,
                                            id="topic-students-input",
                                        ),
                                        dbc.Tooltip(
                                            "Number of seats available for the topic.",
                                            target="topic-students-input",
                                            placement="bottom",
                                        ),
                                    ]
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
                    style={"display": "inline-block"},
                ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Input(
                                            type="number",
                                            min=1,
                                            step=1,
                                            value=1000,
                                            id="budget-size-input",
                                        ),
                                        dbc.Tooltip(
                                            "Set the budget size for the optimization. Higher value provides more accurate results, but takes longer to compute",
                                            target="budget-size-input",
                                            placement="bottom",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            [
                                                dbc.Spinner(
                                                    html.Div(
                                                        "Solve!", id="loading-state"
                                                    ),
                                                    type="grow",
                                                    size="sm",
                                                    id="loading-output",
                                                ),
                                            ],
                                            id="solve-button",
                                        ),
                                        dbc.Tooltip(
                                            "Run the optimization.",
                                            target="solve-button",
                                            placement="bottom",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                    style={"display": "inline-block"},
                ),
                html.Div(
                    id="result-info-target",
                    style={"display": "inline-block", "padding-left": "30px"},
                ),
            ],
            style={"padding": "15px", "padding-bottom": "40px", "padding-top": "40px"},
        ),
        html.Div(
            [],
            id="table-output",
            style={"padding": "15px"},
        ),
    ],
    className="content",
)
