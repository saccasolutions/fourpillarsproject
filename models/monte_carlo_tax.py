#\!/usr/bin/env python3
"""
Tax Revenue Monte Carlo Simulation — Four Pillars UBI Framework
Year-by-year projections with uncertainty bands for all revenue sources.
"""

import random
import math
from dataclasses import dataclass
from typing import List, Dict

random.seed(42)
NUM_SIMULATIONS = 2_000
YEARS = 10

# ============================================================
# BASE PARAMETERS (Year 0 = launch year)
# ============================================================

# GDP
BASE_GDP = 29_000  # $29T in billions

# Revenue sources (Year 1 baseline in billions)
BASE_REVENUE = {
    "VAT": 3_760,
    "Employer_FICA": 990,
    "Corporate_Tax": 840,
    "Automation_Tax": 710,
    "Investment_Income_Tax": 410,
    "Excise_Tariffs": 300,
    "FTT": 200,
    "Corp_Minimum_Tax": 130,
    "Wealth_Tax": 100,
    "Employer_Penalty": 80,
    "Estate_Tax": 80,
    "Digital_Ad_Tax": 60,
    "Buyback_Tax": 40,
}

# Outflows (Year 1 baseline in billions)
BASE_OUTFLOWS = {
    "Floor_Payments": 4_620,
    "Pillar_2_4": 800,
    "Healthcare_Gaps": 1_550,
    "Admin": 50,
    "Federal_Ops": 2_800,
}

TOTAL_BASE_REVENUE = sum(BASE_REVENUE.values())  # $7.70T
TOTAL_BASE_OUTFLOWS = sum(BASE_OUTFLOWS.values())  # $9.82T

# ============================================================
# GROWTH PARAMETERS WITH UNCERTAINTY
# Each parameter: (mean_annual_growth, std_dev)
# ============================================================

GROWTH_PARAMS = {
    # GDP growth drives most other revenues
    "gdp_growth": (0.028, 0.015),  # 2.8% mean, 1.5% std
    
    # VAT grows with consumer spending (correlated with GDP)
    "vat_gdp_elasticity": (1.05, 0.10),  # slightly elastic to GDP
    
    # Automation displacement rate (% of labor force)
    "auto_displacement_yr1": (0.10, 0.02),   # 10% ± 2%
    "auto_displacement_yr10": (0.30, 0.08),  # 30% ± 8%
    
    # Investment income growth
    "investment_income_growth": (0.04, 0.06),  # 4% mean, high volatility
    
    # Corporate profit growth (drives corp tax)
    "corp_profit_growth": (0.03, 0.02),
    
    # Healthcare cost growth
    "healthcare_inflation": (0.04, 0.01),  # 4% ± 1%
    
    # Federal ops growth (defense, debt service)
    "federal_ops_growth": (0.025, 0.01),
    
    # Floor scaling (discretionary, revenue-dependent)
    "floor_scale_threshold": (0.90, 0.05),  # scale when revenue covers 90%+ of outflows
}

