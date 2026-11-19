"""This serves to load and clean the College Scorecard data for the
Research Question 2 EDA."""

import pandas as pd

COLS = ['UNITID', 'INSTNM', 'STABBR', 'CONTROL', 'PREDDEG', 'ADM_RATE',
        'PCTPELL', 'NPT4_PUB', 'NPT4_PRIV', 'C150_4', 'MD_FAMINC', 'UGDS',
        'UGDS_WHITE', 'UGDS_BLACK', 'UGDS_HISP', 'UGDS_ASIAN']

TYPE_LABELS = {1: 'Public', 2: 'Private nonprofit', 3: 'Private for-profit'}
SEL_LABELS = ['<25%', '25-50%', '50-75%', '>75%']
SEL_UNKNOWN = 'Open/unknown'
SEL_ORDER = SEL_LABELS + [SEL_UNKNOWN]


def load_raw(path):
    """Reads only needed columns, and PrivacySuppressed/NULL become NaN."""
    return pd.read_csv(path, usecols=COLS, low_memory=False,
                       na_values=['PrivacySuppressed', 'NULL'])


def add_net_price(df):
    """This combines public and private net price into one column."""
    df = df.copy()
    df['net_price'] = df['NPT4_PUB'].fillna(df['NPT4_PRIV'])
    return df


def add_type(df):
    """Map CONTROL helps provide readable institution types."""
    df = df.copy()
    df['type'] = df['CONTROL'].map(TYPE_LABELS)
    return df


def add_selectivity(df):
    """Bin ADM_RATE, accounts for missing admission rates to form
    their own group."""
    df = df.copy()
    binned = pd.cut(df['ADM_RATE'], [-0.001, 0.25, 0.5, 0.75, 1.0],
                    labels=SEL_LABELS).astype(object)
    df['selectivity'] = binned.where(df['ADM_RATE'].notna(), SEL_UNKNOWN)
    return df


def load_scorecard(path, four_year_only=True):
    """Loads raw data, and optionally keep bachelor's-predominant
    schools."""
    df = load_raw(path)
    if four_year_only:
        df = df[df['PREDDEG'] == 3]
    df = add_net_price(add_type(df))
    return add_selectivity(df).reset_index(drop=True)
