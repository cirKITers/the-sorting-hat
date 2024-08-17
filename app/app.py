import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
from typing import Any, Dict, Optional
import dash
from dash import html, Input, State, Output, callback, ALL, clientside_callback
import dash_bootstrap_components as dbc
import copy
import nevergrad as ng


app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)


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
                            color="info",
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
                    style={"float": "right"},
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

app.layout = html.Div([sidebar, content])

clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)


@callback(
    Output("student-storage-main", "data", allow_duplicate=True),
    [
        Input("add-user-button", "n_clicks"),
    ],
    [
        State("username-input", "value"),
        State("student-storage-main", "data"),
    ],
    prevent_initial_call=True,
)
def on_add_user_button_clicked(
    add_user_button_n_clicks,
    username_input_value,
    storage_main_data,
):
    if username_input_value is None:
        return dash.no_update

    storage_main_data = storage_main_data or {}
    if "students" not in storage_main_data:
        storage_main_data["students"] = {}

    if username_input_value not in storage_main_data["students"]:
        storage_main_data["students"][username_input_value] = {
            "final": None,
            "locked": False,
        }

    return storage_main_data


@callback(
    Output("student-storage-main", "data", allow_duplicate=True),
    [
        Input("add-topic-button", "n_clicks"),
    ],
    [
        State("topic-input", "value"),
        State("topic-students-input", "value"),
        State("student-storage-main", "data"),
    ],
    prevent_initial_call=True,
)
def on_add_topic_button_clicked(
    add_topic_button_n_clicks,
    topic_input_value,
    topic_students_input_value,
    storage_main_data,
):
    if topic_input_value is None:
        return dash.no_update

    storage_main_data = storage_main_data or {}
    if "topics" not in storage_main_data:
        storage_main_data["topics"] = {}

    if topic_input_value not in storage_main_data["topics"]:
        storage_main_data["topics"][topic_input_value] = {
            "students": {},
            "seats": topic_students_input_value,
        }

    return storage_main_data


@callback(
    [Output("table-output", "children"), Output("student-storage-main", "data")],
    [
        Input("student-storage-main", "data"),
    ],
)
def update_table(
    storage_main_data,
):
    if storage_main_data is None:
        return dash.no_update

    if "topics" not in storage_main_data:
        storage_main_data["topics"] = {}
    if "students" not in storage_main_data:
        storage_main_data["students"] = {}

    for student_name, _ in sorted(storage_main_data["students"].items()):
        for _, table_properties in storage_main_data["topics"].items():
            if student_name not in table_properties["students"]:
                table_properties["students"][student_name] = 2

    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("Name"),
                    *[
                        html.Th(
                            [
                                dbc.Button(
                                    html.B(f"({topic['seats']}x) {topic_name}"),
                                    color="danger",
                                    outline=True,
                                    # size="sm",
                                    id={"type": "topic-rm-button", "topic": topic_name},
                                ),
                                dbc.Tooltip(
                                    "Delete this topic",
                                    target={
                                        "type": "topic-rm-button",
                                        "topic": topic_name,
                                    },
                                ),
                            ],
                            style={
                                "text-align": "center",
                                "vertical-align": "middle",
                            },
                        )
                        for topic_name, topic in sorted(
                            storage_main_data["topics"].items()
                        )
                    ],
                    html.Th(
                        "Solution",
                        style={
                            "text-align": "right",
                            "vertical-align": "right",
                        },
                    ),
                ]
            )
        )
    ]

    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(
                            [
                                dbc.Button(
                                    html.B(f"{student_name}"),
                                    color="danger",
                                    outline=True,
                                    # size="sm",
                                    id={"type": "name-rm-button", "name": student_name},
                                ),
                                dbc.Tooltip(
                                    "Delete this user",
                                    target={
                                        "type": "name-rm-button",
                                        "name": student_name,
                                    },
                                ),
                            ]
                        ),
                        *[
                            html.Td(
                                gen_dropdown(
                                    student_name,
                                    topic_name,
                                    (topic_properties["students"][student_name]),
                                ),
                                style={
                                    "text-align": "center",
                                    "vertical-align": "middle",
                                },
                            )
                            for topic_name, topic_properties in storage_main_data[
                                "topics"
                            ].items()
                        ],
                        html.Td(
                            [
                                (
                                    dbc.Button(
                                        html.B(student_properties["final"]),
                                        color="success",
                                        outline=True,
                                        # size="sm",
                                        id={
                                            "type": "accept-name-button",
                                            "name": student_name,
                                        },
                                    )
                                    if student_properties["final"]
                                    else dbc.Button(
                                        "Topic N/A",
                                        color="dark",
                                        outline=True,
                                        disabled=True,
                                        # size="sm",
                                        id={
                                            "type": "accept-name-button",
                                            "name": student_name,
                                        },
                                    )
                                ),
                                dbc.Tooltip(
                                    "Mark as accepted",
                                    target={
                                        "type": "accept-name-button",
                                        "name": student_name,
                                    },
                                ),
                            ],
                            style={
                                "text-align": "right",
                                "vertical-align": "right",
                            },
                        ),
                    ]
                )
                for student_name, student_properties in sorted(
                    storage_main_data["students"].items()
                )
            ]
        )
    ]
    table = dbc.Table(
        table_header + table_body,
        bordered=False,
        responsive=True,
        hover=True,
    )
    return [table, storage_main_data]


