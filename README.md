# Did the 2008 Crisis Make People Want Term Deposits? A Learning Project

**Using the financial crisis as a natural experiment to learn causal inference**

---

## What I'm Trying to Figure Out

Did customers subscribe to term deposits *because of* the financial crisis (flight to safety), or were they just going to subscribe anyway?

This might seem like a banking question, but it's really about learning **causal inference** - a skill I need for product analytics work at Pleo, especially for evaluating ICP scoring and feature launches.

**The Big Challenge:** People weren't randomly assigned to crisis vs no-crisis. So how do I know if the crisis *caused* behavior change, or if customers were just different to begin with?

---

## The Dataset

**Source:** [UCI Bank Marketing Dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing)
- 41,188 phone calls from a Portuguese bank
- May 2008 - November 2010
- Goal: Get customers to subscribe to term deposits
- Includes: customer demographics, economic indicators, contact history

**The Opportunity:** The 2008 financial crisis happened RIGHT IN THE MIDDLE of their campaign! This creates a "natural experiment" I can use for causal analysis.

---

## My Approach: Difference-in-Differences

**The Natural Experiment:**

| Period | When | Economic Conditions | What I Call It |
|--------|------|-------------------|----------------|
| **Wave 1** | May-Aug 2008 | Pre-crisis, normal times | Control group |
| **Wave 2** | Apr-Aug 2009 | During crisis recovery | Treatment group |

**The Logic:**
- Compare subscription rates before vs after crisis
- But also account for natural time trends
- DiD = (Wave 2 - Wave 1) adjusted for time

**What Made This Work:**
- 8-month gap between waves (clean separation)
- Huge economic shock:
  - Interest rates: 4.9% → 1.3% (73% drop!)
  - Jobs: +1.3% growth → -1.9% decline (114k lost)
  - Consumer confidence: -38.9 → -45.8

---

## What I Learned (The Journey)

### Challenge 1: No Customer IDs

The dataset had 41,188 contacts but no way to tell which contacts were the same person.

**My Solution:** Created "pseudo-IDs" using demographics (age, job, education, marital status, etc.)
- Identified ~14,000 unique customers
- About 3 contacts per customer on average

**What I Learned:** Sometimes you have to be creative with messy data.

### Challenge 2: People Were Contacted Multiple Times

Some customers were contacted in both waves - this creates "contamination."

**My Solution:** Excluded cross-wave customers (kept only single-wave)
- Lost 18% of data, but gained clean comparison
- Better to have smaller, cleaner sample

**What I Learned:** Sometimes you SHOULD throw away data to get causal clarity.

### Challenge 3: Which Customers to Include?

Initial dataset had customers with prior contact history - not comparable.

**My Solution:** Restricted to **first-time contacts only** (previous=0, pdays=999)
- Final sample: 9,125 customers (7,475 Wave 1, 1,650 Wave 2)

**What I Learned:** Sample restrictions are crucial for causal inference.

---

## What I Found

### Main Result: 10.9 percentage point increase (250% jump)

I built up my analysis step by step:

| Model | Wave 2 Effect | What I Added | Why |
|-------|---------------|--------------|-----|
| **Model 1** | 12.5pp | Nothing (just difference) | Baseline |
| **Model 2** | 12.3pp | Campaign intensity | Control for targeting |
| **Model 3** | 11.8pp | + Demographics | Control for who they called |
| **Model 4** | **10.9pp** | + Month controls | **Final - adjusted for time trend** |

**What I Discovered Through Testing:**

1. **Time Trend Issue:** Found through placebo test that Wave 1 had an upward trend
   - Subscription rates went from 3% → 6% even before crisis
   - Had to control for month to remove this bias
   - Adjusted estimate from 11.8pp to 10.9pp

2. **Sample Sensitivity:** Effect varies by customer type
   - Fresh prospects only: 10.9pp
   - Including dormant customers: 9.5pp
   - Difference is modest (13%) - effect is robust

3. **Heterogeneous Effects:** Effect varied by age
   - Seniors (>50): 16.2pp - most responsive
   - Middle-aged (36-50): 7.5pp - least responsive  
   - Young (≤35): 11.1pp - close to average

**Final Answer:** The crisis increased subscriptions by about **10.9 percentage points** among first-time contacts - that's a **250% increase** from the baseline rate of 4.4%.

---

## The "Aha!" Moments

### Finding 1: Placebo Test Revealed a Problem

When I split Wave 1 into early vs late, I found a significant "effect" - but both periods were pre-crisis! This revealed a time trend I hadn't expected.

**What I Did:** Added month controls to remove the trend. Estimate dropped from 11.8pp to 10.9pp.

**What I Learned:** Always run placebo tests. They find issues you didn't know existed.

### Finding 2: Multicollinearity is Actually Good Here

I tried adding economic indicators (interest rates, employment) as controls, but they were TOO correlated with wave_2 (r > 0.99).

**What I Realized:** This isn't a bug - it's a feature! The economic shock IS the treatment. Can't separate them because they're the same thing.

**What I Learned:** Sometimes you CAN'T add controls, and that's okay.

### Finding 3: Effect is Robust

Worried my result depended on sample choices, I tested including dormant customers.

**What I Found:** Effect only dropped from 10.9pp to 9.5pp (13% smaller) - still huge.

**What I Learned:** When your result holds up across different samples, that's reassuring.

---

## Project Structure

