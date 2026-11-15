# Titanic Survival Analysis: Project Report

**Author:** Derrick D. Agbenorto
**Programme:** Swynex Data Analytics Internship, Task 4
**Tools:** Power BI Desktop (DAX), Python (pandas) for verification
**Date:** November 2026

---

## 1. Problem statement

The sinking of the RMS Titanic in April 1912 killed most of the people on board, yet survival was far from random. This project asks:

> **Which passenger characteristics were associated with survival, and how can those patterns be presented in a way that a non-technical audience can explore for themselves?**

**Objectives**

1. Prepare a clean, analysis-ready passenger dataset.
2. Measure survival across sex, travel class, age, port of embarkation, family size and title.
3. Build an interactive Power BI dashboard with filters, KPIs and comparison charts.
4. Summarise the findings as clear, evidence-based insights, and state their limits.

---

## 2. Dataset information

| Item | Detail |
|---|---|
| Subject | Titanic passenger records |
| Size | 891 passengers x 12 columns |
| Target variable | `Survived` (1 = survived, 0 = did not survive) |
| File used | `data/cleaned_titanic.csv` |
| Missing values after cleaning | 0 |
| Duplicate rows / duplicate `PassengerId` | 0 / 0 |

**Data dictionary**

| Column | Type | Description |
|---|---|---|
| `PassengerId` | integer | Unique passenger identifier (1 to 891) |
| `Survived` | integer | 0 = did not survive, 1 = survived |
| `Pclass` | integer | Ticket class: 1 = upper, 2 = middle, 3 = lower |
| `Name` | text | Passenger name, including title (Mr, Mrs, Miss, Master and so on) |
| `Sex` | text | `male` or `female` |
| `Age` | decimal | Age in years (0.42 to 80) |
| `SibSp` | integer | Number of siblings or spouses aboard |
| `Parch` | integer | Number of parents or children aboard |
| `Ticket` | text | Ticket number |
| `Fare` | decimal | Ticket fare, originally in pounds sterling (0 to 512.33) |
| `Cabin` | text | Cabin number, or `Unknown` |
| `Embarked` | text | Port of embarkation: S = Southampton, C = Cherbourg, Q = Queenstown |

**Overall picture:** 342 of the 891 passengers survived, an overall survival rate of **38.4%**. The average age is 29.1 and the average fare is 32.20.

---

## 3. Data cleaning process

The raw dataset has gaps in three columns. The table below lists each issue and how it was handled.

| Issue | Raw data | Treatment | Why |
|---|---|---|---|
| Missing `Age` | 177 passengers (19.9%) | Filled with the median age of passengers in the same class and sex | Age differs strongly by class and sex, so a group median is more realistic than one overall value. The cleaned file shows the expected spikes at the group medians (for example 105 third-class men at 25.0 and 42 third-class women at 21.5). |
| Missing `Cabin` | 687 passengers (77.1%) | Replaced with `Unknown` | Too sparse to estimate. The cleaned file has exactly 687 `Unknown` cabins, and the column is not used in the analysis. |
| Missing `Embarked` | 2 passengers | Filled with the most common port, Southampton (S) | A mode fill is the standard choice for a tiny number of gaps in a categorical field. |
| Zero fares | 15 passengers | Kept | Plausibly genuine records (for example staff or special tickets). Removing them would drop real passengers. |
| Fare outliers | Maximum 512.33 | Kept; the scatter plot uses a log scale | The extreme fares are real first-class tickets. |
| Infants | 7 passengers under 1 year | Kept | Valid ages (minimum 0.42). |
| Duplicates | None found | No action | Checked on full rows and on `PassengerId`. |

**Derived fields** (created in Power BI with DAX, see `powerbi/dax_measures.md`): `Survival Status`, `Class Label`, `Age Group`, `Age Group Sort`, `Family Size`, `Family Type`, `Port`, `Title`, and a helper column `Scatter Group` used to colour the scatter plot.

**Validation:** the cleaned file contains 891 rows, 12 columns, no missing values and no duplicates. `scripts/analysis.py` re-computes every number in this report from the cleaned file.

---

## 4. Analysis

All rates are the share of passengers in the group who survived.

### 4.1 Sex

| Sex | Passengers | Survivors | Survival rate |
|---|---|---|---|
| Female | 314 | 233 | **74.2%** |
| Male | 577 | 109 | **18.9%** |

### 4.2 Travel class

| Class | Passengers | Survivors | Survival rate | Average fare |
|---|---|---|---|---|
| 1st | 216 | 136 | **63.0%** | 84.15 |
| 2nd | 184 | 87 | **47.3%** | 20.66 |
| 3rd | 491 | 119 | **24.2%** | 13.68 |

### 4.3 Class and sex together

| Class | Women | Men |
|---|---|---|
| 1st | 96.8% | 36.9% |
| 2nd | 92.1% | 15.7% |
| 3rd | 50.0% | 13.5% |

### 4.4 Age group

| Age group | Passengers | Survival rate |
|---|---|---|
| Child (0-12) | 69 | **58.0%** |
| Teen (13-19) | 95 | 41.1% |
| Adult (20-39) | 543 | 36.3% |
| Middle-aged (40-59) | 158 | 37.3% |
| Senior (60+) | 26 | 26.9% |

### 4.5 Family size

| Family type | Passengers | Survival rate |
|---|---|---|
| Solo | 537 | 30.4% |
| Small family (2-4) | 292 | **57.9%** |
| Large family (5+) | 62 | **16.1%** |

### 4.6 Port of embarkation

