"""
Extended Monte Carlo — uses the ORIGINAL model parameters but runs 20 years
"""
import random
import math

random.seed(42)
NUM_SIMULATIONS = 2_000
YEARS = 20

BASE_GDP = 29_000
BASE_REVENUE = {
    "VAT": 3_760, "Employer_FICA": 990, "Corporate_Tax": 840,
    "Automation_Tax": 710, "Investment_Income_Tax": 410,
    "Excise_Tariffs": 300, "FTT": 200, "Corp_Minimum_Tax": 130,
    "Wealth_Tax": 100, "Employer_Penalty": 80, "Estate_Tax": 80,
    "Digital_Ad_Tax": 60, "Buyback_Tax": 40,
}
BASE_OUTFLOWS = {
    "Floor_Payments": 4_620, "Pillar_2_4": 800,
    "Healthcare_Gaps": 1_550, "Admin": 50, "Federal_Ops": 2_800,
}
TOTAL_BASE_REVENUE = sum(BASE_REVENUE.values())
TOTAL_BASE_OUTFLOWS = sum(BASE_OUTFLOWS.values())

GROWTH_PARAMS = {
    "gdp_growth": (0.028, 0.015),
    "vat_gdp_elasticity": (1.05, 0.10),
    "auto_displacement_yr1": (0.10, 0.02),
    "auto_displacement_yr10": (0.30, 0.08),
    "investment_income_growth": (0.04, 0.06),
    "corp_profit_growth": (0.03, 0.02),
    "healthcare_inflation": (0.04, 0.01),
    "federal_ops_growth": (0.025, 0.01),
}

def run_simulation():
    gdp_growth_base = random.gauss(*GROWTH_PARAMS["gdp_growth"])
    vat_elasticity = random.gauss(*GROWTH_PARAMS["vat_gdp_elasticity"])
    auto_start = max(0.05, random.gauss(*GROWTH_PARAMS["auto_displacement_yr1"]))
    auto_end = max(auto_start + 0.05, random.gauss(*GROWTH_PARAMS["auto_displacement_yr10"]))
    inv_growth = random.gauss(*GROWTH_PARAMS["investment_income_growth"])
    corp_growth = random.gauss(*GROWTH_PARAMS["corp_profit_growth"])
    health_infl = max(0.02, random.gauss(*GROWTH_PARAMS["healthcare_inflation"]))
    fed_growth = random.gauss(*GROWTH_PARAMS["federal_ops_growth"])
    
    # For years beyond 10, extrapolate automation displacement
    auto_yr20 = min(0.60, auto_end + (auto_end - auto_start))  # continues growing but caps at 60%
    
    yearly_results = []
    gdp = BASE_GDP
    
    for year in range(1, YEARS + 1):
        year_gdp_shock = random.gauss(0, 0.008)
        gdp_rate = gdp_growth_base + year_gdp_shock
        
        if random.random() < 0.12:
            gdp_rate = random.gauss(-0.015, 0.01)
        
        gdp = gdp * (1 + gdp_rate)
        gdp_factor = gdp / BASE_GDP
        
        # Revenue
        ubi_spending_boost = 1.0 + 0.02 * min(year, 5)
        vat = BASE_REVENUE["VAT"] * gdp_factor * vat_elasticity * ubi_spending_boost
        
        wage_growth = gdp_rate * 0.6 + 0.01
        fica_factor = (1 + wage_growth) ** year
        employer_fica = BASE_REVENUE["Employer_FICA"] * fica_factor
        
        corp_factor = (1 + corp_growth + random.gauss(0, 0.03)) ** year
        corp_tax = BASE_REVENUE["Corporate_Tax"] * max(0.5, corp_factor)
        
        # Automation displacement — interpolate through 3 points
        if year <= 10:
            displacement = auto_start + (auto_end - auto_start) * (year / 10)
        else:
            displacement = auto_end + (auto_yr20 - auto_end) * ((year - 10) / 10)
        
        labor_cost_basis = 9_200 * gdp_factor
        auto_savings = labor_cost_basis * displacement
        auto_tax = auto_savings * 0.50
        
        inv_factor = (1 + inv_growth + random.gauss(0, 0.08)) ** year
        inv_tax = BASE_REVENUE["Investment_Income_Tax"] * max(0.3, inv_factor)
        
        excise = BASE_REVENUE["Excise_Tariffs"] * gdp_factor
        ftt = BASE_REVENUE["FTT"] * gdp_factor * (1 + 0.02 * year)
        corp_min = BASE_REVENUE["Corp_Minimum_Tax"] * max(0.5, corp_factor)
        wealth = BASE_REVENUE["Wealth_Tax"] * (1 + 0.05) ** year
        employer_pen = BASE_REVENUE["Employer_Penalty"] * (0.9 ** year)
        estate = BASE_REVENUE["Estate_Tax"] * (1 + 0.03) ** year
        digital = BASE_REVENUE["Digital_Ad_Tax"] * (1 + 0.08) ** year
        buyback = BASE_REVENUE["Buyback_Tax"] * gdp_factor
        
        total_revenue = (vat + employer_fica + corp_tax + auto_tax + inv_tax +
                        excise + ftt + corp_min + wealth + employer_pen +
                        estate + digital + buyback)
        
        # Outflows
        floor = BASE_OUTFLOWS["Floor_Payments"]
        pillar24 = BASE_OUTFLOWS["Pillar_2_4"] * (1 + 0.02) ** year
        healthcare = BASE_OUTFLOWS["Healthcare_Gaps"] * (1 + health_infl) ** year
        admin = BASE_OUTFLOWS["Admin"] * (1 + 0.02) ** year
        federal_ops = BASE_OUTFLOWS["Federal_Ops"] * (1 + fed_growth) ** year
        
        total_outflows = floor + pillar24 + healthcare + admin + federal_ops
        gap = total_revenue - total_outflows
        
        yearly_results.append({
            "year": year, "gap": gap,
            "total_revenue": total_revenue,
            "total_outflows": total_outflows,
            "auto_tax": auto_tax, "vat": vat,
            "displacement": displacement, "gdp": gdp,
        })
    
    return yearly_results

