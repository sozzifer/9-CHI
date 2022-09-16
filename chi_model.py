import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stat

# Generate dataframe from csv
chi_happy = pd.read_csv("data/chi_happy.csv")

# Colour palette
stat_colours = {
    "UK": "#d10373",
    "EU": "#9eab05",
    "International": "#0085a1",
    "Y": "#d10373",
    "N": "#9eab05",
    "F": "#9eab05",
    "M": "#d10373",
    "Extrovert": "#d10373",
    "Introvert": "#9eab05"
}

# Filter dataframe, perform Chi-squared test and return data for graph and DataTables
def calc_chi2_ind(y, x):
    dff = chi_happy[[y, x]].dropna().reset_index(drop=True)
    # ct: data for Observed Values DataTable
    ct = pd.crosstab(index=dff[y],
                     columns=dff[x],
                     margins=True,
                     margins_name="Expected")
    # ct: data for Observed Values (percentages) DataTable
    ct_norm = pd.crosstab(index=dff[y],
                          columns=dff[x],
                          normalize="columns",
                          margins=True,
                          margins_name="Expected")
    # ct_t: data for bar chart
    ct_t = pd.crosstab(index=dff[y],
                       columns=dff[x],
                       normalize="columns",
                       margins=True,
                       margins_name="Expected").transpose()
    # ct_table: data for Expected Values DataTable
    ct_table = pd.crosstab(index=dff[y],
                           columns=dff[x],
                           margins=True,
                           margins_name="Expected").transpose()
    dep_cat = dff[y].unique()
    ind_cat = dff[x].unique()
    chi2, p, dof, expected = stat.chi2_contingency(ct, correction=True)
    return ct, ct_norm, ct_t, ct_table, dep_cat, ind_cat, chi2, p, dof, expected


def create_blank_fig():
    ct = pd.crosstab(index=chi_happy["Sex"],
                     columns=chi_happy["UK_citizen"],
                     normalize="columns",
                     margins=True,
                     margins_name="Expected").transpose()
    data = []
    for x in ct.columns:
        data.append(go.Bar(name=str(x),
                           x=ct.index,
                           y=ct[x],
                           marker_color=stat_colours[str(x)],
                           marker_opacity=0.7,
                           hovertemplate="Proportion: %{y:.2%}<extra></extra>"))
    blank_fig = go.Figure(data)
    blank_fig.update_layout(barmode="stack",
                            margin=dict(t=20, b=10, l=20, r=20),
                            height=400,
                            font_size=14,
                            dragmode=False,
                            legend_title_text="UK citizen",
                            legend_title_font_size=14,
                            xaxis_type="category")
    blank_fig.update_xaxes(tick0=ct.index[0],
                           dtick=1,
                           title_text="Sex")
    blank_fig.update_yaxes(title_text=f"Proportion (UK citizen)",
                           range=[0,1])
    return blank_fig

# ct, ct_norm, ct_t, ct_table, dep_cat, ind_cat, chi2, p, dof, expected = calc_chi2_ind(
#     "UK_citizen", "Sex")

# Goodness of fit
# expected = [20, 20, 20, 20, 20, 20]
# observed = [25, 17, 15, 23, 24, 16]
# chisq, p = stat.chisquare(observed, expected)
# print(f"Chi squared: {chisq}")
# print(f"P value: {p}")

# obs_mendel = [315, 108, 101, 32]
# ratios = [9, 3, 3, 1]
# exp_mendel = []
# print(len(ratios))
# for i in range(len(obs_mendel)):
#     exp_mendel.append(sum(obs_mendel)*(ratios[i]/sum(ratios)))
# print(exp_mendel)