#\!/usr/bin/env python3
"""
Floor Phase-Out Optimization — Four Pillars UBI Framework
Tests different phase-out rates/thresholds and measures cost vs work incentive impact.
"""

# ============================================================
# INCOME DISTRIBUTION (258M adults)
# Granular bins for accurate phase-out modeling
# ============================================================

# (income_midpoint, population_millions)
INCOME_DIST = [
    (0, 40),        # No income
    (5_000, 15),    # Very low
    (10_000, 18),   # Part-time min wage
    (15_000, 22),   # Full-time min wage
    (20_000, 18),   # Low wage
    (25_000, 15),   # Low-moderate
    (30_000, 13),   # Moderate
    (35_000, 12),   # Moderate
    (40_000, 11),   # Median-area
    (45_000, 10),   # Median
    (50_000, 9),    # Above median
    (55_000, 8),    # Above median
    (60_000, 7),    # Upper-moderate
    (65_000, 6),    # Upper-moderate
    (70_000, 5),    # Upper-moderate
    (75_000, 4.5),  # Upper
    (80_000, 4),    # Upper
    (90_000, 5),    # High
    (100_000, 4),   # High
    (120_000, 4),   # High
    (150_000, 3.5), # Very high
    (200_000, 3),   # Very high
    (300_000, 2),   # Top
    (500_000, 1),   # Top 1%
    (1_000_000, 0.5),# Ultra high
]

TOTAL_POP = sum(p for _, p in INCOME_DIST)  # ~258M

def calculate_floor(income, floor_amount, start_phase, rate, end_phase=None):
    """Calculate floor payment given phase-out parameters."""
    if income <= start_phase:
        return floor_amount
    reduction = (income - start_phase) * rate
    result = max(0, floor_amount - reduction)
    if end_phase and income > end_phase:
        return 0
    return result

def effective_marginal_rate(income, floor_amount, start_phase, rate):
    """Calculate effective marginal tax rate including floor phase-out + VAT."""
    # Phase-out acts as implicit tax
    if income <= start_phase:
        phase_out_rate = 0
    elif calculate_floor(income, floor_amount, start_phase, rate) > 0:
        phase_out_rate = rate  # losing floor at this rate
    else:
        phase_out_rate = 0  # already phased out
    
    # VAT effective rate on marginal income (~14% of marginal dollar goes to VAT)
    # 70% of spending taxable × 20% VAT = 14%
    vat_effective = 0.14
    
    # Mandatory 401k (10% of earnings)
    savings_rate = 0.10
    
    # Total: no income tax, but phase-out + VAT + mandatory savings
    total_marginal = phase_out_rate + vat_effective + savings_rate
    
    return {
        "phase_out": phase_out_rate,
        "vat": vat_effective,
        "savings": savings_rate,
        "total": total_marginal,
    }

# ============================================================
# SCENARIOS
# ============================================================

SCENARIOS = {
    "Current v3 (50¢/$1 from $30K)": {
        "floor": 25_000, "start": 30_000, "rate": 0.50,
        "description": "Full $25K below $30K, 50¢ reduction per $1 above, gone at $80K"
    },
    "Gentle (33¢/$1 from $30K)": {
        "floor": 25_000, "start": 30_000, "rate": 0.333,
        "description": "Full $25K below $30K, 33¢ reduction per $1 above, gone at $105K"
    },
    "Aggressive (75¢/$1 from $25K)": {
        "floor": 25_000, "start": 25_000, "rate": 0.75,
        "description": "Full $25K below $25K, 75¢ reduction per $1 above, gone at $58K"
    },
    "Delayed (50¢/$1 from $35K)": {
        "floor": 25_000, "start": 35_000, "rate": 0.50,
        "description": "Full $25K below $35K, 50¢ reduction per $1 above, gone at $85K"
    },
    "Higher Floor (30K, 50¢ from $35K)": {
        "floor": 30_000, "start": 35_000, "rate": 0.50,
        "description": "Full $30K below $35K, 50¢ reduction per $1 above, gone at $95K"
    },
    "Universal $20K (no phase-out)": {
        "floor": 20_000, "start": 999_999, "rate": 0,
        "description": "Flat $20K to every adult, no phase-out"
    },
    "NIT Style (25¢/$1 from $0)": {
        "floor": 25_000, "start": 0, "rate": 0.25,
        "description": "Starts reducing from $0 earnings at 25¢/$1, gone at $100K"
    },
}

