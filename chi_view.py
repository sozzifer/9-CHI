from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from chi_model import chi_happy, create_blank_fig

# Specify HTML <head> elements
app = Dash(__name__,
           title="Association of categorical variables",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

# Specify app layout (HTML <body> elements) using dash.html, dash.dcc and dash_bootstrap_components
# All component IDs should relate to the Input or Output of callback functions in *_controller.py
app.layout = dbc.Container([
    # Row - User Input, Results and Conclusion
    dbc.Row([
        dbc.Col([
            html.H4("Variables"),
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
        ], xs=12, sm=6, md=3),
        dbc.Col([
            html.Div([
                html.H4("Results"),
                html.P([
                    html.Span("P value: ", className="bold-p"),
                    html.Span(id="p-value"),
                    dcc.Store(id="p-store")
                ], **{"aria-live": "polite"}),
                html.Br(),
                html.P("Null hypothesis", className="bold-p"),
                html.P(id="null-hyp", **{"aria-live": "polite"}),
                html.Br(),
                html.P("Alternative hypothesis", className="bold-p"),
                html.P(id="alt-hyp", **{"aria-live": "polite"})
            ], id="results", style={"display": "none"})
        ], xs=12, md=5),
        dbc.Col([
            html.H4("Conclusion"),
            dbc.Label("Based on the results obtained, should you accept or reject the null hypothesis at the 95% confidence level?",
                      className="label",
                      html_for="accept-reject95"),
            dbc.Select(id="accept-reject95",
                       options=[{"label": "Accept the null hypothesis",
                                 "value": "accept"},
                                {"label": "Reject the null hypothesis",
                                 "value": "reject"}],
                       value=None,
                       disabled=True),
            html.Br(),
            html.P(id="conclusion95", children=[], **{"aria-live": "polite"}),
            html.Br(),
            dbc.Label("What about at the 99% confidence level?",
                      className="label",
                      html_for="accept-reject99"),
            dbc.Select(id="accept-reject99",
                       options=[{"label": "Accept the null hypothesis",
                                 "value": "accept"},
                                {"label": "Reject the null hypothesis",
                                 "value": "reject"}],
                       value=None,
                       disabled=True),
            html.Br(),
            html.P(id="conclusion99", children=[], **{"aria-live": "polite"})
        ], xs=12, sm=6, md=4)
    ]),
    # Row - Graph and DataTables
    dbc.Row([
        dbc.Col([
            # Graph components are placed inside a Div with role="img" to manage UX for screen reader users
            html.Div([
                dcc.Graph(id="graph",
                          figure=create_blank_fig(),
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", **{"aria-hidden": "true"}),
            html.Br(),
            # A second Div is used to associate alt text with the relevant Graph component to manage the experience for screen reader users, styled using CSS class sr-only
            html.Div(id="sr-bar",
                     children=["Bar chart of dependent variable UK citizen for independent variable Sex"],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6),
        dbc.Col([
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
        ], style={"padding-left": 30}, xs=12, md=6)
    ])
], fluid=True)