```
marketing-campaign-causal-impact/
├── notebooks/
│   ├── 00_wip.ipynb                   # Random explorations
│   ├── 01_exploration.ipynb           # Understanding the data
│   ├── 02_treatment_design.ipynb      # Sample selection & validation
│   └── 03_did_analysis.ipynb          # DiD estimation
├── data/
│   ├── raw/bank-additional-full.csv
│   └── processed/
│       ├── data_with_waves.csv        # With wave assignments
│       └── analysis_sample.csv        # Clean sample (9,125 customers)
├── outputs/
│   ├── did_final_results.json         # All results
│   ├── did_regression_progression.csv # Model comparison
│   ├── did_sample_sensitivity.csv     # Robustness check
│   └── figures/                       # 17 visualizations
└── src/
    └── utils.py                       # Helper functions
```

---

## Current Progress

**Status: Complete**

### Notebook 01: Data Exploration
- Contact volume patterns
- Economic indicator trends
- Subscription rate patterns
- Wave definitions

### Notebook 02: Treatment Design
- Created pseudo-customer IDs
- Handled cross-wave contamination
- Sample restriction to fresh prospects
- Covariate balance checks

### Notebook 03: DiD Analysis
- **Section 1-2:** Simple difference estimation (12.5pp)
- **Section 3:** Progressive model building (12.5pp → 10.9pp)
- **Section 4:** Interpretation and mechanism
- **Section 5:** Robustness checks (sample sensitivity)
- **Section 6:** Placebo tests (found time trend, adjusted)
- **Section 7:** Heterogeneous effects (by age)
- **Section 8:** Mechanism exploration (multicollinearity)
- **Section 9:** Complete summary (learning journey)
- **Section 10:** Save results (JSON, CSV files)

---

## Key Lessons

1. **Natural experiments exist in product data**
   - Feature launches, pricing changes, external shocks
   - Look for "before/after" opportunities with clean separation

2. **Sample restrictions are your friend**
   - Better small & clean than large & messy
   - Think carefully about who to include

3. **Check for time trends**
   - Placebo tests revealed issues I wouldn't have found otherwise
   - Don't assume parallel trends - test them

4. **Not all controls are good controls**
   - Mediators vs confounders matter
   - Sometimes multicollinearity tells you something important

5. **Robustness checks**
   - Test different samples, test different specifications
   - If result holds up, you can trust it more

6. **Finding problems is good science**
   - I found a time trend and adjusted for it
   - This makes the analysis stronger, not weaker
   - Honesty > perfection

---

## Files Created

**Analysis Outputs:**
- `outputs/did_final_results.json` - Comprehensive results dictionary
- `outputs/did_regression_progression.csv` - Model comparison table
- `outputs/did_sample_sensitivity.csv` - Robustness check comparison

**Visualizations (17 total):**
1. Daily contact volume
2. Economic indicators over time
3. Monthly subscription rates
4. Contact intensity distribution
5. Customer demographics
6. Covariate balance check
7. Economic divergence (Wave 1 vs Wave 2)
8. Subscription rates (fresh prospects)
9. Naive comparison (before/after)
10. Multicollinearity visualization
11. DiD estimate stability
12. Sample sensitivity comparison
13. Monthly rate trends
14. Final sample sensitivity
15. Heterogeneous effects by age
16. Economic shock (dual axis)
17. Economic shock magnitude

---

## How to Run This

```bash
# Clone and setup
git clone https://github.com/tomasz-solis/marketing-campaign-causal-impact.git
cd marketing-campaign-causal-impact
pip install -r requirements.txt

# Run notebooks in order
jupyter notebook notebooks/01_exploration.ipynb
jupyter notebook notebooks/02_treatment_design.ipynb
jupyter notebook notebooks/03_did_analysis.ipynb
```

---

## Honest Limitations

**What I CAN claim:**
- Strong evidence for causal effect (~11pp)
- Effect is robust to sample definition (13% variation)
- "Flight to safety" mechanism is plausible
- Methodology is rigorous (placebo tests, robustness checks)

**What I CANNOT claim:**
- Would this work in other countries? (Dataset only from  Portugal)
- Would this work for other crises? (Dataset covers 2008 financial crisis)
- Long-term effects? (Only observed subscription, not retention)
- Exact mechanism split? (Can't separate interest rate vs job loss effects)

**Why this matters:** Being honest about what you don't know is just as important as being confident about what you do know.

---

## About Me

**Tomasz Solis** | Senior Product Data Analyst at Pleo

I'm learning causal inference to apply to product analytics challenges - specifically evaluating ICP scoring effectiveness where randomized experiments aren't possible.

This project is my learning journey, not a demonstration of expertise. I'm documenting what I discover, including mistakes and corrections, because that's how real analysis works.

- Email: tomasz.solis@gmail.com
- LinkedIn: [linkedin.com/in/tomaszsolis](https://www.linkedin.com/in/tomaszsolis/)
- GitHub: [github.com/tomasz-solis](https://github.com/tomasz-solis)

---

## What I'm Learning From

**Books:**
- Scott Cunningham - *Causal Inference: The Mixtape*
- Matheus Facure - *Causal Inference in Python*

**Dataset:**
- Moro, Cortez, & Rita (2014) - UCI Bank Marketing dataset

---

## Project Status

**Status: Complete**

- Notebooks 01-02: Complete
- Notebook 03: Complete (all 10 sections)
- Results saved: JSON + CSV files
- Visualizations: 17 figures created

---

## Summary

I used the 2008 financial crisis as a natural experiment to estimate whether the crisis causally affected term deposit subscriptions. After careful sample selection, progressive model building, and rigorous robustness checking (including finding and correcting for a time trend through placebo tests), I estimated the crisis increased subscription rates by approximately **10.9 percentage points** (a 250% increase) among first-time banking prospects. 

The effect operates through "flight to safety" - when interest rates crashed and jobs disappeared, people sought guaranteed returns. The result is robust across sample definitions (only 13% variation) and shows interesting heterogeneity by age (seniors responded most strongly at 16.2pp).

---

**Last Updated:** November 25, 2025  <br>
**Status:** Complete - ready for discussion and application