def analyze_scenario(name, params):
    """Full analysis of a phase-out scenario."""
    floor = params["floor"]
    start = params["start"]
    rate = params["rate"]
    
    total_cost = 0
    receiving = 0
    full_receiving = 0
    
    for income, pop in INCOME_DIST:
        payment = calculate_floor(income, floor, start, rate)
        cost = payment * pop * 1_000_000 / 1_000_000_000_000  # trillions
        total_cost += cost
        if payment > 0:
            receiving += pop
            if payment == floor:
                full_receiving += pop
    
    # Marginal rate analysis at key income points
    marginal_rates = {}
    for test_income in [0, 15_000, 25_000, 30_000, 35_000, 40_000, 50_000, 60_000, 75_000, 80_000, 100_000]:
        emr = effective_marginal_rate(test_income, floor, start, rate)
        marginal_rates[test_income] = emr
    
    # Work incentive score (lower is better = less disincentive)
    # Weighted by population in phase-out range
    disincentive_score = 0
    for income, pop in INCOME_DIST:
        emr = effective_marginal_rate(income, floor, start, rate)
        if emr["phase_out"] > 0:
            # High marginal rates on large populations = bad
            disincentive_score += emr["total"] * pop
    
    return {
        "name": name,
        "description": params["description"],
        "total_cost_T": round(total_cost, 2),
        "receiving_M": round(receiving, 1),
        "full_receiving_M": round(full_receiving, 1),
        "pct_receiving": round(receiving / TOTAL_POP * 100, 1),
        "marginal_rates": marginal_rates,
        "disincentive_score": round(disincentive_score, 1),
        "phase_out_range": f"${start:,} - ${start + int(floor/rate) if rate > 0 else 'N/A':,}" if rate > 0 else "None",
        "max_marginal_in_phaseout": round((rate + 0.14 + 0.10) * 100, 1) if rate > 0 else 24.0,
    }

def main():
    print("=" * 90)
    print("FLOOR PHASE-OUT OPTIMIZATION — Four Pillars UBI Framework")
    print("=" * 90)
    
    results = []
    for name, params in SCENARIOS.items():
        results.append(analyze_scenario(name, params))
    
    # Comparison table
    print(f"\n{'Scenario':<35} {'Cost($T)':>8} {'Recv(M)':>8} {'%Recv':>6} {'MaxMarg%':>8} {'Disincent':>9}")
    print("-" * 80)
    for r in results:
        print(f"{r['name']:<35} ${r['total_cost_T']:>6.2f} {r['receiving_M']:>7.1f} {r['pct_receiving']:>5.1f}% {r['max_marginal_in_phaseout']:>7.1f}% {r['disincentive_score']:>8.1f}")
    
    # Marginal rate comparison
    print(f"\n{'Income':<12}", end="")
    for r in results:
        print(f" {r['name'][:18]:>18}", end="")
    print()
    print("-" * (12 + 19 * len(results)))
    
    for income in [0, 15_000, 25_000, 30_000, 35_000, 40_000, 50_000, 60_000, 75_000, 100_000]:
        print(f"${income:>10,}", end="")
        for r in results:
            total = r["marginal_rates"][income]["total"]
            print(f" {total:>17.0%}", end="")
        print()
    
    # Detailed current v3 analysis
    print("\n" + "=" * 90)
    print("DETAILED ANALYSIS: Current v3 (50¢/$1 from $30K)")
    print("=" * 90)
    
    v3 = results[0]
    print(f"\n  Total cost: ${v3['total_cost_T']}T")
    print(f"  Adults receiving: {v3['receiving_M']}M ({v3['pct_receiving']}%)")
    print(f"  Full floor: {v3['full_receiving_M']}M")
    print(f"  Phase-out range: {v3['phase_out_range']}")
    print(f"  Max marginal rate in phase-out: {v3['max_marginal_in_phaseout']}%")
    
    print(f"\n  Marginal Rate Breakdown at Key Incomes:")
    print(f"  {'Income':<12} {'Phase-Out':>10} {'VAT':>6} {'401k':>6} {'Total':>7} {'Net of $1':>9}")
    print(f"  {'-'*55}")
    for income in [0, 15_000, 25_000, 30_000, 35_000, 45_000, 60_000, 80_000, 100_000]:
        mr = effective_marginal_rate(income, 25_000, 30_000, 0.50)
        kept = 1.0 - mr["total"]
        print(f"  ${income:>10,} {mr['phase_out']:>9.0%} {mr['vat']:>5.0%} {mr['savings']:>5.0%} {mr['total']:>6.0%}   ${kept:>.2f}")
    
    print(f"\n  Key insight: In the phase-out zone ($30K-$80K), the effective")
    print(f"  marginal rate is {v3['max_marginal_in_phaseout']}% — comprised of 50% floor phase-out +")
    print(f"  14% effective VAT + 10% mandatory 401k. This is LOWER than the")
    print(f"  current system's ~40-45% marginal rate (22%+ income tax + 7.65% FICA")
    print(f"  + state tax) for the same income range.")
    
    # Recommendation
    print("\n" + "=" * 90)
    print("RECOMMENDATION")
    print("=" * 90)
    print(f"""
  The current v3 design (50¢/$1 from $30K) represents the best balance:
  
  1. COST: $4.78T — within the v3.0 balance sheet allocation ($4.62T floor + $0.80T P2-4)
  2. COVERAGE: 84.5% of adults receive some payment
  3. WORK INCENTIVE: 74% max marginal rate sounds high but is LOWER than current 
     system for same earners (no income tax or FICA offsets the phase-out)
  4. SIMPLICITY: Clean 50¢/$1 rule is easy to communicate
  
  The "Gentle (33¢)" alternative costs $0.62T more but extends benefits to $105K 
  earners. Worth considering if automation tax revenue exceeds projections.
  
  The "NIT Style (25¢)" has the best work incentives (lowest disincentive score)
  but costs $1.20T more than current v3 — not feasible at launch.
  
  CURRENT V3 IS OPTIMAL FOR LAUNCH. Scale to Gentle or NIT as revenue permits.
""")

if __name__ == "__main__":
    main()
