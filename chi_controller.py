from dash import html, Input, Output, State, exceptions, no_update, dash_table
import plotly.graph_objects as go
import pandas as pd
from chi_view import app
from chi_model import calc_chi2_ind, stat_colours


@app.callback(
    Output("graph", "figure"),
    Output("sr-bar", "children"),
    Output("p-value", "children"),
    Output("p-store", "data"),
    Output("dependent", "invalid"),
    Input("submit", "n_clicks"),
    State("dependent", "value"),
    State("independent", "value"),
    prevent_initial_call=True
)
def update_bar(n_clicks, dependent, independent):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        if dependent == independent:
            return no_update, no_update, no_update, no_update, True
        else:
            _, _, ct_t, _, _, _, _, p, _, _ = calc_chi2_ind(
                dependent, independent)
            data = []
            for x in ct_t.columns:
                data.append(go.Bar(name=str(x),
                                   x=ct_t.index,
                                   y=ct_t[x],
                                   marker_color=stat_colours[str(x)],
                                   marker_opacity=0.7,
                                   hovertemplate="Proportion: %{y:.2%}<extra></extra>"))
            fig = go.Figure(data)
            fig.update_layout(barmode="stack",
                              margin=dict(t=20, b=10, l=20, r=20),
                              height=400,
                              font_size=14,
                              dragmode=False,
                              legend_title_text=dependent,
                              legend_title_font_size=14,
                              xaxis_type="category")
            fig.update_xaxes(tick0=ct_t.index[0],
                             dtick=1,
                             title_text=independent)
            fig.update_yaxes(title_text=f"Proportion ({dependent})",
                             range=[0,1])
            sr_text = f"Bar chart of dependent variable {dependent} for independent variable {independent}"
        return fig, sr_text, f"{p:.3f}", p, False


@app.callback(
    Output("null-hyp", "children"),
    Output("alt-hyp", "children"),
    Output("accept-reject95", "value"),
    Output("accept-reject99", "value"),
    Output("accept-reject95", "disabled"),
    Output("accept-reject99", "disabled"),
    Input("submit", "n_clicks"),
    State("dependent", "value"),
    State("independent", "value"),
    prevent_initial_call=True
)
def update_results(n_clicks, dependent, independent):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        if dependent == independent:
            return no_update, no_update, no_update, no_update, True, True
        else:
            null_hyp = f"The value of {dependent} does not depend on {independent} - there is no association between the variables"
            alt_hyp = f"The value of {dependent} does depend on {independent} - there is an association between the variables"
            return null_hyp, alt_hyp, None, None, False, False


