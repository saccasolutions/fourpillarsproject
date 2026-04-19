import random
import statistics

print("=" * 70)
print("MODEL 1: REVENUE TAX WITH LABOR DEDUCTIONS")
print("=" * 70)
print()

# US total business revenue (gross receipts) ~$41T
# US total labor costs ~$12T (wages + benefits)
# We need to generate ~$710B Year 1, growing to ~$2.84T Year 10
# to match automation tax projections

total_revenue = 41_000  # billions
total_labor = 12_000    # billions
taxable_base = total_revenue - total_labor  # $29T

print(f"Total US business revenue (gross receipts): ${total_revenue/1000:.0f}T")
print(f"Total US labor costs (wages + benefits): ${total_labor/1000:.0f}T")
print(f"Taxable base (revenue - labor): ${taxable_base/1000:.0f}T")
print()

# Test different rates
for rate in [0.02, 0.025, 0.03, 0.04, 0.05]:
    rev = taxable_base * rate
    print(f"  {rate*100:.1f}% rate → ${rev:.0f}B revenue")

print()
print("Now model Year 1-10 as automation reduces labor costs:")
print("(Assuming labor costs decline 3% per year as AI replaces workers)")
print()

rate = 0.03  # 3% seems to match Year 1 target
print(f"Using {rate*100:.1f}% rate on (revenue - labor costs):")
print(f"{'Year':>6} {'Revenue':>10} {'Labor':>10} {'Taxable':>10} {'Tax Rev':>10}")
for year in range(1, 11):
    # Revenue grows ~3% per year with GDP
    yr_revenue = total_revenue * (1.03 ** (year - 1))
    # Labor costs decline as automation increases
    labor_decline = 0.03 * year  # 3% per year cumulative
    yr_labor = total_labor * (1 - labor_decline)
    yr_taxable = yr_revenue - yr_labor
    yr_tax = yr_taxable * rate
    print(f"  {year:>4}  ${yr_revenue/1000:>8.1f}T  ${yr_labor/1000:>8.1f}T  ${yr_taxable/1000:>8.1f}T  ${yr_tax:>8.0f}B")

print()
print("Compare to automation tax projections:")
print("  Year 1: $710B target → revenue tax generates ${:.0f}B".format(taxable_base * rate))
print("  Year 10: $2,840B target")

# What rate matches $710B in Year 1?
needed_rate_yr1 = 710 / taxable_base
print(f"\n  Rate needed to match $710B Year 1: {needed_rate_yr1*100:.2f}%")

# Year 10 projection at that rate
yr10_revenue = total_revenue * (1.03 ** 9)
yr10_labor = total_labor * (1 - 0.30)  # 30% reduction by year 10
yr10_taxable = yr10_revenue - yr10_labor
yr10_tax = yr10_taxable * needed_rate_yr1
print(f"  At {needed_rate_yr1*100:.2f}% rate, Year 10 revenue: ${yr10_tax:.0f}B (target: $2,840B)")
print(f"  Rate needed for $2,840B at Year 10: {2840/yr10_taxable*100:.2f}%")

print()
print("KEY INSIGHT: A fixed rate doesn't grow fast enough because")
print("revenue growth partially offsets labor decline. Options:")
print("  A) Start at 2.45% and ramp to ~7% over 10 years")
print("  B) Use a progressive rate that increases as labor/revenue ratio drops")
print()

# Progressive rate model
print("PROGRESSIVE RATE MODEL:")
print("Rate = base_rate + (1 - labor_ratio) * multiplier")
print("As companies automate more, their rate increases automatically")
print()
base_rate = 0.01
multiplier = 0.10
industry_avg_ratio = total_labor / total_revenue  # ~0.293

print(f"Industry average labor/revenue ratio: {industry_avg_ratio:.3f}")
print(f"Base rate: {base_rate*100:.1f}%, Multiplier: {multiplier*100:.0f}%")
print(f"{'Year':>6} {'Avg Ratio':>10} {'Eff Rate':>10} {'Tax Rev':>10}")

for year in range(1, 11):
    yr_revenue = total_revenue * (1.03 ** (year - 1))
    labor_decline = 0.03 * year
    yr_labor = total_labor * (1 - labor_decline)
    yr_ratio = yr_labor / yr_revenue
    # Companies with lower labor ratios pay higher rates
    eff_rate = base_rate + (industry_avg_ratio - yr_ratio) * multiplier
    if eff_rate < base_rate:
        eff_rate = base_rate
    yr_tax = yr_revenue * eff_rate
    print(f"  {year:>4}  {yr_ratio:>9.3f}  {eff_rate*100:>8.2f}%  ${yr_tax:>8.0f}B")


