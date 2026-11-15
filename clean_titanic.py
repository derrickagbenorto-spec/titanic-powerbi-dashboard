"""Reference cleaning script for the raw Titanic passenger file.

The dashboard uses data/cleaned_titanic.csv. This script documents the cleaning
steps described in REPORT.md (section 3) so they can be repeated on the raw file.

Usage (from the project root):
    1. Put the raw file at data/raw/titanic_raw.csv
       (the standard 891-row Titanic training file with the 12 columns listed in REPORT.md)
    2. python scripts/clean_titanic.py

The result is written to data/cleaned_titanic_rebuilt.csv so that the original
cleaned file is never overwritten.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "titanic_raw.csv"
OUT = ROOT / "data" / "cleaned_titanic_rebuilt.csv"

df = pd.read_csv(RAW)
print("Raw shape:", df.shape)
print("Missing values before cleaning:\n", df.isna().sum()[lambda s: s > 0].to_string(), "\n")

# 1. Age: fill with the median age of passengers in the same class and sex.
df["Age"] = df["Age"].fillna(df.groupby(["Pclass", "Sex"])["Age"].transform("median"))

# 2. Cabin: too sparse to estimate, so label the gaps explicitly.
df["Cabin"] = df["Cabin"].fillna("Unknown")

# 3. Embarked: fill the few gaps with the most common port.
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# 4. Integrity checks. Zero fares, extreme fares and infants are kept on purpose.
assert df.isna().sum().sum() == 0, "Missing values remain"
assert not df.duplicated().any(), "Duplicate rows found"
assert not df["PassengerId"].duplicated().any(), "Duplicate PassengerId found"

df.to_csv(OUT, index=False)
print("Clean shape:", df.shape)
print("Saved to", OUT)
