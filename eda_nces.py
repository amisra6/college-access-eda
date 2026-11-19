"""
EDA of NCES Table 10: Enrollment weighted average 6-year graduation
rates for racial/ethnic groups, by Carnegie classification, selectivity,
and size of low-income enrollment in the 1998 graduation rate cohort:
2004.

The raw Excel file's formatting messes with pandas, so this file cleans
it up, then summarizes and plots it.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATA_PATH = 'NCES_2007161_10_Estimates.xlsx'

# Cleaned-up column names, lists used to reference later on
RACE_COLS = ['White', 'Black', 'Hispanic', 'Asian', 'American Indian']
GAP_COLS = ['White-Black Gap', 'White-Hispanic Gap']
NUM_COLS = RACE_COLS + GAP_COLS

CARNEGIE = ['Doctoral', 'Master’s', 'Bachelor’s']
SELECTIVITY = ['Very selective', 'Moderately selective',
               'Minimally selective']
SIZES = ['Small', 'Moderate', 'Large', 'Small and moderate']


def clean_text(value):
    """
    Removes the Excel line-break codes and extra whitespace that appear
    in raw cells. Returns non-string values unchanged.
    """
    if not isinstance(value, str):
        return value
    for code in ['_x000D_', '_x000A_', '\n']:
        value = value.replace(code, '')
    return value.strip()


def to_number(value):
    """
    Converts a cell to a float. The '‡' symbol (reporting standards not
    met) and blank cells become NaN.
    """
    value = clean_text(value)
    # '‡' appears in the Excel file where NCES did not report a value
    if value is None or value == '‡' or value == '':
        return float('nan')
    return float(value)


def load_data(path):
    """
    Reads the raw table and returns a tidy DataFrame with one row per
    Carnegie classification / selectivity / low-income size group.
    Summary rows are dropped so that there is no duplicate group.
    """
    raw = pd.read_excel(path, header=None)
    rows = []
    carnegie = None
    selectivity = None
    for row_number, row in raw.iterrows():
        label = clean_text(row[0])
        if label in CARNEGIE:
            carnegie = label
        elif label in SELECTIVITY:
            selectivity = label
        elif label in SIZES and carnegie is not None:
            record = {
                'Carnegie': carnegie,
                'Selectivity': selectivity,
                'Low-Income Size': label,
            }
            for i, col in enumerate(NUM_COLS):
                record[col] = to_number(row[i + 1])
            rows.append(record)
    return pd.DataFrame(rows)


def describe_size(df):
    """
    Prints the number of rows and columns and the column types.
    """
    print('Rows:', df.shape[0], 'Columns:', df.shape[1])
    print(df.dtypes)


def missing_report(df):
    """
    Returns the count and percent of missing values per column.
    """
    counts = df.isna().sum()
    percent = (counts / len(df) * 100).round(1)
    return pd.DataFrame({'missing': counts, 'percent': percent})


def summarize(df):
    """
    Gives the seven-number summary of each graduation rate and gap
    column and the counts of each categorical column.
    """
    print(df[NUM_COLS].describe().round(2))
    for col in ['Carnegie', 'Selectivity', 'Low-Income Size']:
        print(df[col].value_counts())


def to_long(df):
    """
    Reshapes the race columns into long format with one row per group
    and race, so that seaborn can group them for plots.
    """
    id_cols = ['Carnegie', 'Selectivity', 'Low-Income Size']
    return df.melt(id_vars=id_cols, value_vars=RACE_COLS,
                   var_name='Race/Ethnicity',
                   value_name='Graduation Rate')


def plot_rates_by_selectivity(df):
    """
    Creates a grouped bar chart of mean graduation rate by selectivity,
    with one bar per racial/ethnic group.
    """
    long_df = to_long(df)
    sns.catplot(data=long_df, x='Selectivity', y='Graduation Rate',
                hue='Race/Ethnicity', kind='bar', errorbar=None,
                order=SELECTIVITY, height=5, aspect=1.6)
    plt.title('Six-Year Graduation Rate by Selectivity and Race/Ethnicity')
    plt.ylabel('Graduation Rate (%)')
    plt.savefig('rates_by_selectivity.png', bbox_inches='tight')
    plt.close()


def plot_gap_by_low_income(df):
    """
    Creates a box plot of the White-Black graduation gap for each size
    of low-income enrollment.
    """
    order = ['Small', 'Moderate', 'Large', 'Small and moderate']
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Low-Income Size', y='White-Black Gap',
                order=order)
    plt.axhline(0, color='gray', linewidth=1)
    plt.title('White-Black Graduation Gap by Size of Low-Income '
              'Enrollment')
    plt.ylabel('Gap (percentage points)')
    plt.savefig('gap_by_low_income.png', bbox_inches='tight')
    plt.close()


def main():
    df = load_data(DATA_PATH)
    describe_size(df)
    print(df.head())
    print(missing_report(df))
    print(df[df.isna().any(axis=1)])
    summarize(df)
    plot_rates_by_selectivity(df)
    plot_gap_by_low_income(df)


if __name__ == '__main__':
    main()