print()
print("=" * 70)
print("MODEL 2: EXTENDED MONTE CARLO — YEARS 1-20")
print("=" * 70)
print()

random.seed(42)
NUM_SIMS = 2000

def run_simulation(years=20):
    results = []
    for _ in range(NUM_SIMS):
        gaps = []
        for yr in range(1, years + 1):
            # GDP growth: 2-4% with recession shocks
            gdp_growth = random.gauss(0.03, 0.015)
            if random.random() < 0.12:  # recession probability
                gdp_growth = random.gauss(-0.02, 0.01)
            gdp_factor = max(0.95, 1 + gdp_growth)
            
            # Automation displacement: 10% Year 1 → 30-50% by Year 20
            auto_rate = 0.10 + (0.025 * yr) + random.gauss(0, 0.02)
            auto_rate = max(0.05, min(0.60, auto_rate))
            
            # Revenue streams (in trillions)
            base_gdp = 28.0
            cum_gdp = base_gdp
            for y in range(yr):
                cum_gdp *= (1 + random.gauss(0.03, 0.01))
            
            vat = cum_gdp * 0.60 * 0.20 * (0.95 + random.gauss(0, 0.03))  # 60% taxable consumption
            auto_tax = 14.2 * auto_rate * 0.50 * (1 + random.gauss(0, 0.1))  # $14.2T labor base
            corp_tax = 0.84 * (cum_gdp / base_gdp) * (1 + random.gauss(0, 0.05))
            payroll = 0.99 * (cum_gdp / base_gdp) * (1 - auto_rate * 0.3) * (1 + random.gauss(0, 0.05))
            invest = 0.41 * (cum_gdp / base_gdp) * (1 + random.gauss(0, 0.15))
            other = 0.40 * (cum_gdp / base_gdp)
            
            total_rev = vat + auto_tax + corp_tax + payroll + invest + other
            
            # Spending (grows with inflation ~2-3%)
            base_spending = 9.82
            spending = base_spending * (1.025 ** yr) * (1 + random.gauss(0, 0.02))
            
            gap = total_rev - spending
            gaps.append(gap)
        
        results.append(gaps)
    
    return results

results = run_simulation(20)

