import pandas as pd
import scipy.stats as stat

chi_happy = pd.read_csv("data/chi_happy.csv")
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


def calc_chi2_ind(y, x):
    dff = chi_happy[[y, x]].dropna().reset_index(drop=True)
    ct = pd.crosstab(index=dff[y],
                     columns=dff[x],
                     margins=True,
                     margins_name="Expected")
    ct_norm = pd.crosstab(index=dff[y],
                          columns=dff[x],
                          normalize="columns",
                          margins=True,
                          margins_name="Expected")
    ct_t = pd.crosstab(index=dff[y],
                       columns=dff[x],
                       normalize="columns",
                       margins=True,
                       margins_name="Expected").transpose()
    ct_table = pd.crosstab(index=dff[y],
                           columns=dff[x],
                           margins=True,
                           margins_name="Expected").transpose()
    dep_cat = dff[y].unique()
    ind_cat = dff[x].unique()
    chi2, p, dof, expected = stat.chi2_contingency(ct, correction=True)
    return ct, ct_norm, ct_t, ct_table, dep_cat, ind_cat, chi2, p, dof, expected


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