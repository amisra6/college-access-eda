# Impact of Socioeconomic Background on Higher Education Access and Academic Success

Authors: Anika Misra, Name 2, Name 3

## Project Overview
Higher education can open doors to academic and career goals, but students don't all have equal access to those opportunities. Factors like household income, socioeconomic background, and race or ethnicity can shape who enrolls in college and who succeeds once there. This project explores how those factors relate to college access and outcomes in the United States, with the goal of highlighting potential barriers and where more support may be needed.

We investigate three research questions:

1. **Household income and outcomes:** How does household income relate to students' academic performance and graduation rates at U.S. colleges and universities?
2. **Cost, aid, and selectivity:** How do factors tied to socioeconomic status, such as university cost, financial aid availability (Pell share), and institutional selectivity, relate to access to educational opportunities and academic success?
3. **Race, ethnicity, and enrollment:** How does enrollment across racial and ethnic groups vary by institutional selectivity and type, and how do these patterns compare to national trends in university attendance?

Our analysis uses the U.S. Department of Education's College Scorecard institution-level data....**add other sources here

## Data
Download the College Scorecard "Most Recent Institution-Level Data" CSV from https://collegescorecard.ed.gov/data/ and place it in the project folder as `Most-Recent-Cohorts-Institution-2.csv`.
(The file is about 100 MB, so it is not included in this repo.)
**add other data file sources

## How to Run
Run the EDA, which prints results and saves figures to `figures/`:

    python eda.py Most-Recent-Cohorts-Institution-2.csv

Run the tests:

    python test_eda.py

## Files
- `data_loader.py`: loads and cleans the Scorecard data
- `eda.py`: exploratory data analysis, statistical checks and figures
- `test_eda.py`: tests for the loading and analysis code
- ***Team members add other code files once complete