| Port | Passengers | Survival rate | Share travelling 1st class |
|---|---|---|---|
| Cherbourg | 168 | 55.4% | 50.6% |
| Queenstown | 77 | 39.0% | 2.6% |
| Southampton | 646 | 33.9% | 20.0% |

### 4.7 Title

| Title | Passengers | Survival rate |
|---|---|---|
| Mrs | 125 | 79.2% |
| Miss | 182 | 69.8% |
| Master | 40 | 57.5% |
| Mr | 517 | 15.7% |

Rare titles (Capt, Col, Don, Lady, Sir and others) have fewer than 10 passengers each and are not interpreted individually.

### 4.8 Survivors compared with non-survivors

| Group | Passengers | Average age | Average fare |
|---|---|---|---|
| Survived | 342 | 28.1 | 48.40 |
| Did not survive | 549 | 29.7 | 22.12 |

---

## 5. Dashboard

![Titanic Power BI dashboard](images/dashboard.png)

The dashboard is a single interactive page (`powerbi/Titanic.pbix`) with a dark navy and gold theme (`powerbi/titanic_theme.json`). Teal always means *survived* and coral always means *did not survive*.

| Area | Visuals |
|---|---|
| Filters | Three dropdown slicers: Sex, Class Label, Port. They filter the whole page. |
| KPI cards | Total Passengers (891), Survivors (342), Survival Rate (38%), Avg Age (29.1), Avg Fare (32.20) |
| Row 1 | Survival rate by class (column chart); survival by sex (100% stacked bar); survived vs did not survive (donut) |
| Row 2 | Passengers and survival rate by age group (column and line); passengers by port (bar); survival rate by family type (bar) |
| Row 3 | Fare vs age scatter, coloured by survival, with a log fare axis; passengers by title (top 8) |

**Design notes**

- The slicers drive every visual, so a reader can ask questions such as "how did women in 3rd class do?" with two clicks.
- Edit-interaction settings stop a click on one chart from filtering the KPI cards.
- The fare axis is logarithmic because a few very high fares would otherwise flatten the rest of the plot.
- The cards display a `$` symbol because of Power BI's currency format. The original fares are in pounds sterling.

**Measures used**: `Total Passengers`, `Survivors`, `Survival Rate`, `Avg Age`, `Avg Fare` (full DAX in `powerbi/dax_measures.md`).

---

## 6. Key business insights

The Titanic is a historical case, but the way survival divided across groups is a useful model for any risk, safety or service-prioritisation question: *who is most exposed, who is protected, and why?*

1. **Sex was the strongest dividing line.** Women survived at 74.2% against 18.9% for men, a gap of about 4 to 1. Any analysis of outcomes should check this dimension first.
2. **Class mattered almost as much.** Survival fell from 63.0% in 1st class to 47.3% in 2nd and 24.2% in 3rd. Third class made up 55.1% of passengers but only 34.8% of survivors, so lower-fare customers carried a disproportionate share of the loss.
3. **The effects compound.** Women in 1st and 2nd class survived at 96.8% and 92.1%. Men in 3rd class survived at 13.5%. Looking at one factor at a time hides this gap, which is why the dashboard lets users combine filters.
4. **Children were prioritised.** Children aged 0 to 12 survived at 58.0% against 36.3% for adults in their twenties and thirties. Seniors had the lowest rate (26.9%), though only 26 people are in that group.
5. **Family size had a non-linear effect.** Small families (2 to 4 people) survived at 57.9%, solo travellers at 30.4%, and large families (5 or more) at 16.1%. Large groups appear to have been the hardest to keep together and move.
6. **The port effect is mostly a class effect.** Cherbourg passengers survived at 55.4% against 33.9% at Southampton, but half of the Cherbourg passengers (50.6%) travelled 1st class against 20.0% at Southampton. Port should not be treated as a cause on its own.
7. **Fare works as a proxy for access.** Survivors paid an average fare of 48.40 against 22.12 for non-survivors. Spending tracks closely with position on the ship and therefore with access to lifeboats.
8. **Adult men travelling as "Mr" were the highest-risk large group.** They were 517 of 891 passengers and only 15.7% survived.

**What an analyst or decision-maker can take from this**

- Segment before averaging. The overall 38% hides outcomes ranging from 13.5% to 96.8%.
- Identify high-exposure groups early (here: adult men, 3rd class, large families) and check whether policy, layout or access explains the gap.
- Treat cheap-to-measure proxies such as fare or class as signals of unequal access, and test them against outcomes.
- Build dashboards with combined filters so stakeholders can test their own questions.

---

## 7. Limitations

- **Association, not causation.** The data shows who survived, not why. Rescue priority, cabin location and time to reach the deck all influenced outcomes but are only partly captured.
- **Imputed ages.** About 20% of ages were estimated from class and sex medians, so age-group results are approximate.
- **Small groups.** Seniors (26), large families (62) and most titles other than Mr, Mrs, Miss and Master have very few passengers, so their rates are unstable.
- **Subset of passengers.** The dataset contains 891 records and does not cover everyone on board, and crew are not included.
- **Cabin data is largely missing** (687 of 891), so deck location could not be analysed.

---

## 8. How to reproduce

```bash
pip install -r requirements.txt
python scripts/analysis.py      # re-computes every figure above into outputs/
```

Open `powerbi/Titanic.pbix` in Power BI Desktop to explore the dashboard. To apply the theme to a fresh report, use **Design > Themes > Browse for themes** and select `powerbi/titanic_theme.json`.
