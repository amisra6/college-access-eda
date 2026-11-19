# Title of your project

Authors: Name 1, Name 2, Name 3

## Overview
One or two sentences on what the project analyzes (how completion rates relate to cost, Pell share and selectivity at 4-year colleges).

## Data
Download the College Scorecard "Most Recent Institution-Level Data" CSV from https://collegescorecard.ed.gov/data/ and place it in the project folder as `Most-Recent-Cohorts-Institution-2.csv`.
(The file is about 100 MB, so it is not included in this repo.)

## Requirements
Python 3 with pandas, numpy, matplotlib, seaborn and scipy:

    pip install pandas numpy matplotlib seaborn scipy

## How to run
Run the EDA, which prints results and saves figures to `figures/`:

    python eda.py Most-Recent-Cohorts-Institution-2.csv

Run the tests:

    python test_eda.py

## Files
- `data_loader.py`: loads and cleans the Scorecard data
- `eda.py`: exploratory data analysis, statistical checks and figures
- `test_eda.py`: tests for the loading and analysis code