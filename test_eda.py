"""Tests for data_loader and eda helpers using tiny hand-made data."""

import io
import os
import tempfile

import numpy as np
import pandas as pd

import data_loader as dl
import eda


def test_privacy_suppressed_is_nan():
    csv = io.StringIO('UNITID,C150_4\n1,PrivacySuppressed\n2,0.5\n')
    df = pd.read_csv(csv, na_values=['PrivacySuppressed', 'NULL'])
    assert np.isnan(df.loc[0, 'C150_4'])
    assert df.loc[1, 'C150_4'] == 0.5


def test_net_price_combines():
    df = pd.DataFrame({'NPT4_PUB': [100, np.nan, np.nan],
                       'NPT4_PRIV': [999, 200, np.nan]})
    out = dl.add_net_price(df)
    assert out['net_price'].iloc[0] == 100
    assert out['net_price'].iloc[1] == 200
    assert np.isnan(out['net_price'].iloc[2])


def test_type_labels():
    out = dl.add_type(pd.DataFrame({'CONTROL': [1, 2, 3]}))
    assert list(out['type']) == ['Public', 'Private nonprofit',
                                 'Private for-profit']


def test_selectivity_bins():
    df = pd.DataFrame({'ADM_RATE': [0.1, 0.25, 0.4, 0.6, 0.9, np.nan]})
    out = dl.add_selectivity(df)
    assert list(out['selectivity']) == ['<25%', '<25%', '25-50%',
                                        '50-75%', '>75%', 'Open/unknown']


def test_missing_report():
    df = pd.DataFrame({'a': [1, np.nan, 3, np.nan], 'b': [1, 2, 3, 4]})
    rep = eda.missing_report(df, ['a', 'b'])
    assert rep.loc['a', 'missing'] == 2
    assert rep.loc['a', 'pct_missing'] == 50.0
    assert rep.loc['b', 'missing'] == 0


def test_levene_detects_unequal_variance():
    rng = np.random.RandomState(0)
    df = pd.DataFrame({'y': np.r_[rng.normal(0, 1, 200),
                                  rng.normal(0, 10, 200)],
                       'g': ['a'] * 200 + ['b'] * 200})
    assert eda.levene_by_group(df, 'y', 'g').pvalue < 0.001


def test_loader_filters_four_year():
    row = {c: 1 for c in dl.COLS}
    rows = [dict(row, PREDDEG=3), dict(row, PREDDEG=2)]
    p = os.path.join(tempfile.mkdtemp(), 's.csv')
    pd.DataFrame(rows).to_csv(p, index=False)
    assert len(dl.load_scorecard(p)) == 1
    assert len(dl.load_scorecard(p, four_year_only=False)) == 2


def main():
    tests = [v for k, v in globals().items() if k.startswith('test_')]
    for t in tests:
        t()
    print('All', len(tests), 'tests passed')


if __name__ == '__main__':
    main()
