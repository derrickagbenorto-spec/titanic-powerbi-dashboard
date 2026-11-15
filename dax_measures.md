# DAX columns and measures

The table in the Power BI model is named `Titanic` (loaded from `data/cleaned_titanic.csv`).

Add each formula on its own: **Table tools > New column** for columns, **Home > New measure** for measures. Clear the formula bar first so that `Column =` or `Measure =` is not left in front of the formula.

## Calculated columns

```DAX
Survival Status = IF(Titanic[Survived] = 1, "Survived", "Did not survive")
```

```DAX
Class Label = SWITCH(Titanic[Pclass], 1, "1st Class", 2, "2nd Class", 3, "3rd Class")
```

```DAX
Age Group =
SWITCH(TRUE(),
    ISBLANK(Titanic[Age]), "Unknown",
    Titanic[Age] < 13, "Child (0-12)",
    Titanic[Age] < 20, "Teen (13-19)",
    Titanic[Age] < 40, "Adult (20-39)",
    Titanic[Age] < 60, "Middle-aged (40-59)",
    "Senior (60+)")
```

`Age Group Sort` is built from `Age`, **not** from `Age Group`. Using `Age Group` creates a circular dependency once the sort is applied.

```DAX
Age Group Sort =
SWITCH(TRUE(),
    ISBLANK(Titanic[Age]), 6,
    Titanic[Age] < 13, 1,
    Titanic[Age] < 20, 2,
    Titanic[Age] < 40, 3,
    Titanic[Age] < 60, 4,
    5)
```

Then select `Age Group` and use **Column tools > Sort by column > Age Group Sort**.

```DAX
Family Size = Titanic[SibSp] + Titanic[Parch] + 1
```

```DAX
Family Type =
SWITCH(TRUE(),
    Titanic[Family Size] = 1, "Solo",
    Titanic[Family Size] <= 4, "Small (2-4)",
    "Large (5+)")
```

```DAX
Port = SWITCH(Titanic[Embarked], "S", "Southampton", "C", "Cherbourg", "Q", "Queenstown", "Unknown")
```

```DAX
Title =
IFERROR(
    TRIM(MID(Titanic[Name],
        SEARCH(", ", Titanic[Name]) + 2,
        SEARCH(".", Titanic[Name]) - SEARCH(", ", Titanic[Name]) - 2)),
    "Other")
```

The scatter plot uses a helper column so that the default theme colours land on the right groups (teal for survived, coral for did not survive):

```DAX
Scatter Group = IF(Titanic[Survived] = 1, "A Survived", "B Did not survive")
```

## Measures

```DAX
Total Passengers = COUNTROWS(Titanic)
```

```DAX
Survivors = CALCULATE(COUNTROWS(Titanic), Titanic[Survived] = 1)
```

```DAX
Survival Rate = DIVIDE([Survivors], [Total Passengers])
```

```DAX
Avg Age = AVERAGE(Titanic[Age])
```

```DAX
Avg Fare = AVERAGE(Titanic[Fare])
```

Format `Survival Rate` as a percentage (0 decimals), `Avg Age` as a decimal number (1 decimal) and `Avg Fare` as currency (2 decimals).

## Report settings worth knowing

- Canvas size: 1280 x 960 (custom).
- Scatter plot: Age on the X axis and Fare on the Y axis, both set to **Don't summarize**; Legend is `Scatter Group`; Y axis minimum is 1 with **Logarithmic scale** on.
- Titles chart: filter `Title` to **Top N = 8** by `Total Passengers`.
- Use **Format > Edit interactions** to stop chart clicks from filtering the KPI cards.
