# Marketing Campaign Causal Impact: A Difference-in-Differences Analysis

**Estimating the causal effect of macroeconomic conditions on customer subscription rates using the 2008 financial crisis as a natural experiment**

---

## 🎯 Project Overview

This project applies **Difference-in-Differences (DiD)** methodology to estimate how economic shocks affect consumer financial decisions. Using the UCI Bank Marketing dataset, I exploit the 2008 financial crisis as a natural experiment to identify the causal effect of macroeconomic conditions on term deposit subscriptions.

**Core Question:** Did customers subscribe to term deposits *because of* deteriorating economic conditions (flight to safety), or were they already predisposed to subscribe?

**Why This Matters:** In product analytics and customer targeting (e.g., ICP scoring, feature launches), distinguishing selection effects from true causal effects is critical for resource allocation and strategic decision-making.

---

## Dataset

- **Source:** [UCI Machine Learning Repository - Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing)
- **Observations:** 41,188 customer contact events from a Portuguese bank
- **Time Period:** May 2008 - November 2010
- **Outcome:** Binary - Customer subscribed to term deposit (yes/no)
- **Features:** 
  - Customer demographics (age, job, education, marital status)
  - Contact history (campaign intensity, days since last contact, previous campaigns)
  - Economic indicators (employment variation rate, consumer price index, consumer confidence, Euribor 3-month rate, number employed)
  - Campaign timing (contact date, month, day of week)

---

## Methodology

### **Causal Identification Strategy: Difference-in-Differences**

**Natural Experiment:** The 2008 global financial crisis created an exogenous shock to economic conditions between two marketing campaign waves.

**Treatment Definition:**
- **Wave 1 (Control):** Customers contacted May-August 2008 (pre-crisis)
- **Wave 2 (Treatment):** Customers contacted April-August 2009 (crisis recovery)

**Key Features:**
1. **Clean temporal separation:** 8-month gap with minimal marketing activity (September 2008-March 2009)
2. **Dramatic economic divergence:**
   - Employment variation rate: +1.3% → -1.9% 
   - Euribor 3-month rate: 4.9% → 1.3%
   - Consumer confidence index: -38.9 → -45.8
   - Employment level: 5,211k → 5,097k

**Sample Restriction:** Analysis limited to **first-time contacts only** (customers with no prior marketing exposure) to ensure clean comparison and eliminate selection bias from relationship history.
- Final sample: **9,125 customers** (7,475 Wave 1, 1,650 Wave 2)

---

## Key Findings

### **1. Causal Effect: +11.78 Percentage Points**

**DiD Estimation Results (Notebook 03):**

| Specification | Wave 2 Effect | Std Error | R² | Controls |
|---------------|---------------|-----------|-----|----------|
| **Model 1:** Baseline | +12.46pp*** | 0.0066 | 0.037 | None |
| **Model 2:** + Campaign | +12.34pp*** | 0.0067 | 0.038 | Campaign intensity |
| **Model 3:** + Demographics | **+11.78pp***✓ | 0.0068 | 0.044 | Campaign + demographics |

***p < 0.001  
✓ Preferred specification

**Interpretation:**
- Being contacted during crisis recovery (vs pre-crisis) causally increased subscription probability by **11.78 percentage points**
- This represents a **268% increase** over the baseline rate of 4.4%
- 95% Confidence Interval: [10.45pp, 13.11pp]

**Coefficient Stability:**
- Estimate changed only -5.5% across specifications (12.46pp → 11.78pp)
- Indicates **minimal selection bias** — Wave 1 and Wave 2 customers are comparable on observables
- Effect is robust to controlling for demographics and campaign intensity

**Why Model 3 is Preferred:**
- Controls for potential confounders (age, job, education, marital status, campaign intensity)
- Does NOT over-control for mediators (economic indicators cause multicollinearity: r > 0.99 with wave_2)
- Captures **total causal effect** operating through economic channels

---

### **2. Economic Mechanism: "Flight to Safety"**

The causal effect operates through three economic channels:

**1. Interest Rate Channel (Primary)**
- Euribor 3-month rate collapsed 73%: 4.91% → 1.32%
- Lower rates made term deposits more attractive relative to other safe assets
- When market returns crashed, guaranteed returns became appealing

**2. Risk Aversion Channel**
- Employment variation rate: +1.26% (growth) → -1.91% (recession)
- Consumer confidence deteriorated: -38.9 → -45.8
- Job losses (114,000) created existential uncertainty
- Customers sought capital preservation over risky investments

