"""EDA for Research Question 2: cost, financial aid (Pell share) and selectivity vs completion."""

import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

from data_loader import load_raw, load_scorecard, SEL_ORDER

VARS = ['C150_4', 'net_price', 'PCTPELL', 'ADM_RATE']
OUT_DIR = 'figures'


def missing_report(df, cols):
    """Records count and percent missing for given columns."""
    return pd.DataFrame({'missing': df[cols].isna().sum(),
                         'pct_missing': (df[cols].isna().mean() * 100)
                         .round(1)})


def levene_by_group(df, col, group):
    """This uses Levene's statistical test for equal variances of columns across groups."""
    groups = [g[col].dropna() for _, g in df.groupby(group)]
    return stats.levene(*groups)


def group_normality(df, col, group, seed=0):
    """Tests Shapiro-Wilk p-value test per group, using a sample size of 500)."""
    out = {}
    for name, g in df.groupby(group):
        x = g[col].dropna()
        if len(x) >= 3:
            x = x.sample(min(len(x), 500), random_state=seed)
            out[name] = stats.shapiro(x).pvalue
    return out


def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, name), dpi=200)
    plt.close()


def plot_box(df):
    d = df[df['selectivity'] != 'Open/unknown']
    sns.boxplot(data=d, x='selectivity', y='C150_4',
                order=SEL_ORDER[:4], color='lightsteelblue')
    plt.title('Completion rate by admission-rate group')
    plt.xlabel('Admission rate group')
    plt.ylabel('Completion rate (C150_4)')
    save('fig1_box_selectivity.png')


def plot_scatter(df):
    sns.scatterplot(data=df, x='PCTPELL', y='C150_4', hue='type',
                    alpha=0.5, s=18)
    sns.regplot(data=df, x='PCTPELL', y='C150_4', scatter=False,
                color='black', label='Linear fit')
    plt.title('Pell share vs completion rate')
    plt.xlabel('Share of students receiving Pell (PCTPELL)')
    plt.ylabel('Completion rate (C150_4)')
    plt.legend(title='Institution type')
    save('fig2_scatter_pell.png')


def plot_pell_bar(df):
    sns.barplot(data=df, x='selectivity', y='PCTPELL', order=SEL_ORDER,
                color='darkseagreen', errorbar='ci')
    plt.title('Mean Pell share by admission-rate group')
    plt.xlabel('Admission rate group')
    plt.ylabel('Mean Pell share')
    save('fig3_bar_pell_selectivity.png')


def plot_hist(df):
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    ax[0].hist(df['C150_4'].dropna(), bins=30, color='steelblue')
    ax[0].set_title('Completion rate')
    ax[0].set_xlabel('C150_4')
    ax[0].set_ylabel('Institutions')
    ax[1].hist(df['net_price'].dropna(), bins=30, color='indianred')
    ax[1].set_title('Average net price')
    ax[1].set_xlabel('Net price (USD)')
    save('fig4_hist_completion_price.png')


def plot_qq(df):
    fig, ax = plt.subplots(1, 4, figsize=(12, 3.2))
    for a, s in zip(ax, SEL_ORDER[:4]):
        x = df.loc[df['selectivity'] == s, 'C150_4'].dropna()
        stats.probplot(x, plot=a)
        a.set_title(s)
    save('fig5_qq_by_selectivity.png')


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        'Most-Recent-Cohorts-Institution-2.csv'
    os.makedirs(OUT_DIR, exist_ok=True)
    raw = load_raw(path)
    print('RAW shape:', raw.shape)
    df = load_scorecard(path)
    print('4-year (PREDDEG==3) shape:', df.shape)
    print('\nMissing (4-year):')
    print(missing_report(df, VARS + ['MD_FAMINC']))
    print('\nDescribe:')
    print(df[VARS].describe().round(3).T)
    print('\nType counts:')
    print(df['type'].value_counts(dropna=False))
    print('\nSelectivity counts:')
    print(df['selectivity'].value_counts().reindex(SEL_ORDER))
    clean = df.dropna(subset=['C150_4'])
    print('\nRows with C150_4:', len(clean))
    print('\nMean by selectivity:')
    print(clean.groupby('selectivity')[['C150_4', 'PCTPELL', 'net_price']]
          .agg(['mean', 'count']).reindex(SEL_ORDER).round(3))
    print('\nLevene:', levene_by_group(clean, 'C150_4', 'selectivity'))
    print('Shapiro p:', group_normality(clean, 'C150_4', 'selectivity'))
    pr = clean.dropna(subset=['PCTPELL'])
    print('Pearson PCTPELL~C150_4:', stats.pearsonr(pr['PCTPELL'],
                                                   pr['C150_4']))
    print('Spearman PCTPELL~C150_4:', stats.spearmanr(pr['PCTPELL'],
                                                     pr['C150_4']))
    plot_box(clean)
    plot_scatter(clean)
    plot_pell_bar(df)
    plot_hist(df)
    plot_qq(clean)


if __name__ == '__main__':
    main()
