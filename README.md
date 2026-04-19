# The Four Pillars Project

**A comprehensive economic framework for universal basic income in the age of automation.**

[![License: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## The One-Sentence Version

The Four Pillars framework eliminates income tax, replaces Social Security with personal investment accounts, provides every citizen a guaranteed $25,000 floor funded by consumption and automation taxes, and reaches budget surplus within a decade — all while making every income level better off.

---

## What Is This?

This repository contains the complete design, economic modeling, and supporting analysis for a proposed restructuring of the American fiscal and social safety net. It is not a thought experiment — it is an engineering document with a full federal balance sheet, Monte Carlo simulations, 17 persona stress tests, and a year-by-year implementation plan.

**Core design:**

- **$25,000/year income floor** for every adult US citizen (phased out above $80K earnings)
- **No federal income tax.** No employee FICA. Keep 100% of your paycheck.
- **20% VAT** (groceries, rent, healthcare, education exempt)
- **50% automation tax** on net labor savings from AI/robotics
- **28% corporate tax** (restored to pre-2017 level)
- **Mandatory 10% 401(k)** replacing Social Security — you own it, you keep it, you pass it on
- **Child seed accounts** at birth ($5K seed → $1.2M by age 65)
- **Four pillars** recognizing contribution beyond employment: Creative, Civic, and Family
- **Employer insurance stays** + government covers gaps for the uninsured

**The numbers:** $9.82T total outflows, $7.69T total revenue, $2.13T initial gap (vs $1.30T current deficit). Gap closes to surplus by Year 7-10 as automation tax grows from $0.71T to $2.84T.

---

## Repository Structure

```
fourpillarsproject/
├── docs/                          # Framework documents (CC BY 4.0)
│   ├── Four_Pillars_Whitepaper.md    # Full peer-review paper
│   ├── Executive_Summary.md          # One-page overview
│   ├── UBI_Framework_v1.md           # Master framework design
│   ├── Economic_Model_Research.md    # Balance sheet & GDP analysis
│   ├── Persona_Stress_Tests.md       # 17 scenarios tested
│   ├── Inflation_Analysis.md         # Price stability analysis
│   ├── Transition_Plan.md            # Year-by-year implementation
│   ├── Pilot_Program_Design.md       # Federal demonstration project
│   ├── International_Comparison.md   # Worldwide UBI/VAT/savings comparison
│   ├── Political_Brief.md            # Left/right/center messaging
│   ├── Objections_And_Responses.md   # 20 rebuttals with data
│   └── Expert_Engagement_Plan.md     # Academic outreach strategy
│
├── models/                        # Computational models (MIT)
│   ├── pillar1_calibration.py        # BLS occupation × BEA GDP analysis
│   ├── monte_carlo_tax.py            # 2,000-run revenue simulation
│   ├── floor_optimization.py         # 7 phase-out scenarios
│   ├── retirement_transition.py      # SS→401(k) transition + child seed
│   └── pillar234_calibration.py      # Creative/Civic/Family payment scales
│
├── website/                       # Interactive website (MIT)
│   └── index.jsx                     # React app with calculator
│
├── LICENSE-DOCS.md                # CC BY 4.0 (documents)
├── LICENSE-CODE.md                # MIT (code)
└── README.md                      # This file
```

---

## Quick Start

### Read the Framework

Start with the [Executive Summary](docs/Executive_Summary.md) for a one-page overview, then dive into the [Whitepaper](docs/Four_Pillars_Whitepaper.md) for the full analysis.

### Run the Models

```bash
# All models use Python 3 standard library only — no dependencies required
python models/monte_carlo_tax.py          # 10-year revenue simulation
python models/pillar1_calibration.py      # Occupation × GDP analysis
python models/floor_optimization.py       # Phase-out scenario comparison
python models/retirement_transition.py    # SS transition + child seed accounts
python models/pillar234_calibration.py    # Pillar 2-4 payment calibration
```

### Try the Calculator

The `website/index.jsx` file is a React component that provides an interactive "What does this mean for me?" calculator. It uses Tailwind CSS and Lucide React icons.

---

## Key Findings

| Finding | Detail |
|---------|--------|
| GDP Growth Factor | Wages are 40% below GDP-justified levels (weighted avg GF = 1.68) |
| Monte Carlo surplus | 34.4% probability of surplus by Year 10; 90th percentile by Year 6 |
| Floor optimization | Current v3 design (50¢/$1 from $30K) confirmed optimal for launch |
| 401(k) vs SS | Every worker beats Social Security — min wage worker gets $66K/yr retirement vs $16K from SS |
| Pillar 2-4 cost | $549B total, well within $800B budget allocation |
| Automation tax | Biggest variance driver — $1.18T difference between high and low automation scenarios |

---

## What Makes This Different

This isn't Andrew Yang's $1,000/month. This isn't European-style welfare. This is a complete economic redesign:

- **Eliminates income tax** — no other UBI proposal does this
- **Replaces Social Security** with personally owned investment accounts
- **Rewards contribution** across four dimensions, not just employment
- **Companies pay 37%** of revenue (up from 16% today)
- **Has real math** — Monte Carlo simulated, stress tested, balance sheet complete
- **Self-reinforcing** — automation drives both the need and the funding

---

## Contributing

This is a working paper. We welcome:

- **Economic critique** — find a flaw in the math, challenge an assumption
- **Model improvements** — fork the Python models, test different parameters
- **Policy expertise** — tax law, healthcare economics, retirement policy
- **International data** — better numbers from VAT implementations, UBI pilots, savings programs

Open an issue or submit a pull request. Serious engagement with the substance is what moves this forward.

---

## Author

**Rob DeMaria**
robert@saccasolutions.com

---

## License

- Documents (`docs/`): [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
- Code (`models/`, `website/`): [MIT License](LICENSE-CODE.md)

You are free to share, adapt, and build upon this work — with attribution.