**3. Wealth Protection**
- Financial crisis created market volatility
- Term deposits offered stability and guaranteed returns
- Risk-averse behavior intensified during uncertainty

**Evidence:**
- Economic indicators are near-perfectly correlated with wave_2 (r = -0.99 for euribor3m, r = -0.99 for emp.var.rate)
- This confirms economic shock IS the treatment mechanism
- Cannot statistically separate "wave effect" from "economic effect" — they are observationally equivalent

---

### **3. Massive Subscription Rate Increase During Crisis**

| Wave | Time Period | N Customers | Subscription Rate | Economic Context |
|------|-------------|-------------|-------------------|------------------|
| **Wave 1** | May-Aug 2008 | 7,475 | **4.4%** | Pre-crisis, high interest rates |
| **Wave 2** | Apr-Aug 2009 | 1,650 | **16.8%** | Crisis recovery, rock-bottom rates |

**Naive difference: +12.5 percentage points (+284% relative increase)**

---

### **4. Data Structure Insights**

**Challenge:** No explicit customer IDs in dataset.

**Solution:** Created pseudo-customer ID using stable demographics:
- Age, job, marital status, education, housing status, loan status, contact method
- Identified **14,010 unique customers** from 41,188 contact events (~3 contacts per customer)

**Sample Selection:**
- Total customers in analysis waves: 11,970
- Single-wave customers: 9,858 (82%)
- Cross-wave contamination: 2,112 (18%) - **excluded to ensure clean comparison**

**Prior Contact Analysis:**
- Wave 1: 100% fresh prospects (no prior contact)
- Wave 2: 69% fresh prospects, 31% had previous contact history
- Customers with prior contact converted at 12.6% (vs 16.8% for fresh prospects)
- **Key decision:** Restrict to fresh prospects only (previous=0, pdays=999) to ensure apples-to-apples comparison

**Covariate Balance:**
- Age difference: 1.5 years (3.5% — well balanced ✓)
- Campaign intensity: 21% difference (controlled in regression)
- Demographics (job, marital, education): similar distributions
- Economic indicators: PERFECT divergence (good for DiD!) ✓

---

## Project Structure

```
marketing-campaign-causal-impact/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── data/
│   ├── raw/
│   │   └── bank-additional-full.csv   # Original UCI dataset
│   └── processed/
│       ├── data_with_waves.csv        # Customer-level with wave assignments
│       └── analysis_sample.csv        # Clean analysis dataset (fresh prospects only)
├── notebooks/
│   ├── 01_exploration.ipynb           # Data exploration, economic indicators, time series
│   ├── 02_treatment_design.ipynb      # Sample selection, covariate balance, treatment validation
│   └── 03_did_analysis.ipynb          # DiD estimation (Models 1-3), robustness checks [IN PROGRESS]
├── src/
│   └── utils.py                       # Helper functions (date reconstruction, pseudo-ID creation)
└── outputs/
    └── figures/                       # 9 publication-ready Plotly visualizations
        ├── 01_daily_contact_volume.png
        ├── 02_economic_indicators.png
        ├── 03_monthly_subscription_rates.png
        ├── 04_contact_intensity_distribution.png
        ├── 05_customer_demographics_distribution.png
        ├── 06_customer_characteristics_balance.png
        ├── 07_economic_indicators.png
        ├── 08_subscription_rates_fresh_prospects.png
        └── 09_subscription_rates_naive_comparison.png
```

---

## Environment Setup

```bash
# Clone repository
git clone https://github.com/tomasz-solis/marketing-campaign-causal-impact.git
cd marketing-campaign-causal-impact

# Install dependencies
pip install -r requirements.txt

# Run notebooks in order
jupyter notebook notebooks/01_exploration.ipynb
```

**Key Dependencies:**
- `pandas`, `numpy`: Data manipulation
- `plotly`: Interactive visualizations
- `statsmodels`: Regression analysis and DiD estimation
- `scipy`: Statistical tests

---

## Progress & Next Steps

### ✅ **Completed (Notebooks 01-03, Sections 1-3)**
1. ✅ Data exploration and economic indicator analysis
2. ✅ Natural experiment identification (2008 crisis as shock)
3. ✅ Customer ID creation from demographics (pseudo_id)
4. ✅ Sample restriction (fresh prospects only, single-wave customers)
5. ✅ Covariate balance validation
6. ✅ DiD estimation (Models 1-3)
7. ✅ Coefficient stability analysis
8. ✅ 9 visualizations

