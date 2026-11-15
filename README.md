# Titanic Survival Analysis: Power BI Dashboard

An end-to-end data analytics project: problem statement, dataset profiling, cleaning, analysis, an interactive Power BI dashboard and business insights.

Built by **Derrick D. Agbenorto** as Task 4 of the **Swynex** data analytics internship.

![Dashboard](images/dashboard.png)

## The question

Which passenger characteristics were associated with survival on the Titanic, and how can those patterns be presented so that anyone can explore them?

## Headline results

| Measure | Value |
|---|---|
| Passengers analysed | 891 |
| Survivors | 342 (38.4%) |
| Women vs men survival | **74.2%** vs **18.9%** |
| 1st vs 3rd class survival | **63.0%** vs **24.2%** |
| Children (0-12) survival | 58.0% |
| Small families (2-4) vs large (5+) | 57.9% vs 16.1% |

Sex and class were the strongest dividing lines, and they compound: women in 1st class survived at 96.8%, men in 3rd class at 13.5%. The higher survival at Cherbourg is largely explained by its 1st-class share (50.6% against 20.0% at Southampton).

**Read the full write-up in [REPORT.md](REPORT.md).**

## What is in this repository

```
.
├── README.md                    This file
├── REPORT.md                    Full project report
├── requirements.txt             Python dependencies
├── data/
│   └── cleaned_titanic.csv      Cleaned dataset (891 rows, 12 columns)
├── scripts/
│   ├── clean_titanic.py         Reference cleaning script for the raw file
│   └── analysis.py              Reproduces every figure in the report
├── powerbi/
│   ├── Titanic.pbix             The Power BI dashboard
│   ├── titanic_theme.json       Custom theme (navy, gold, teal, coral)
│   └── dax_measures.md          All DAX columns and measures
├── outputs/                     Summary tables written by analysis.py
└── images/
    └── dashboard.png            Dashboard screenshot
```

## Project workflow

1. **Problem statement**: define the question and objectives.
2. **Dataset information**: profile the data and document every column.
3. **Cleaning**: handle missing ages, cabins and ports; check duplicates, outliers and zero fares.
4. **Analysis**: survival by sex, class, age, family size, port and title.
5. **Dashboard**: a one-page interactive Power BI report with slicers, KPI cards and eight charts.
6. **Insights**: eight findings and the limits of the data.

## Dashboard features

- Three slicers (Sex, Class, Port) that filter the whole page
- Five KPI cards
- Survival by class, sex, age group, port, family type and title
- Fare vs age scatter plot (log scale), coloured by survival
- Custom theme: teal means survived, coral means did not survive

## Run it yourself

```bash
pip install -r requirements.txt
python scripts/analysis.py
```

Open `powerbi/Titanic.pbix` in Power BI Desktop (free for Windows).

## Tools

Power BI Desktop, DAX, Python (pandas)
