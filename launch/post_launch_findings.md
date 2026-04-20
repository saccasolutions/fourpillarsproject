# Post-Launch Findings — Reddit Feedback + Extended Modeling

## Date: April 19, 2026

---

## Extended Monte Carlo Results (20-Year Horizon)

### Without LVT:
| Year | Median Gap | P(Surplus) | Auto Tax | VAT |
|------|-----------|------------|----------|-----|
| 1 | -$1.97T | 0.0% | $0.57T | $4.12T |
| 5 | -$0.94T | 13.3% | $1.02T | $4.86T |
| 10 | +$0.21T | 55.7% | $1.71T | $5.44T |
| 14 | +$1.34T | 70.9% | $2.32T | $5.94T |
| 20 | +$3.73T | 80.5% | $3.42T | $6.77T |

### With 1% Land Value Tax ($240B/yr):
| Year | Median Gap | P(Surplus) |
|------|-----------|------------|
| 9 | +$0.27T | 58.0% |
| 10 | +$0.50T | 62.8% |
| 12 | +$1.09T | 70.7% |
| 17 | +$2.84T | 80.2% |

### Milestones:
| Milestone | Without LVT | With LVT |
|-----------|-------------|----------|
| 25% surplus | Year 7 | Year 6 |
| 34% surplus | Year 8 | Year 7 |
| 50% surplus | Year 10 | Year 9 |
| 70% surplus | Year 14 | Year 12 |
| 80% surplus | Year 20 | Year 17 |

---

## Revenue Tax with Labor Deductions (Alternative to Automation Tax)

- A 2.45% flat rate on (revenue - labor costs) matches $710B Year 1 target
- But only reaches $1.1T by Year 10 (vs $2.84T target) — fixed rate doesn't grow fast enough
- Progressive rate model (rate increases as labor/revenue ratio drops) reaches $1.26T by Year 10
- CONCLUSION: Useful complement but cannot fully replace automation tax alone
- RECOMMENDATION: Consider hybrid — revenue tax as baseline (simpler, harder to game) + automation tax for large documented layoffs

---

## Effective Progressivity Analysis

Framework is MORE progressive than current system at every decile:

| Decile | Income | Current Eff Rate | Four Pillars Net Rate |
|--------|--------|-----------------|----------------------|
| Bottom 10% | $8K | 17.6% tax | -298.5% (net recipient) |
| 20-30% | $24K | 21.6% tax | -91.3% (net recipient) |
| 40-50% | $45K | 21.6% tax | -26.4% (net recipient) |
| 60-70% | $75K | 27.7% tax | +7.5% (net payer) |
| Top 10% | $300K | 40.6% tax | +8.4% (VAT only, before investment/wealth/estate taxes) |

---

## Whitepaper Numbers That Need Updating

1. **Monte Carlo surplus probability**: Whitepaper says "34% by Year 10" — extended model shows 55.7%. Need to reconcile. The 34% may have been from a different parameter set. Should either re-run with original seed to confirm, or update to new number with explanation.

2. **Add 20-year projections**: Whitepaper only covers 10 years. Extended horizon shows much stronger case — 70% surplus by Year 14, 80% by Year 20.

3. **VAT-GDP compounding loop**: Not emphasized enough. VAT grows from $4.1T to $6.8T purely from economic growth. This is a $2.7T revenue increase independent of the automation tax.

4. **Add LVT as recommended addition**: Model shows it accelerates every milestone by ~2 years. Low-risk, high-consensus addition.

5. **Automation tax measurement section**: Needs dedicated section on enforcement mechanics, industry baselines, reporting requirements, and anti-gaming provisions. The revenue-tax-with-labor-deductions hybrid should be presented as an alternative/complement.

6. **Border adjustment mechanism**: Currently mentioned in passing. Needs concrete design spec.

7. **Floor framing**: Everywhere the $25K is mentioned, lead with what a median worker actually takes home ($55,500) and make clear the floor is the foundation, not the income.

8. **Disability/existing benefits**: Add explicit section clarifying the floor does NOT replace disability, Medicaid, or specialized care programs.

---

## New Models Created

- `extended_monte_carlo.py` — 20-year Monte Carlo with LVT scenario
- `feedback_models.py` — Revenue tax alternative, LVT, progressivity analysis

---

## Reddit Thread Takeaways

### r/Futurology (removed, but 20+ comments in ~4 hours):
- Automation tax measurement was #1 concern (5+ commenters)
- Offshoring was #2 concern (4+ commenters)
- $25K floor misunderstood as total income by multiple people
- Revenue tax with labor deductions suggested as alternative (strongest suggestion)
- Georgism/LVT suggested
- VAT, retirement accounts, and Monte Carlo held up with no challenges

### r/BasicIncome:
- MMT framing critique (taxes manage inflation, not "pay for" spending)
- $25K may be too high for current automation levels (25% GDP/capita max suggested)
- Surplus probability questions
- Detailed critique hitting VAT regressivity, 401(k) risk, progressivity, citizenship, disability
- All points have answers in the framework but messaging needs to surface them better