@app.callback(
    Output("table-observed", "children"),
    Output("table-expected", "children"),
    Output("table-observed-pc", "children"),
    Input("submit", "n_clicks"),
    State("dependent", "value"),
    State("independent", "value")
)
def update_datatables(n_clicks, dependent, independent):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        if dependent == independent:
            return no_update, no_update, no_update
        else:
            ct, ct_norm, _, ct_table, _, _, _, _, _, expected = calc_chi2_ind(
                dependent, independent)

            obs_df = ct.iloc[:-1, :].copy()
            obs_df.rename(columns={"Expected": "Total"},
                        inplace=True)
            obs_df.sort_index(ascending=False, inplace=True)

            exp_df = pd.DataFrame(data=expected,
                                  index=ct_table.columns,
                                  columns=ct_table.index).round(2).iloc[:-1, :]
            exp_df.rename(columns={"Expected": "Total"},
                          inplace=True)
            exp_df.sort_index(ascending=False, inplace=True)

            obs_pc_df = ct_norm
            obs_pc_df.rename(columns={"UK": "UK (obs)",
                                      "EU": "EU (obs)",
                                      "International": "Int'l (obs)",
                                      "Y": "Y (obs)",
                                      "N": "N (obs)",
                                      "F": "F (obs)",
                                      "M": "M (obs)",
                                      "Extrovert": "Extrovert (obs)",
                                      "Introvert": "Introvert (obs)",
                                      "Expected": "Expected"},
                             inplace=True)
            obs_pc_df.sort_index(ascending=False, inplace=True)

            formatted = {'locale': {},
                        'nully': '',
                        'prefix': None,
                        'specifier': '.2%'}

            table_obs = dash_table.DataTable(data=obs_df.to_dict("records"),
                                             columns=[{"name": i,
                                                       "id": i}
                                                      for i in obs_df.columns],
                                             style_header={"fontWeight": "bold"},
                                             style_table={"width": "70%"},
                                             style_cell={"minWidth": "120px",
                                                         "width": "120px",
                                                         "maxWidth": "120px",
                                                         "font-family": "Regular"},
                                             fill_width=False,
                                             cell_selectable=False)
            table_exp = dash_table.DataTable(data=exp_df.to_dict("records"),
                                             columns=[{"name": i,
                                                       "id": i}
                                                      for i in exp_df.columns],
                                             style_header={
                                                "fontWeight": "bold"},
                                             style_table={"width": "70%"},
                                             style_cell={"minWidth": "120px",
                                                         "width": "120px",
                                                         "maxWidth": "120px",
                                                         "font-family": "Regular"},
                                            fill_width=False,
                                            cell_selectable=False)
            table_obs_pc = dash_table.DataTable(data=obs_pc_df.to_dict("records"),
                                                columns=[{"name": i,
                                                        "id": i,
                                                        "type": "numeric",
                                                        "format": formatted}
                                                        for i in obs_pc_df.columns],
                                                style_header={"fontWeight": "bold"},
                                                style_table={"width": "70%"},
                                                style_cell={"minWidth": "120px",
                                                            "width": "120px",
                                                            "maxWidth": "120px",
                                                            "font-family": "Regular"},
                                                fill_width=False,
                                                cell_selectable=False)
            return table_obs, table_exp, table_obs_pc


@app.callback(
    Output("conclusion95", "children"),
    Input("accept-reject95", "value"),
    State("p-store", "data"),
    prevent_initial_call=True
)
def accept_or_reject95(accept_reject, p):
    if accept_reject is None:
        return ""
    else:
        if accept_reject == "reject":
            if p < 0.05:
                conclusion = [html.Span("Correct", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is less than 0.05, so we reject the null hypothesis at the 95% confidence level"])]
            else:
                conclusion = [html.Span("Incorrect", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is greater than 0.05, so we accept the null hypothesis at the 95% confidence level"])]
        elif accept_reject == "accept":
            if p < 0.05:
                conclusion = [html.Span("Incorrect", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is less than 0.05, so we reject the null hypothesis at the 95% confidence level"])]
            else:
                conclusion = [html.Span("Correct", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is greater than 0.05, so we accept the null hypothesis at the 95% confidence level"])]
        return conclusion


@app.callback(
    Output("conclusion99", "children"),
    Input("accept-reject99", "value"),
    State("p-store", "data"),
    prevent_initial_call=True
)
def accept_or_reject99(accept_reject, p):
    if accept_reject is None:
        return ""
    else:
        if accept_reject == "reject":
            if p < 0.01:
                conclusion = [html.Span("Correct", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is less than 0.01, so we reject the null hypothesis at the 99% confidence level"])]
            else:
                conclusion = [html.Span("Incorrect", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is greater than 0.01, so we accept the null hypothesis at the 99% confidence level"])]
        elif accept_reject == "accept":
            if p < 0.01:
                conclusion = [html.Span("Incorrect", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is less than 0.01, so we reject the null hypothesis at the 99% confidence level"])]
            else:
                conclusion = [html.Span("Correct", className="bold-p"),
                              html.Span(children=[
                                        f" - {p:.3f} is greater than 0.01, so we accept the null hypothesis at the 99% confidence level"])]
        return conclusion


if __name__ == "__main__":
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
    app.run(debug=True)