def run_simulation():
    """Run a single 10-year simulation."""
    
    # Draw random parameters for this simulation
    gdp_growth_base = random.gauss(*GROWTH_PARAMS["gdp_growth"])
    vat_elasticity = random.gauss(*GROWTH_PARAMS["vat_gdp_elasticity"])
    auto_start = max(0.05, random.gauss(*GROWTH_PARAMS["auto_displacement_yr1"]))
    auto_end = max(auto_start + 0.05, random.gauss(*GROWTH_PARAMS["auto_displacement_yr10"]))
    inv_growth = random.gauss(*GROWTH_PARAMS["investment_income_growth"])
    corp_growth = random.gauss(*GROWTH_PARAMS["corp_profit_growth"])
    health_infl = max(0.02, random.gauss(*GROWTH_PARAMS["healthcare_inflation"]))
    fed_growth = random.gauss(*GROWTH_PARAMS["federal_ops_growth"])
    
    yearly_results = []
    gdp = BASE_GDP
    
    for year in range(1, YEARS + 1):
        # GDP growth with year-specific noise
        year_gdp_shock = random.gauss(0, 0.008)  # annual shock
        gdp_rate = gdp_growth_base + year_gdp_shock
        
        # Recession probability increases every ~7 years
        if random.random() < 0.12:  # ~12% chance of recession year
            gdp_rate = random.gauss(-0.015, 0.01)
        
        gdp = gdp * (1 + gdp_rate)
        gdp_factor = gdp / BASE_GDP
        
        # --- REVENUE ---
        
        # VAT: grows with GDP × elasticity + consumer spending boost from UBI
        ubi_spending_boost = 1.0 + 0.02 * min(year, 5)  # UBI boosts spending ~2%/yr for 5 yrs
        vat = BASE_REVENUE["VAT"] * gdp_factor * vat_elasticity * ubi_spending_boost
        
        # Employer FICA: grows with employment and wage growth
        wage_growth = gdp_rate * 0.6 + 0.01  # wages grow at 60% of GDP rate + 1%
        fica_factor = (1 + wage_growth) ** year
        employer_fica = BASE_REVENUE["Employer_FICA"] * fica_factor
        
        # Corporate tax: grows with profits
        corp_factor = (1 + corp_growth + random.gauss(0, 0.03)) ** year
        corp_tax = BASE_REVENUE["Corporate_Tax"] * max(0.5, corp_factor)
        
        # Automation tax: interpolate displacement from start to end
        displacement = auto_start + (auto_end - auto_start) * (year / YEARS)
        # Total labor cost basis grows with GDP
        labor_cost_basis = 9_200 * gdp_factor  # ~$9.2T total wage bill
        auto_savings = labor_cost_basis * displacement
        auto_tax = auto_savings * 0.50  # 50% tax rate
        
        # Investment income: volatile but trending up
        inv_factor = (1 + inv_growth + random.gauss(0, 0.08)) ** year
        inv_tax = BASE_REVENUE["Investment_Income_Tax"] * max(0.3, inv_factor)
        
        # Other taxes: grow roughly with GDP
        excise = BASE_REVENUE["Excise_Tariffs"] * gdp_factor
        ftt = BASE_REVENUE["FTT"] * gdp_factor * (1 + 0.02 * year)  # market volume grows
        corp_min = BASE_REVENUE["Corp_Minimum_Tax"] * max(0.5, corp_factor)
        wealth = BASE_REVENUE["Wealth_Tax"] * (1 + 0.05) ** year  # wealth concentrates
        employer_pen = BASE_REVENUE["Employer_Penalty"] * (0.9 ** year)  # decreases as compliance rises
        estate = BASE_REVENUE["Estate_Tax"] * (1 + 0.03) ** year
        digital = BASE_REVENUE["Digital_Ad_Tax"] * (1 + 0.08) ** year  # digital grows fast
        buyback = BASE_REVENUE["Buyback_Tax"] * gdp_factor
        
        total_revenue = (vat + employer_fica + corp_tax + auto_tax + inv_tax +
                        excise + ftt + corp_min + wealth + employer_pen +
                        estate + digital + buyback)
        
        # --- OUTFLOWS ---
        
        # Floor: fixed unless scaled (discretionary)
        floor = BASE_OUTFLOWS["Floor_Payments"]
        if year >= 5 and total_revenue / (floor + BASE_OUTFLOWS["Pillar_2_4"] + 
            BASE_OUTFLOWS["Healthcare_Gaps"] * (1 + health_infl) ** year +
            BASE_OUTFLOWS["Admin"] + BASE_OUTFLOWS["Federal_Ops"] * (1 + fed_growth) ** year) > 0.95:
            floor = floor * 1.12  # scale to $28K
        if year >= 8 and total_revenue / (floor + BASE_OUTFLOWS["Pillar_2_4"] +
            BASE_OUTFLOWS["Healthcare_Gaps"] * (1 + health_infl) ** year +
            BASE_OUTFLOWS["Admin"] + BASE_OUTFLOWS["Federal_Ops"] * (1 + fed_growth) ** year) > 0.98:
            floor = BASE_OUTFLOWS["Floor_Payments"] * 1.20  # scale to $30K
        
        pillar24 = BASE_OUTFLOWS["Pillar_2_4"] * (1 + 0.02) ** year  # modest growth
        healthcare = BASE_OUTFLOWS["Healthcare_Gaps"] * (1 + health_infl) ** year
        admin = BASE_OUTFLOWS["Admin"] * (1 + 0.02) ** year
        federal_ops = BASE_OUTFLOWS["Federal_Ops"] * (1 + fed_growth) ** year
        
        total_outflows = floor + pillar24 + healthcare + admin + federal_ops
        
        gap = total_revenue - total_outflows
        
        yearly_results.append({
            "year": year,
            "gdp": gdp,
            "gdp_growth": gdp_rate,
            "total_revenue": total_revenue,
            "total_outflows": total_outflows,
            "gap": gap,
            "vat": vat,
            "auto_tax": auto_tax,
            "corp_tax": corp_tax,
            "employer_fica": employer_fica,
            "inv_tax": inv_tax,
            "floor": floor,
            "healthcare": healthcare,
            "federal_ops": federal_ops,
            "displacement": displacement,
        })
    
    return yearly_results

