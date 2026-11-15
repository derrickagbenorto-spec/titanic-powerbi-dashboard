"""Reproduce every figure used in REPORT.md from data/cleaned_titanic.csv.

Usage (from the project root):
    python scripts/analysis.py

Writes summary tables to outputs/ and prints them to the console.
The derived columns mirror the DAX columns used in the Power BI report.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data" / "cleaned_titanic.csv")

# ---- Derived columns (same logic as the DAX calculated columns) ----------
df["Survival Status"] = np.where(df["Survived"] == 1, "Survived", "Did not survive")
df["Class Label"] = df["Pclass"].map({1: "1st Class", 2: "2nd Class", 3: "3rd Class"})
df["Age Group"] = pd.cut(
    df["Age"],
    bins=[-1, 12.999, 19.999, 39.999, 59.999, 200],
    labels=["Child (0-12)", "Teen (13-19)", "Adult (20-39)",
            "Middle-aged (40-59)", "Senior (60+)"],
)
df["Family Size"] = df["SibSp"] + df["Parch"] + 1
df["Family Type"] = np.select(
    [df["Family Size"] == 1, df["Family Size"] <= 4],
    ["Solo", "Small (2-4)"],
    default="Large (5+)",
)
df["Port"] = df["Embarked"].map(
    {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}
)
df["Title"] = df["Name"].str.extract(r", ([^.]*)\.")[0].str.strip()


def survival_table(by):
    t = df.groupby(by, observed=True).agg(
        passengers=("Survived", "size"),
        survivors=("Survived", "sum"),
        survival_rate_pct=("Survived", lambda s: round(s.mean() * 100, 1)),
        avg_fare=("Fare", lambda s: round(s.mean(), 2)),
        avg_age=("Age", lambda s: round(s.mean(), 1)),
    )
    return t


# ---- Headline KPIs -------------------------------------------------------
kpis = pd.Series({
    "total_passengers": len(df),
    "survivors": int(df["Survived"].sum()),
    "survival_rate_pct": round(df["Survived"].mean() * 100, 2),
    "avg_age": round(df["Age"].mean(), 1),
    "avg_fare": round(df["Fare"].mean(), 2),
})
print("HEADLINE KPIs\n", kpis.to_string(), "\n")
kpis.to_csv(OUT / "kpis.csv", header=["value"])

# ---- Survival by single dimension ---------------------------------------
for dim, name in [
    ("Sex", "sex"), ("Class Label", "class"), ("Age Group", "age_group"),
    ("Port", "port"), ("Family Type", "family_type"), ("Title", "title"),
]:
    t = survival_table(dim)
    print(f"SURVIVAL BY {dim.upper()}\n", t.to_string(), "\n")
    t.to_csv(OUT / f"survival_by_{name}.csv")

# ---- Sex x class ---------------------------------------------------------
sc = df.pivot_table(index="Class Label", columns="Sex", values="Survived",
                    aggfunc="mean").mul(100).round(1)
print("SURVIVAL RATE (%) BY CLASS AND SEX\n", sc.to_string(), "\n")
sc.to_csv(OUT / "survival_by_class_and_sex.csv")

# ---- Port x class (is the port effect really a class effect?) ------------
pc = pd.crosstab(df["Port"], df["Class Label"], normalize="index").mul(100).round(1)
print("CLASS MIX (%) BY PORT\n", pc.to_string(), "\n")
pc.to_csv(OUT / "class_mix_by_port.csv")

# ---- Survivors vs non-survivors -----------------------------------------
sv = df.groupby("Survival Status").agg(
    passengers=("Survived", "size"),
    avg_age=("Age", lambda s: round(s.mean(), 2)),
    avg_fare=("Fare", lambda s: round(s.mean(), 2)),
)
print("SURVIVORS VS NON-SURVIVORS\n", sv.to_string(), "\n")
sv.to_csv(OUT / "survivors_vs_non_survivors.csv")

# ---- Data quality checks -------------------------------------------------
print("DATA QUALITY")
print("rows x columns:", df.shape[0], "x", 12)
print("missing values:", int(df[["PassengerId", "Survived", "Pclass", "Name", "Sex",
                                  "Age", "SibSp", "Parch", "Ticket", "Fare",
                                  "Cabin", "Embarked"]].isna().sum().sum()))
print("duplicate rows:", int(df.duplicated().sum()))
print("duplicate PassengerId:", int(df["PassengerId"].duplicated().sum()))
print("Cabin == 'Unknown':", int((df["Cabin"] == "Unknown").sum()))
print("Fare == 0:", int((df["Fare"] == 0).sum()))
print("Age < 1:", int((df["Age"] < 1).sum()))
