# Marketing Campaign Causal Impact: A Difference-in-Differences Analysis

## Project Overview
This project applies **Difference-in-Differences (DiD)** methodology to estimate the causal effect of direct marketing campaigns on customer subscription rates using the UCI Bank Marketing dataset.

**Business Question:** Did the marketing campaign increase term deposit subscriptions, or would customers have subscribed anyway?

**Why this matters:** In product analytics (e.g., ICP scoring, feature launches), we need to separate selection effects from true causal effects. This project demonstrates how to do that when randomized experiments aren't available.

## Dataset
- **Source:** [UCI Machine Learning Repository - Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing)
- **Observations:** 41,188 customer contacts
- **Outcome:** Term deposit subscription (yes/no)
- **Features:** Customer demographics, contact history, economic indicators, campaign timing

## Methodology
1. **Identification Strategy:** Difference-in-Differences
2. **Treatment Definition:** [To be defined based on data exploration]
3. **Key Assumption:** Parallel trends (verified visually and statistically)
4. **Robustness Checks:** Event study, placebo tests, alternative specifications

## Planned Project Structure
- `notebooks/01_exploration.ipynb` - Data exploration and treatment design
- `notebooks/02_treatment_design.ipynb` - Treatment/control group creation and validation
- `notebooks/03_did_analysis.ipynb` - Full DiD estimation and robustness checks
- `src/utils.py` - Reusable functions for analysis

## Key Findings
[To be completed after analysis]


## Environment Setup
```bash
pip install -r requirements.txt
```

## Author
Tomasz Solis

Learning causal inference for application to SaaS product analytics and ICP scoring projects.