### ⏳ **In Progress (Notebook 03, Sections 4-11)**
1. ⏳ Robustness checks:
   - Include long-dormant customers (pdays=999, previous>0)
   - Contact-level analysis with clustered standard errors
   - Alternative wave boundaries (sensitivity analysis)
   - Exclude May 2008 (campaign ramp-up)
2. ⏳ Placebo tests:
   - Fake treatment dates (within Wave 1)
   - Placebo outcomes (age, pre-determined variables)
3. ⏳ Heterogeneous treatment effects:
   - By age group (young vs middle vs senior)
   - By job type (white collar vs blue collar)
4. ⏳ Mechanism exploration (which economic indicator matters most?)
5. ⏳ Final interpretation and business implications

### **Future Enhancements**
- Section 12: Regression Discontinuity Design (RDD) using campaign intensity threshold
- Panel data methods (if repeated observations per customer)
- Synthetic control method (if comparing regions)
- Causal forests for heterogeneous effect estimation

---

## Learning Objectives

This project demonstrates practical application of causal inference techniques relevant to product analytics:

1. **Identifying natural experiments** in observational data
2. **Handling messy data structures** (no customer IDs, repeated contacts, cross-contamination)
3. **Sample restriction decisions** (when to lose data to gain causal clarity)
4. **Validating DiD assumptions** (covariate balance, parallel trends logic)
5. **Addressing confounding** through regression controls
6. **Transparent documentation** of design decisions and limitations

---

## Business Implications

### **For Financial Services:**
1. **Counter-cyclical marketing opportunity:** Economic downturns may INCREASE demand for safe products
2. **Timing matters:** Campaign ROI can vary 3x based on macroeconomic context
3. **Risk-averse messaging:** More effective during uncertain times
4. **Product positioning:** Emphasize capital preservation during volatility

### **For SaaS/Product Analytics:**
1. **ICP scoring evaluation:** Need cross-sectional variation to avoid confounding with time
2. **Feature launch timing:** Macroeconomic context affects adoption rates
3. **Customer targeting:** Selection into treatment (high ICP score) may be confounded with outcomes
4. **A/B testing limitations:** When can't randomize, quasi-experiments (DiD, RDD) are alternatives

---

## 👤 Author

**Tomasz Solis** | Senior Product Data Analyst  
Building causal inference skills for application to SaaS product analytics and ICP scoring projects at Pleo.

- Email: [tomasz.solis@gmail.com](mailto:tomasz.solis@gmail.com)
- LinkedIn: [linkedin.com/in/tomaszsolis](https://www.linkedin.com/in/tomaszsolis/)
- GitHub: [github.com/tomasz-solis](https://github.com/tomasz-solis)

---

## 📚 References

**Dataset:**
- Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the success of bank telemarketing. *Decision Support Systems*, 62, 22-31.

**Causal Inference Methodology:**
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
- Cunningham, S. (2021). *Causal Inference: The Mixtape*. Yale University Press.
- Huntington-Klein, N. (2021). *The Effect: An Introduction to Research Design and Causality*. Chapman and Hall/CRC.

**DiD Implementation:**
- Difference-in-Differences estimation with repeated cross-sections
- Linear probability model (OLS on binary outcome) with heteroskedasticity-robust standard errors
- Covariate balance checks and specification sensitivity analysis

---

## License

This project is for educational and portfolio purposes. Dataset sourced from UCI Machine Learning Repository under their usage terms.

---

## Project Status

**Current Status:** 🟡 **In Progress** (60% complete)
- ✅ Notebooks 01-02: Complete and documented
- 🟡 Notebook 03: Core DiD analysis complete (Models 1-3), robustness checks in progress
- ⏳ Final documentation: Pending

---

## Quick Results Summary

> **TL;DR:** Using the 2008 financial crisis as a natural experiment, I estimated that being contacted during crisis recovery (vs pre-crisis) causally increased term deposit subscription rates by **11.78 percentage points** (a 268% increase), operating primarily through interest rate effects and risk-averse customer behavior. The analysis handles messy observational data through careful sample restriction, validates DiD assumptions via covariate balance checks, and demonstrates coefficient stability across specifications, providing strong evidence for causal interpretation.

---

**Last Updated**: November 21, 2025