# Run simulations
print("Running {} simulations over {} years...".format(NUM_SIMULATIONS, YEARS))
all_results = []
for _ in range(NUM_SIMULATIONS):
    all_results.append(run_simulation())

# Results for every year
print()
print(f"{'Year':>4} {'Rev P50':>9} {'Out P50':>9} {'Gap P50':>10} {'Gap P10':>10} {'Gap P90':>10} {'P(Surp)':>9} {'AutoTax':>9} {'VAT':>9}")
print("-" * 95)

for yr in range(YEARS):
    gaps = sorted([sim[yr]["gap"] for sim in all_results])
    revs = sorted([sim[yr]["total_revenue"] for sim in all_results])
    outs = sorted([sim[yr]["total_outflows"] for sim in all_results])
    autos = sorted([sim[yr]["auto_tax"] for sim in all_results])
    vats = sorted([sim[yr]["vat"] for sim in all_results])
    
    n = len(gaps)
    p50 = gaps[n//2]
    p10 = gaps[int(n*0.1)]
    p90 = gaps[int(n*0.9)]
    surplus = sum(1 for g in gaps if g > 0) / n
    
    print(f"  {yr+1:>2}  ${revs[n//2]/1000:>7.2f}T ${outs[n//2]/1000:>7.2f}T ${p50/1000:>+8.2f}T ${p10/1000:>+8.2f}T ${p90/1000:>+8.2f}T {surplus:>8.1%} ${autos[n//2]/1000:>7.2f}T ${vats[n//2]/1000:>7.2f}T")

# Milestone table
print()
print("MILESTONE ANALYSIS:")
for threshold in [25, 34, 50, 70, 80, 90]:
    for yr in range(YEARS):
        gaps = [sim[yr]["gap"] for sim in all_results]
        surplus = sum(1 for g in gaps if g > 0) / len(gaps) * 100
        if surplus >= threshold:
            print(f"  {threshold}% surplus probability reached at Year {yr+1}")
            break
    else:
        gaps = [sim[YEARS-1]["gap"] for sim in all_results]
        final = sum(1 for g in gaps if g > 0) / len(gaps) * 100
        print(f"  {threshold}% surplus probability: NOT reached (final: {final:.1f}% at Year {YEARS})")

# What if we add LVT?
print()
print("=" * 70)
print("SCENARIO: ADD 1% LAND VALUE TAX ($240B/yr, growing 2%/yr)")
print("=" * 70)
print()
print(f"{'Year':>4} {'Gap w/o LVT':>12} {'LVT Rev':>9} {'Gap w/ LVT':>12} {'P(Surp)':>9}")
print("-" * 55)

for yr in range(YEARS):
    gaps = sorted([sim[yr]["gap"] for sim in all_results])
    lvt = 240 * (1.02 ** yr)  # land values grow ~2%/yr
    gaps_with_lvt = sorted([sim[yr]["gap"] + lvt for sim in all_results])
    
    n = len(gaps)
    p50_base = gaps[n//2]
    p50_lvt = gaps_with_lvt[n//2]
    surplus_lvt = sum(1 for g in gaps_with_lvt if g > 0) / n
    
    print(f"  {yr+1:>2}  ${p50_base/1000:>+10.2f}T ${lvt:>7.0f}B ${p50_lvt/1000:>+10.2f}T {surplus_lvt:>8.1%}")

# LVT milestones
print()
print("WITH LVT — MILESTONES:")
for threshold in [25, 34, 50, 70, 80]:
    for yr in range(YEARS):
        lvt = 240 * (1.02 ** yr)
        gaps = [sim[yr]["gap"] + lvt for sim in all_results]
        surplus = sum(1 for g in gaps if g > 0) / len(gaps) * 100
        if surplus >= threshold:
            print(f"  {threshold}% surplus probability reached at Year {yr+1}")
            break
    else:
        gaps = [sim[YEARS-1]["gap"] + 240 * (1.02 ** (YEARS-1)) for sim in all_results]
        final = sum(1 for g in gaps if g > 0) / len(gaps) * 100
        print(f"  {threshold}% surplus probability: NOT reached (final: {final:.1f}% at Year {YEARS})")

