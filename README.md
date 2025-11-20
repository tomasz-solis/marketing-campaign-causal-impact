# Marketing Campaign Causal Impact: A Difference-in-Differences Analysis

**Estimating the causal effect of macroeconomic conditions on customer subscription rates using the 2008 financial crisis as a natural experiment**

---

## 🎯 Project Overview

This project applies **Difference-in-Differences (DiD)** methodology to estimate how economic shocks affect consumer financial decisions. Using the UCI Bank Marketing dataset, I exploit the 2008 financial crisis as a natural experiment to identify the causal effect of macroeconomic conditions on term deposit subscriptions.

**Core Question:** Did customers subscribe to term deposits *because of* deteriorating economic conditions (flight to safety), or were they already predisposed to subscribe?

**Why This Matters:** In product analytics and customer targeting (e.g., ICP scoring, feature launches), distinguishing selection effects from true causal effects is critical for resource allocation and strategic decision-making.

---

## 📊 Dataset

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

## 🔬 Methodology

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

## 🔑 Key Findings

### **1. Massive Subscription Rate Increase During Crisis**

| Wave | Time Period | N Customers | Subscription Rate | Economic Context |
|------|-------------|-------------|-------------------|------------------|
| **Wave 1** | May-Aug 2008 | 7,475 | **4.4%** | Pre-crisis, high interest rates |
| **Wave 2** | Apr-Aug 2009 | 1,650 | **16.8%** | Crisis recovery, rock-bottom rates |

**Naive difference: +12.4 percentage points (+282% increase)**

---

### **2. Strong Economic Shock Between Waves**

The 2008 financial crisis created dramatic economic divergence:

- **Employment variation rate:** Swung from +1.26% (growth) to -1.91% (recession)
- **Interest rates collapsed:** Euribor 3m dropped 73% (4.91% → 1.32%)
- **Consumer confidence deteriorated:** -38.9 → -45.8
- **Employment fell:** 114,000 jobs lost

This provides the quasi-experimental variation needed for causal identification.

---

### **3. Data Structure Insights**

**Challenge:** No explicit customer IDs in dataset.

**Solution:** Created pseudo-customer ID using stable demographics:
- Age, job, marital status, education, housing status, loan status, contact method
- Identified **14,010 unique customers** from 41,188 contact events (~3 contacts per customer)

**Sample Selection:**
- Total customers in analysis waves: 11,970
- Single-wave customers: 9,858 (82%)
- Cross-wave contamination: 2,112 (18%) - **excluded**

**Prior Contact Analysis:**
- Wave 1: 100% fresh prospects (no prior contact)
- Wave 2: 69% fresh prospects, 31% had previous contact history
- Customers with prior contact converted at 12.6% (vs 16.8% for fresh prospects)
- **Key decision:** Restrict to fresh prospects only to ensure apples-to-apples comparison

---

### **4. "Flight to Safety" Hypothesis**

**Counterintuitive Result:** Subscription rates increased dramatically *during* economic crisis.

**Economic Interpretation:**
1. **Interest rate effect:** When rates crash, term deposits become more attractive relative to other safe assets
2. **Risk aversion:** During crises, customers seek guaranteed returns over risky investments
3. **Wealth preservation:** Term deposits offer capital protection when market volatility is high

**Confounding addressed:**
- Campaign intensity differed (2.94 vs 2.32 contacts) - controlled in regression
- Customer demographics balanced (age, education, job)
- Prior relationship history eliminated through sample restriction

---

## 📂 Project Structure

```
marketing-campaign-causal-impact/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── data/
│   ├── raw/
│   │   └── bank-additional-full.csv   # Original UCI dataset
│   └── processed/
│       └── analysis_sample.csv        # Clean analysis dataset (fresh prospects only)
├── notebooks/
│   ├── 01_exploration.ipynb           # Data exploration, economic indicators, time series
│   ├── 02_treatment_design.ipynb      # Sample selection, covariate balance, treatment validation
│   └── 03_did_analysis.ipynb          # DiD estimation, robustness checks, results
├── src/
│   └── utils.py                       # Helper functions for date reconstruction and cleaning
└── outputs/
    └── figures/                       # Visualizations for presentation
```

---

## 🔧 Environment Setup

```bash
# Clone repository
git clone https://github.com/yourusername/marketing-campaign-causal-impact.git
cd marketing-campaign-causal-impact

# Install dependencies
pip install -r requirements.txt

# Run notebooks in order
jupyter notebook notebooks/01_exploration.ipynb
```

---

## 📈 Next Steps

**Notebook 03 (In Progress): DiD Estimation**
1. Simple difference estimation (baseline effect)
2. Regression-adjusted DiD (control for campaign intensity, demographics)
3. Robustness checks:
   - Include long-dormant customers (sensitivity analysis)
   - Contact-level analysis with clustered standard errors
   - Placebo tests with fake treatment dates
4. Interpretation and business implications

---

## 🎓 Learning Objectives

This project demonstrates practical application of causal inference techniques relevant to product analytics:

1. **Identifying natural experiments** in observational data
2. **Handling messy data structures** (no customer IDs, repeated contacts, cross-contamination)
3. **Validating DiD assumptions** (parallel trends, covariate balance)
4. **Addressing confounding** through sample restrictions and regression controls
5. **Transparent documentation** of design decisions and limitations

**Relevance to ICP Scoring:** Similar challenges arise when evaluating customer targeting strategies—selection bias, time-varying treatment, incomplete customer tracking. The methods applied here transfer directly to real-world product analytics.

---

## 👤 Author

**Tomasz Solis** | Senior Product Data Analyst  
Learning causal inference for application to SaaS product analytics and ICP scoring projects.

- Email: [tomasz.solis@gmail.com](mailto:tomasz.solis@gmail.com)
- LinkedIn: [linkedin.com/in/tomaszsolis](https://www.linkedin.com/in/tomaszsolis/)
- GitHub: [github.com/tomasz-solis](https://github.com/tomasz-solis)
---

## 📚 References

- Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the success of bank telemarketing. *Decision Support Systems*, 62, 22-31.
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
- Cunningham, S. (2021). *Causal Inference: The Mixtape*. Yale University Press.

---

## 📄 License

This project is for educational and portfolio purposes. Dataset sourced from UCI Machine Learning Repository under their usage terms.
