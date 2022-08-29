from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from chi_model import chi_happy

app = Dash(__name__,
           title="Association of categorical variables",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Dependent variable (y axis)",
                          className="label",
                          html_for="dependent"),
                dbc.Select(id="dependent",
                           options=[{"label": x, "value": x}
                                     for x in chi_happy.columns[1:7]],
                           value="UK_citizen"),
                dbc.FormFeedback(
                    "Dependent variable must be different to independent variable",
                    type="invalid")
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Label("Independent variable (x axis)",
                          className="label",
                          html_for="independent"),
                dbc.Select(id="independent",
                           options=[{"label": x, "value": x}
                                     for x in chi_happy.columns[1:7]],
                           value="Sex")
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Button(id="submit",
                           n_clicks=0,
                           children="Update results",
                           class_name="button",
                           style={"width": 150})
            ], className="d-flex justify-content-center")
        ], xs=12, sm=6, md=3, lg=3, xl=3),
        dbc.Col([
            html.P([
                html.Span("P value: ", className="bold-p"),
                html.Span(id="p-value"),
                dcc.Store(id="p-store")
            ]),
            html.Br(),
            html.P("Null hypothesis", className="bold-p"),
            html.P(id="null-hyp"),
            html.Br(),
            html.P("Alternative hypothesis", className="bold-p"),
            html.P(id="alt-hyp"),
        ], xs=12, sm=12, md=5, lg=5, xl=5),
        dbc.Col([
            html.H4("Conclusion"),
            html.P(
                "Based on the results obtained, should you accept or reject the null hypothesis at the 95% confidence level?", className="bold-p"),
            dcc.Dropdown(id="accept-reject95",
                         options=[{"label": "Accept the null hypothesis",
                                   "value": "accept"},
                                  {"label": "Reject the null hypothesis",
                                   "value": "reject"}
                                  ],
                         value=None),
            html.Br(),
            html.P(id="conclusion95", children=[]),
            html.P(
                "What about at the 99% confidence level?", className="bold-p"),
            dcc.Dropdown(id="accept-reject99",
                         options=[{"label": "Accept the null hypothesis",
                                   "value": "accept"},
                                  {"label": "Reject the null hypothesis",
                                   "value": "reject"}
                                  ],
                         value=None),
            html.Br(),
            html.P(id="conclusion99", children=[])
        ], xs=12, sm=6, md=4, lg=4, xl=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img"),
            html.Br(),
            html.Div(id="sr-bar",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
            # html.H4("Results"),
            # html.P(children=[
            #     html.Span("Chi squared: ", className="bold-p"),
            #     html.Span(id="chi2")]),
            # html.Br(),
            html.Div([
                html.H5("Observed vs expected proportions"),
                html.Div(id="table-observed-pc", children=[]),
                html.Br(),
                html.H5("Observed values"),
                html.Div(id="table-observed", children=[]),
                html.Br(),
                html.H5("Expected values"),
                html.Div(id="table-expected", children=[]),
            ])
        ], style={"padding-left": 30}, xs=12, sm=12, md=6, lg=6, xl=6)
    ])
], fluid=True)