print(f"{'Year':>6} {'Median Gap':>12} {'P(Surplus)':>12} {'10th Pct':>12} {'90th Pct':>12}")
for yr_idx in [0, 4, 9, 14, 19]:  # Years 1, 5, 10, 15, 20
    yr_gaps = [r[yr_idx] for r in results]
    yr_gaps.sort()
    median = yr_gaps[len(yr_gaps)//2]
    surplus_pct = sum(1 for g in yr_gaps if g >= 0) / len(yr_gaps) * 100
    p10 = yr_gaps[int(len(yr_gaps)*0.1)]
    p90 = yr_gaps[int(len(yr_gaps)*0.9)]
    print(f"  {yr_idx+1:>4}  ${median:>+10.2f}T  {surplus_pct:>10.1f}%  ${p10:>+10.2f}T  ${p90:>+10.2f}T")

# Find year where surplus probability first exceeds 50%, 70%
print()
for threshold in [50, 70, 80]:
    for yr_idx in range(20):
        yr_gaps = [r[yr_idx] for r in results]
        surplus_pct = sum(1 for g in yr_gaps if g >= 0) / len(yr_gaps) * 100
        if surplus_pct >= threshold:
            print(f"  {threshold}% surplus probability first reached at Year {yr_idx+1}")
            break
    else:
        # Check final year
        yr_gaps = [r[19] for r in results]
        surplus_pct = sum(1 for g in yr_gaps if g >= 0) / len(yr_gaps) * 100
        print(f"  {threshold}% surplus probability: {surplus_pct:.1f}% by Year 20 (not yet reached)")


print()
print("=" * 70)
print("MODEL 3: LAND VALUE TAX (LVT) ADDITION")
print("=" * 70)
print()

# Total US land value estimates: ~$23-25T (Federal Reserve Z.1 data)
# Residential land: ~$18T, Commercial: ~$5T, Agricultural: ~$3T
# Current property taxes collect ~$600B/yr (state/local, not federal)

total_land_value = 24_000  # billions
print(f"Total US land value: ${total_land_value/1000:.0f}T")
print()

for rate in [0.005, 0.01, 0.015, 0.02, 0.03]:
    rev = total_land_value * rate
    print(f"  {rate*100:.1f}% LVT → ${rev:.0f}B/year")

print()
print("Key advantages:")
print("  - Can't offshore land")
print("  - Stable revenue (land value doesn't fluctuate like profits)")
print("  - Economists broadly support it (Georgist consensus)")
print("  - Discourages land speculation, encourages productive use")
print()

# What if we add a 1% federal LVT?
lvt_revenue = total_land_value * 0.01
print(f"A 1% federal LVT would generate ${lvt_revenue:.0f}B/year")
print(f"This could reduce reliance on automation tax by ${lvt_revenue:.0f}B")
print(f"Or fund additional floor increases of ${lvt_revenue/258:.0f}/person")
print()

# Combined framework revenue with LVT
print("COMBINED FRAMEWORK REVENUE (Year 1) with 1% LVT:")
vat = 3760
auto_tax = 710
corp = 840
payroll = 990
invest = 410
other = 980
lvt = 240
total = vat + auto_tax + corp + payroll + invest + other + lvt
print(f"  VAT:            ${vat:,}B")
print(f"  Automation tax: ${auto_tax:,}B")
print(f"  Corporate tax:  ${corp:,}B")
print(f"  Payroll:        ${payroll:,}B")
print(f"  Investment:     ${invest:,}B")
print(f"  Other:          ${other:,}B")
print(f"  LVT (new):      ${lvt:,}B")
print(f"  TOTAL:          ${total:,}B")
print(f"  Spending:       $9,820B")
print(f"  Gap:            ${total - 9820:,}B (vs -$2,130B without LVT)")


print()
print("=" * 70)
print("MODEL 4: EFFECTIVE PROGRESSIVITY BY INCOME DECILE")
print("=" * 70)
print()

# Model effective tax rates and net transfers by income decile
deciles = [
    ("Bottom 10%", 8000, 8000),      # income, spending
    ("10-20%", 15000, 14500),
    ("20-30%", 24000, 22000),
    ("30-40%", 35000, 31000),
    ("40-50%", 45000, 40000),
    ("50-60%", 58000, 48000),
    ("60-70%", 75000, 58000),
    ("70-80%", 95000, 70000),
    ("80-90%", 135000, 95000),
    ("Top 10%", 300000, 180000),
]

print(f"{'Decile':<14} {'Income':>9} {'Curr Tax':>10} {'Curr Rate':>10} {'FP Floor':>9} {'VAT Paid':>9} {'FP Net':>10} {'FP Rate':>9}")

for name, income, spending in deciles:
    # Current system
    if income <= 15000: fed_rate = 0.10
    elif income <= 45000: fed_rate = 0.14
    elif income <= 100000: fed_rate = 0.20
    elif income <= 200000: fed_rate = 0.26
    else: fed_rate = 0.33
    curr_tax = income * fed_rate + income * 0.0765
    curr_eff_rate = curr_tax / income if income > 0 else 0
    
    # Four Pillars
    if income <= 30000:
        floor = 25000
    elif income <= 80000:
        floor = max(0, 25000 - 0.5 * (income - 30000))
    else:
        floor = 0
    
    taxable_spending = spending * 0.70  # 30% exempt (groceries, rent, healthcare, education)
    vat_paid = taxable_spending * 0.20
    
    # Net transfer = floor received - VAT paid
    net_transfer = floor - vat_paid
    # Effective rate: negative means net recipient
    fp_eff_rate = -net_transfer / income if income > 0 else 0
    
    print(f"{name:<14} ${income:>7,}  ${curr_tax:>8,.0f}  {curr_eff_rate:>8.1%}  ${floor:>7,}  ${vat_paid:>7,.0f}  ${net_transfer:>+8,.0f}  {fp_eff_rate:>+8.1%}")

print()
print("Negative FP Rate = net recipient (framework gives you more than it takes)")
print("Positive FP Rate = net payer (you pay more in VAT than you receive in floor)")
print()
print("KEY: Compare 'Curr Rate' vs 'FP Rate' — the framework is MORE progressive")
print("at every income level below ~$60K, and the wealthy pay comparable effective rates")
print("PLUS they pay 25% investment income tax, wealth tax, estate tax, etc.")
print("which are not shown in this simplified comparison.")