@callback(
    Output("student-storage-main", "data", allow_duplicate=True),
    [
        Input({"type": "selection-radio-item", "name": ALL, "topic": ALL}, "id"),
        Input({"type": "selection-radio-item", "name": ALL, "topic": ALL}, "value"),
    ],
    State("student-storage-main", "data"),
    prevent_initial_call=True,
)
def update_selection_callback(ids, values, storage_main_data):
    for id, value in zip(ids, values):
        storage_main_data["topics"][id["topic"]]["students"][id["name"]] = value

    return storage_main_data


@callback(
    Output("student-storage-main", "data", allow_duplicate=True),
    [
        Input({"type": "topic-rm-button", "topic": ALL}, "id"),
        Input({"type": "topic-rm-button", "topic": ALL}, "n_clicks"),
    ],
    State("student-storage-main", "data"),
    prevent_initial_call=True,
)
def delete_topic_callback(ids, n_clicks, storage_main_data):
    for id, n_click in zip(ids, n_clicks):
        if n_click is None:
            continue
        storage_main_data["topics"].pop(id["topic"])
    return storage_main_data


@callback(
    Output("student-storage-main", "data", allow_duplicate=True),
    [
        Input({"type": "name-rm-button", "name": ALL}, "id"),
        Input({"type": "name-rm-button", "name": ALL}, "n_clicks"),
    ],
    State("student-storage-main", "data"),
    prevent_initial_call=True,
)
def delete_name_callback(ids, n_clicks, storage_main_data):
    for id, n_click in zip(ids, n_clicks):
        if n_click is None:
            continue
        storage_main_data["students"].pop(id["name"])
        for topic in storage_main_data["topics"].keys():
            if id["name"] in storage_main_data["topics"][topic]["students"]:
                storage_main_data["topics"][topic]["students"].pop(id["name"])
    return storage_main_data


@callback(
    [
        Output("result-info-target", "children"),
        Output("loading-output", "children"),
        Output("student-storage-main", "data", allow_duplicate=True),
    ],
    Input("solve-button", "n_clicks"),
    State("budget-size-input", "value"),
    State("student-storage-main", "data"),
    prevent_initial_call=True,
)
def trigger_solver(_, budget_size, storage_main_data):
    if storage_main_data is None:
        return dash.no_update
    if "topics" not in storage_main_data:
        return dash.no_update
    if "students" not in storage_main_data:
        return dash.no_update

    def cost(solution):
        data = copy.deepcopy(storage_main_data)
        satisfaction = 0.0
        for student_index, student_name in enumerate(sorted(data["students"].keys())):
            topic_name = solution[student_index]
            rating = data["topics"][topic_name]["students"][student_name]

            data["topics"][topic_name]["seats"] -= 1

            if data["topics"][topic_name]["seats"] < 0:
                satisfaction -= len(storage_main_data["topics"]) ** 4

            satisfaction += 2**rating

        return -satisfaction

    optim = ng.optimizers.NGOpt(
        parametrization=ng.p.Choice(
            storage_main_data["topics"].keys(),
            repetitions=len(storage_main_data["students"]),
        ),
        budget=budget_size,
    )
    result = optim.minimize(cost)

    max_sat = 0
    for student_index, student_name in enumerate(
        sorted(storage_main_data["students"].keys())
    ):
        storage_main_data["students"][student_name]["final"] = result.value[
            student_index
        ]

        best_choice = 0
        for _, topic_properties in storage_main_data["topics"].items():
            if topic_properties["students"][student_name] > best_choice:
                best_choice = topic_properties["students"][student_name]
        max_sat += 2**best_choice

    sat = 100.0 * (-result.loss) / max_sat
    if sat < 60:
        color = "danger"
    elif sat < 80:
        color = "warning"
    else:
        color = "success"

    result_info = (
        html.H4(
            dbc.Badge(
                f"{sat:.2f}% Satisfaction",
                color=color,
                pill=True,
            )
        ),
    )
    return [result_info, "Solve!", storage_main_data]


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