def run_monte_carlo():
    """Run NUM_SIMULATIONS simulations and compute statistics."""
    
    all_results = []
    for _ in range(NUM_SIMULATIONS):
        all_results.append(run_simulation())
    
    # Compute percentiles for each year
    stats = []
    for year_idx in range(YEARS):
        year_data = [sim[year_idx] for sim in all_results]
        
        revenues = sorted([d["total_revenue"] for d in year_data])
        outflows = sorted([d["total_outflows"] for d in year_data])
        gaps = sorted([d["gap"] for d in year_data])
        auto_taxes = sorted([d["auto_tax"] for d in year_data])
        vats = sorted([d["vat"] for d in year_data])
        
        def percentile(data, pct):
            idx = int(len(data) * pct / 100)
            return data[min(idx, len(data)-1)]
        
        stats.append({
            "year": year_idx + 1,
            "revenue_p10": percentile(revenues, 10),
            "revenue_p25": percentile(revenues, 25),
            "revenue_p50": percentile(revenues, 50),
            "revenue_p75": percentile(revenues, 75),
            "revenue_p90": percentile(revenues, 90),
            "outflow_p50": percentile(outflows, 50),
            "gap_p10": percentile(gaps, 10),
            "gap_p25": percentile(gaps, 25),
            "gap_p50": percentile(gaps, 50),
            "gap_p75": percentile(gaps, 75),
            "gap_p90": percentile(gaps, 90),
            "auto_tax_p50": percentile(auto_taxes, 50),
            "vat_p50": percentile(vats, 50),
            "surplus_probability": sum(1 for g in gaps if g > 0) / len(gaps),
        })
    
    return stats, all_results

