# 📊 Global Tech Layoffs (2020–2023): A Data Analysis Case Study

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-2ea44f)
![License](https://img.shields.io/badge/License-MIT-blue)

A walkthrough of a real, messy, public dataset — global company layoffs from 2020 to 2023 — analyzed the way it's actually done in industry: inspect first, clean with documented judgment calls, question your own assumptions, then conclude.

This project is built for learning purposes: to show the *process* of data analysis, not just the output.

---

## Table of Contents

- [Business Question](#business-question)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Methodology](#methodology)
  - [1. Inspection](#1-inspection)
  - [2. Cleaning](#2-cleaning)
  - [3. Exploratory Analysis](#3-exploratory-analysis)
- [Findings](#findings)
- [Conclusions](#conclusions)
- [Key Takeaways for Learners](#key-takeaways-for-learners)
- [How to Run](#how-to-run)
- [Next Questions to Explore](#next-questions-to-explore)
- [Credits](#credits)

---

## Business Question

> What actually drove tech layoffs from 2020–2023 — and did the popular assumptions people made at the time hold up against the data?

Starting from a specific, answerable question — instead of just "look at this data" — is the first real step of any analysis.

---

## Dataset

- **Source:** [Layoffs Dataset — Kaggle](https://www.kaggle.com/datasets/swaptr/layoffs-2022)
- **Size:** 2,361 raw records
- **Time range:** 2020–2023
- **Coverage:** Companies worldwide, primarily tech
- **Columns:** `company`, `location`, `industry`, `total_laid_off`, `percentage_laid_off`, `date`, `stage` (funding stage), `country`, `funds_raised_millions`

---

## Repository Structure

```
layoffs-case-study/
├── README.md                  ← this file
├── data/
│   ├── layoffs_raw.csv        ← original, uncleaned dataset
│   └── layoffs_clean.csv      ← output after cleaning script runs
└── scripts/
    └── analysis.py            ← full reproducible analysis
```

---

## Methodology

### 1. Inspection

Before any cleaning or charting, the raw data was inspected for shape, types, and gaps:

```python
df.shape          # (2361, 9)
df.dtypes         # 'date' is read as text, not a real date
df.isnull().sum() # total_laid_off: 740 nulls, percentage_laid_off: 785 nulls
df.duplicated().sum()  # 5 exact duplicate rows
```

**Findings before a single insight was drawn:**
- ~31–33% of the two key numeric columns (`total_laid_off`, `percentage_laid_off`) were missing — companies didn't always disclose exact figures.
- `date` was stored as a string, so no time-based grouping was possible yet.
- 5 exact duplicate rows, plus inconsistent text values (`"Crypto Currency"` vs `"Crypto"`, `"United States."` with a stray trailing period).

> **Industry habit:** a wrong conclusion almost always traces back to something not caught at this stage. This step is skipped most often by beginners and is the most important one.

### 2. Cleaning

```python
df = df.drop_duplicates()
df['company'] = df['company'].str.strip()
df['industry'] = df['industry'].replace({'Crypto Currency': 'Crypto'})
df['country'] = df['country'].str.rstrip('.')
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y', errors='coerce')

# Judgment call: drop rows with NO layoff numbers at all —
# impact can't be measured without at least one metric.
df = df.dropna(subset=['total_laid_off', 'percentage_laid_off'], how='all')
# 361 rows dropped, 1,995 remain
```

> **Industry habit:** every deletion or fill-in is a decision that changes the story slightly. Document *why* a row was dropped, not just that it was — someone (often future-you) will ask.

### 3. Exploratory Analysis

Each question below was chosen to test a specific assumption, not just to "look at the data."

| Question | Method |
|---|---|
| Did Covid (2020) cause the worst layoffs? | `groupby('year')['total_laid_off'].sum()` |
| Does more funding mean more layoffs? | `.corr()` between `funds_raised_millions` and `total_laid_off` |
| Who was hit hardest — by volume? | `groupby('company')` / `groupby('industry')` |
| Who was hit hardest — by survival? | Filter `percentage_laid_off == 1.0` (100%, i.e. shut down) |

---

## Findings

**Layoffs by year:**

| Year | Total laid off |
|---|---|
| 2020 | 80,998 |
| 2021 | 15,823 |
| 2022 | 160,661 |
| 2023 | 125,677 |

**Correlation, funds raised vs. total laid off:** `0.077` (essentially no relationship)

**Top 5 companies by total laid off:**

| Company | Total laid off |
|---|---|
| Amazon | 18,150 |
| Google | 12,000 |
| Meta | 11,000 |
| Salesforce | 10,090 |
| Microsoft | 10,000 |

**Total laid off by funding stage (top 3):**

| Stage | Total laid off |
|---|---|
| Post-IPO (public companies) | 204,132 |
| Acquired | 27,576 |
| Series C | 20,017 |

**Companies that shut down entirely (100% laid off):**

| Company | Total laid off | Stage |
|---|---|---|
| Katerra | 2,434 | Unknown |
| Butler Hospitality | 1,000 | Series B |
| Deliv | 669 | Series C |
| Jump | 500 | Acquired |
| SEND | 300 | Seed |

---

## Conclusions

1. **2022 was the worst year for layoffs — not 2020.** The popular narrative blames Covid, but 2022 nearly doubled 2020's total. The pattern looks more like a post-pandemic hiring correction: companies over-hired through 2021 betting on continued growth, then cut hard when it didn't materialize.

2. **Funding size does not predict layoffs.** A correlation of 0.077 between funds raised and total laid off is close to nothing — the intuitive "bigger war chest = bigger company = more layoffs" story doesn't hold.

3. **The biggest layoffs by volume came from cash-rich public companies, not struggling startups.** Amazon, Google, Meta, Salesforce, and Microsoft top the list, and "Post-IPO" companies account for more total layoffs than every other funding stage combined. These were typically 3–10% workforce reductions at financially healthy companies, not signs of distress.

4. **But total shutdowns tell a completely different story.** Companies that laid off 100% of staff — meaning they ceased operating — were early-to-mid-stage startups (Katerra, Butler Hospitality, Deliv, Jump), not the big names above. "Most affected by volume" and "did not survive" are two separate rankings from the same dataset, and picking the wrong one produces a technically correct but practically misleading conclusion.

---

## Key Takeaways for Learners

1. **Inspection is not optional.** Nulls, dtypes, and duplicates decide whether conclusions are even valid.
2. **Cleaning is a series of judgment calls**, each of which should be defensible and documented — not a blind script.
3. **Your first hypothesis is usually wrong or incomplete.** Both "Covid caused it" and "funding size predicts layoffs" fell apart under two lines of code.
4. **The same numbers can tell two true, different stories** depending on how you segment them — total volume vs. survival, in this case.
5. **A finding isn't done until it's a sentence a non-analyst would understand.** "Public companies cut the most people, but early-stage startups were the ones that disappeared entirely" is the deliverable — not the correlation coefficient.

---

## How to Run

```bash
git clone <this-repo-url>
cd layoffs-case-study
pip install pandas
python scripts/analysis.py
```

This regenerates `data/layoffs_clean.csv` and prints every table shown above.

---

## Next Questions to Explore

- Which industries kept cutting into 2023 vs. which recovered after 2022?
- Do layoff percentages differ meaningfully by country?
- Is there a seasonal pattern (e.g., more layoffs in January)?

---

## Credits

- Dataset: [Layoffs 2022 — Kaggle](https://www.kaggle.com/datasets/swaptr/layoffs-2022), tracked from [Layoffs.fyi](https://layoffs.fyi)
- Built as a learning case study on the applied data analysis workflow.

## License

MIT — free to use, fork, and adapt for your own learning or portfolio.