def main():
    print("=" * 80)
    print(f"TAX REVENUE MONTE CARLO SIMULATION ({NUM_SIMULATIONS:,} runs, {YEARS} years)")
    print("=" * 80)
    
    print(f"\nBaseline Year 1: Revenue ${TOTAL_BASE_REVENUE:,}B | Outflows ${TOTAL_BASE_OUTFLOWS:,}B | Gap ${TOTAL_BASE_REVENUE - TOTAL_BASE_OUTFLOWS:,}B")
    
    stats, all_results = run_monte_carlo()
    
    # Summary table
    print(f"\n{'Year':>4} {'Rev P10':>9} {'Rev P25':>9} {'Rev P50':>9} {'Rev P75':>9} {'Rev P90':>9} {'Out P50':>9} {'Gap P50':>9} {'P(Surplus)':>10}")
    print("-" * 90)
    for s in stats:
        print(f"{s['year']:>4} ${s['revenue_p10']/1000:>7.2f}T ${s['revenue_p25']/1000:>7.2f}T ${s['revenue_p50']/1000:>7.2f}T ${s['revenue_p75']/1000:>7.2f}T ${s['revenue_p90']/1000:>7.2f}T ${s['outflow_p50']/1000:>7.2f}T ${s['gap_p50']/1000:>+7.2f}T {s['surplus_probability']:>9.1%}")
    
    # Gap analysis
    print(f"\n{'Year':>4} {'Gap P10':>10} {'Gap P25':>10} {'Gap P50':>10} {'Gap P75':>10} {'Gap P90':>10}")
    print("-" * 55)
    for s in stats:
        print(f"{s['year']:>4} ${s['gap_p10']/1000:>+8.2f}T ${s['gap_p25']/1000:>+8.2f}T ${s['gap_p50']/1000:>+8.2f}T ${s['gap_p75']/1000:>+8.2f}T ${s['gap_p90']/1000:>+8.2f}T")
    
    # Key revenue drivers
    print(f"\n{'Year':>4} {'Auto Tax P50':>12} {'VAT P50':>10}")
    print("-" * 30)
    for s in stats:
        print(f"{s['year']:>4} ${s['auto_tax_p50']/1000:>10.2f}T ${s['vat_p50']/1000:>8.2f}T")
    
    # Risk analysis
    print("\n" + "=" * 80)
    print("RISK ANALYSIS")
    print("=" * 80)
    
    # Year the gap closes (median)
    for s in stats:
        if s["gap_p50"] > 0:
            print(f"\nMedian surplus achieved: Year {s['year']}")
            break
    else:
        print("\nMedian surplus NOT achieved within 10 years")
    
    # Probability of surplus by year
    print("\nProbability of surplus by year:")
    for s in stats:
        bar = "█" * int(s["surplus_probability"] * 50)
        print(f"  Year {s['year']:>2}: {s['surplus_probability']:>5.1%} {bar}")
    
    # Worst-case analysis (P10)
    print("\nWorst-case scenario (10th percentile):")
    worst_gap = stats[-1]["gap_p10"]
    print(f"  Year 10 gap at P10: ${worst_gap/1000:+.2f}T")
    if worst_gap < -3000:
        print(f"  ⚠  Worst case gap exceeds current deficit significantly")
    elif worst_gap < -1300:
        print(f"  ⚠  Worst case gap exceeds current deficit")
    else:
        print(f"  ✓  Worst case gap is within manageable range")
    
    # Best-case analysis (P90)
    print("\nBest-case scenario (90th percentile):")
    for s in stats:
        if s["gap_p90"] > 0:
            print(f"  Surplus possible as early as Year {s['year']} (P90)")
            print(f"  Year 10 surplus at P90: ${s['gap_p90']/1000:+.2f}T" if s == stats[-1] else "")
            break
    
    best_surplus = stats[-1]["gap_p90"]
    print(f"  Year 10 surplus at P90: ${best_surplus/1000:+.2f}T")
    
    # Sensitivity: What drives variance?
    print("\n" + "=" * 80)
    print("SENSITIVITY ANALYSIS — What drives uncertainty?")
    print("=" * 80)
    
    # Compare Year 10 outcomes with high vs low automation
    high_auto = [sim[9]["gap"] for sim in all_results if sim[9]["auto_tax"] > stats[9]["auto_tax_p50"]]
    low_auto = [sim[9]["gap"] for sim in all_results if sim[9]["auto_tax"] <= stats[9]["auto_tax_p50"]]
    
    print(f"\nAutomation tax impact on Year 10 gap:")
    print(f"  High automation (above median): avg gap ${sum(high_auto)/len(high_auto)/1000:+.2f}T")
    print(f"  Low automation (below median):  avg gap ${sum(low_auto)/len(low_auto)/1000:+.2f}T")
    print(f"  Difference: ${(sum(high_auto)/len(high_auto) - sum(low_auto)/len(low_auto))/1000:.2f}T")
    
    high_gdp = [sim[9]["gap"] for sim in all_results if sim[9]["gdp"] > sorted([s[9]["gdp"] for s in all_results])[1000]]
    low_gdp = [sim[9]["gap"] for sim in all_results if sim[9]["gdp"] <= sorted([s[9]["gdp"] for s in all_results])[1000]]
    
    print(f"\nGDP growth impact on Year 10 gap:")
    print(f"  High GDP (above median): avg gap ${sum(high_gdp)/len(high_gdp)/1000:+.2f}T")
    print(f"  Low GDP (below median):  avg gap ${sum(low_gdp)/len(low_gdp)/1000:+.2f}T")
    print(f"  Difference: ${(sum(high_gdp)/len(high_gdp) - sum(low_gdp)/len(low_gdp))/1000:.2f}T")

if __name__ == "__main__":
    main()
