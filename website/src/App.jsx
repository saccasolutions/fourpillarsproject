import { useState, useEffect, useRef } from "react";
import { DollarSign, Users, TrendingUp, Shield, ChevronDown, ChevronRight, ArrowRight, Calculator, BookOpen, Github, FileText, BarChart3, Heart, Palette, Building2, Home, ExternalLink } from "lucide-react";

// ─── Utility ───
const fmt = (n) => {
  if (Math.abs(n) >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
  if (Math.abs(n) >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  return n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
};

// ─── Calculator Logic ───
function calculate(income, filingStatus, numChildren, hasEmployerInsurance, creativeTier, civicTier) {
  const adults = filingStatus === "married" ? 2 : 1;

  // Current system
  let fedTaxRate;
  if (income <= 15000) fedTaxRate = 0.10;
  else if (income <= 45000) fedTaxRate = 0.14;
  else if (income <= 100000) fedTaxRate = 0.20;
  else if (income <= 200000) fedTaxRate = 0.26;
  else fedTaxRate = 0.33;
  const currentFedTax = income * fedTaxRate;
  const currentFICA = income * 0.0765;
  const currentTakeHome = income - currentFedTax - currentFICA;

  // Four Pillars
  const perAdultIncome = income / adults;
  let totalFloor = 0;
  for (let i = 0; i < adults; i++) {
    if (perAdultIncome <= 30000) totalFloor += 25000;
    else if (perAdultIncome <= 80000) totalFloor += Math.max(0, 25000 - 0.5 * (perAdultIncome - 30000));
  }

  const childPillar4 = numChildren >= 3 ? 15000 : numChildren >= 2 ? 10000 : numChildren === 1 ? 6000 : 0;

  // Pillar 2 — Creative
  const creativePillar = creativeTier === "emerging" ? 3000 : creativeTier === "active" ? 8000 : creativeTier === "professional" ? 15000 : 0;

  // Pillar 3 — Civic
  const civicPillar = civicTier === "participating" ? 2500 : civicTier === "active" ? 8000 : civicTier === "leader" ? 14000 : 0;

  const gross = income + totalFloor + childPillar4 + creativePillar + civicPillar;
  const mandatory401k = income * 0.10;
  const spending = gross - mandatory401k;
  const taxableSpending = spending * 0.70;
  const vatPaid = taxableSpending * 0.20;
  const netNew = gross - vatPaid;

  // Retirement projection (30 years, 7%)
  let retireBalance = 0;
  const annualContrib = mandatory401k;
  for (let y = 0; y < 30; y++) {
    retireBalance = (retireBalance + annualContrib * 1.02 ** y) * 1.07;
  }
  const retireIncome = retireBalance * 0.04 + 25000; // 4% rule + floor

  // Healthcare
  const healthcareNote = hasEmployerInsurance
    ? "Your employer insurance continues as-is."
    : "You qualify for government healthcare gap coverage at no cost.";

  return {
    current: { fedTax: currentFedTax, fica: currentFICA, takeHome: currentTakeHome },
    fourPillars: {
      floor: totalFloor,
      childPillar4,
      creativePillar,
      civicPillar,
      gross,
      mandatory401k,
      vatPaid,
      net: netNew,
      change: netNew - currentTakeHome,
      changePct: currentTakeHome > 0 ? ((netNew - currentTakeHome) / currentTakeHome) * 100 : 999,
      retireBalance,
      retireIncome,
      healthcareNote,
    },
  };
}

// ─── Components ───

function HeroSection({ onCalculatorClick }) {
  return (
    <div className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-6 py-16 pb-8">
        <div className="text-center max-w-4xl mx-auto mb-12">
          <h1 className="text-4xl md:text-5xl font-bold leading-tight mb-6">
            The Four Pillars Project
          </h1>
          <p className="text-xl md:text-2xl text-blue-200 font-light max-w-3xl mx-auto">
            A complete economic framework that values every kind of contribution — not just a paycheck.
          </p>
        </div>

        {/* The Four Pillars — front and center */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-white/10 backdrop-blur rounded-xl p-5 text-center border border-blue-400/20">
            <Building2 className="w-8 h-8 text-blue-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-white mb-1">Economic</h3>
            <p className="text-sm text-blue-200">Your salary — tax free. Keep 100% of your paycheck.</p>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-xl p-5 text-center border border-purple-400/20">
            <Palette className="w-8 h-8 text-purple-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-white mb-1">Creative</h3>
            <p className="text-sm text-purple-200">Arts, music, writing, innovation. $3K–$15K/year.</p>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-xl p-5 text-center border border-green-400/20">
            <Users className="w-8 h-8 text-green-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-white mb-1">Civic</h3>
            <p className="text-sm text-green-200">Volunteering, mentoring, community. $2.5K–$14K/year.</p>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-xl p-5 text-center border border-rose-400/20">
            <Heart className="w-8 h-8 text-rose-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-white mb-1">Family</h3>
            <p className="text-sm text-rose-200">Raising kids, caregiving. $6K–$15K/year.</p>
          </div>
        </div>

        {/* The problem + what it does */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div className="bg-white/5 rounded-xl p-6 border border-slate-700">
            <p className="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">The Problem</p>
            <p className="text-slate-300 leading-relaxed">
              84% of federal revenue comes from taxing human labor. AI is replacing that labor. Social Security hits insolvency by 2033. The current system has no fix.
            </p>
          </div>
          <div className="bg-white/5 rounded-xl p-6 border border-slate-700">
            <p className="text-xs font-semibold text-green-400 uppercase tracking-wide mb-2">The Framework</p>
            <p className="text-slate-300 leading-relaxed">
              Eliminate income tax. Tax automation instead. A $25K floor plus pillar payments — a median worker takes home <span className="text-white font-semibold">$55,500</span> vs $34,050 today. Open source, Monte Carlo validated.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-4 justify-center">
          <button
            onClick={onCalculatorClick}
            className="bg-blue-500 hover:bg-blue-400 text-white px-8 py-4 rounded-lg text-lg font-semibold flex items-center gap-2 transition-colors"
          >
            <Calculator className="w-5 h-5" />
            What does this mean for me?
          </button>
          <a
            href="https://github.com/saccasolutions/fourpillarsproject"
            target="_blank"
            rel="noopener noreferrer"
            className="border border-slate-500 hover:border-slate-300 text-slate-200 px-8 py-4 rounded-lg text-lg font-semibold flex items-center gap-2 transition-colors"
          >
            <BookOpen className="w-5 h-5" />
            Read the Whitepaper
          </a>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, value, label, sub }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-3 mb-3">
        <div className="bg-blue-50 p-2 rounded-lg">
          <Icon className="w-5 h-5 text-blue-600" />
        </div>
        <span className="text-sm font-medium text-slate-500">{label}</span>
      </div>
      <p className="text-3xl font-bold text-slate-900">{value}</p>
      {sub && <p className="text-sm text-slate-500 mt-1">{sub}</p>}
    </div>
  );
}

function StatsRow() {
  return (
    <div className="bg-slate-50 border-y border-slate-200">
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard icon={DollarSign} value="$25,000" label="Income Floor" sub="Per adult, per year" />
          <StatCard icon={Users} value="0%" label="Income Tax" sub="Keep 100% of your paycheck" />
          <StatCard icon={TrendingUp} value="56%" label="Surplus by Yr 10" sub="Monte Carlo probability" />
          <StatCard icon={Shield} value="$1.2M+" label="Retirement" sub="Min wage worker, age 65" />
        </div>
      </div>
    </div>
  );
}

function PillarCard({ icon: Icon, title, description, color }) {
  const colorClasses = {
    blue: "bg-blue-50 text-blue-600 border-blue-200",
    purple: "bg-purple-50 text-purple-600 border-purple-200",
    green: "bg-green-50 text-green-600 border-green-200",
    rose: "bg-rose-50 text-rose-600 border-rose-200",
  };
  return (
    <div className={`rounded-xl border-2 p-6 ${colorClasses[color]}`}>
      <Icon className="w-8 h-8 mb-4" />
      <h3 className="text-xl font-bold text-slate-900 mb-2">{title}</h3>
      <p className="text-slate-600 leading-relaxed">{description}</p>
    </div>
  );
}

function PillarsSection() {
  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-slate-900 mb-3">How the Pillars Stack Up</h2>
      <p className="text-lg text-slate-500 mb-4 max-w-3xl">
        The $25K floor is just the foundation. Pillar payments stack on top of your tax-free earnings. Here's what real scenarios look like:
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className="bg-blue-50 rounded-xl p-6 border border-blue-200">
          <p className="text-sm font-semibold text-blue-600 mb-2">Stay-at-home parent, 2 kids, volunteers weekends</p>
          <div className="space-y-1 text-sm text-slate-600">
            <p>Floor: <span className="font-semibold text-green-700">+$25,000</span></p>
            <p>Family (Pillar 4): <span className="font-semibold text-green-700">+$10,000</span></p>
            <p>Civic (Pillar 3): <span className="font-semibold text-green-700">+$2,500</span></p>
          </div>
          <p className="text-xl font-bold text-slate-900 mt-3 pt-3 border-t border-blue-200">$37,500/year</p>
          <p className="text-xs text-slate-500">Current system: $0</p>
        </div>
        <div className="bg-green-50 rounded-xl p-6 border border-green-200">
          <p className="text-sm font-semibold text-green-600 mb-2">Median worker ($45K), coaches little league</p>
          <div className="space-y-1 text-sm text-slate-600">
            <p>Salary (no tax): <span className="font-semibold">$45,000</span></p>
            <p>Floor: <span className="font-semibold text-green-700">+$17,500</span></p>
            <p>Civic (Pillar 3): <span className="font-semibold text-green-700">+$2,500</span></p>
            <p>VAT: <span className="font-semibold text-red-600">−$7,700</span></p>
          </div>
          <p className="text-xl font-bold text-slate-900 mt-3 pt-3 border-t border-green-200">$57,300/year</p>
          <p className="text-xs text-slate-500">Current system: $34,050</p>
        </div>
        <div className="bg-purple-50 rounded-xl p-6 border border-purple-200">
          <p className="text-sm font-semibold text-purple-600 mb-2">Freelance artist ($20K), active creator</p>
          <div className="space-y-1 text-sm text-slate-600">
            <p>Salary (no tax): <span className="font-semibold">$20,000</span></p>
            <p>Floor: <span className="font-semibold text-green-700">+$25,000</span></p>
            <p>Creative (Pillar 2): <span className="font-semibold text-green-700">+$8,000</span></p>
            <p>VAT: <span className="font-semibold text-red-600">−$5,180</span></p>
          </div>
          <p className="text-xl font-bold text-slate-900 mt-3 pt-3 border-t border-purple-200">$47,820/year</p>
          <p className="text-xs text-slate-500">Current system: $15,530</p>
        </div>
      </div>
      <p className="text-sm text-slate-500 text-center">Use the calculator above to see your personal scenario with all four pillars.</p>
    </div>
  );
}

function ComparisonTable() {
  const rows = [
    ["Total federal spending", "$6.4T", "$9.82T"],
    ["Total federal revenue", "$5.1T", "$7.69T"],
    ["Deficit / gap", "$1.3T", "$2.13T"],
    ["Path to balance", "None", "Year 7\u201310"],
    ["Company share of revenue", "16%", "37%"],
    ["Your income tax rate", "10\u201337%", "0%"],
    ["Your FICA deduction", "7.65%", "0%"],
  ];
  return (
    <div className="bg-slate-900 text-white">
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold mb-3">The Numbers</h2>
        <p className="text-slate-400 mb-10 max-w-2xl text-lg">
          Real math, not hand-waving. Every dollar accounted for.
        </p>
        <div className="overflow-x-auto">
          <table className="w-full max-w-2xl">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-3 pr-8 text-slate-400 font-medium"></th>
                <th className="text-right py-3 px-4 text-slate-400 font-medium">Current</th>
                <th className="text-right py-3 pl-4 text-blue-400 font-medium">Four Pillars</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(([label, current, fp], i) => (
                <tr key={i} className="border-b border-slate-800">
                  <td className="py-3 pr-8 text-slate-300">{label}</td>
                  <td className="py-3 px-4 text-right text-slate-400">{current}</td>
                  <td className="py-3 pl-4 text-right text-white font-semibold">{fp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-slate-500 mt-8 text-sm max-w-2xl">
          The $830B additional gap closes through automation tax growth ($0.71T → $2.84T over 10 years)
          and GDP expansion from consumer spending. Monte Carlo simulation: 56% probability of surplus by Year 10, 80% by Year 20,
          90th percentile surplus by Year 6.
        </p>
      </div>
    </div>
  );
}

function CalculatorSection({ calculatorRef }) {
  const [income, setIncome] = useState(45000);
  const [filing, setFiling] = useState("single");
  const [children, setChildren] = useState(0);
  const [insured, setInsured] = useState(true);
  const [creativeTier, setCreativeTier] = useState("none");
  const [civicTier, setCivicTier] = useState("none");
  const [showDetails, setShowDetails] = useState(false);

  const result = calculate(income, filing, children, insured, creativeTier, civicTier);
  const r = result.fourPillars;
  const c = result.current;

  return (
    <div ref={calculatorRef} className="bg-white border-y border-slate-200">
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-slate-900 mb-3">What Does This Mean For You?</h2>
        <p className="text-lg text-slate-500 mb-10">Enter your details to see your personal impact.</p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Inputs */}
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Annual Household Income</label>
              <input
                type="range"
                min={0}
                max={300000}
                step={1000}
                value={income}
                onChange={(e) => setIncome(Number(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between mt-2">
                <span className="text-2xl font-bold text-slate-900">{fmt(income)}</span>
                <span className="text-sm text-slate-400">$0 — $300K</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Filing Status</label>
                <select
                  value={filing}
                  onChange={(e) => setFiling(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 bg-white"
                >
                  <option value="single">Single</option>
                  <option value="married">Married</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Children</label>
                <select
                  value={children}
                  onChange={(e) => setChildren(Number(e.target.value))}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 bg-white"
                >
                  {[0, 1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={insured}
                  onChange={(e) => setInsured(e.target.checked)}
                  className="w-5 h-5 rounded border-slate-300 text-blue-600"
                />
                <span className="text-sm text-slate-700">I have employer-provided health insurance</span>
              </label>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Creative Work</label>
                <select
                  value={creativeTier}
                  onChange={(e) => setCreativeTier(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 bg-white text-sm"
                >
                  <option value="none">None</option>
                  <option value="emerging">Emerging ($3K/yr)</option>
                  <option value="active">Active ($8K/yr)</option>
                  <option value="professional">Professional ($15K/yr)</option>
                </select>
                <p className="text-xs text-slate-400 mt-1">Arts, music, writing, innovation</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Civic Contribution</label>
                <select
                  value={civicTier}
                  onChange={(e) => setCivicTier(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 bg-white text-sm"
                >
                  <option value="none">None</option>
                  <option value="participating">Participating ($2.5K/yr)</option>
                  <option value="active">Active ($8K/yr)</option>
                  <option value="leader">Leader ($14K/yr)</option>
                </select>
                <p className="text-xs text-slate-400 mt-1">Volunteering, mentoring, community service</p>
              </div>
            </div>
          </div>

          {/* Results */}
          <div className="space-y-6">
            {/* Big result */}
            <div className={`rounded-xl p-6 ${r.change >= 0 ? "bg-green-50 border-2 border-green-200" : "bg-red-50 border-2 border-red-200"}`}>
              <p className="text-sm font-medium text-slate-500 mb-1">Your annual change</p>
              <p className={`text-4xl font-bold ${r.change >= 0 ? "text-green-700" : "text-red-700"}`}>
                {r.change >= 0 ? "+" : ""}{fmt(r.change)}
              </p>
              <p className="text-sm text-slate-500 mt-1">
                {r.changePct > 0 ? `${r.changePct.toFixed(0)}% increase` : ""} in take-home income
              </p>
            </div>

            {/* Side by side */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-50 rounded-lg p-4">
                <p className="text-xs font-medium text-slate-400 mb-1">CURRENT SYSTEM</p>
                <p className="text-sm text-slate-600">Income tax: <span className="font-semibold text-red-600">−{fmt(c.fedTax)}</span></p>
                <p className="text-sm text-slate-600">FICA: <span className="font-semibold text-red-600">−{fmt(c.fica)}</span></p>
                <p className="text-lg font-bold text-slate-900 mt-2 pt-2 border-t border-slate-200">
                  {fmt(c.takeHome)}
                </p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-xs font-medium text-blue-400 mb-1">FOUR PILLARS</p>
                <p className="text-sm text-slate-600">Floor: <span className="font-semibold text-green-600">+{fmt(r.floor)}</span></p>
                {r.childPillar4 > 0 && (
                  <p className="text-sm text-slate-600">Family: <span className="font-semibold text-green-600">+{fmt(r.childPillar4)}</span></p>
                )}
                {r.creativePillar > 0 && (
                  <p className="text-sm text-slate-600">Creative: <span className="font-semibold text-green-600">+{fmt(r.creativePillar)}</span></p>
                )}
                {r.civicPillar > 0 && (
                  <p className="text-sm text-slate-600">Civic: <span className="font-semibold text-green-600">+{fmt(r.civicPillar)}</span></p>
                )}
                <p className="text-sm text-slate-600">VAT: <span className="font-semibold text-red-600">−{fmt(r.vatPaid)}</span></p>
                <p className="text-lg font-bold text-slate-900 mt-2 pt-2 border-t border-blue-200">
                  {fmt(r.net)}
                </p>
              </div>
            </div>

            {/* Expand details */}
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              {showDetails ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              {showDetails ? "Hide details" : "Show retirement & healthcare details"}
            </button>

            {showDetails && (
              <div className="space-y-4 border-t border-slate-200 pt-4">
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-sm font-medium text-slate-700 mb-2">Retirement Projection (30 years)</p>
                  <p className="text-sm text-slate-600">
                    Mandatory 401(k): {fmt(r.mandatory401k)}/year → <span className="font-bold text-slate-900">{fmt(r.retireBalance)}</span> balance at retirement
                  </p>
                  <p className="text-sm text-slate-600 mt-1">
                    Retirement income (4% rule + floor): <span className="font-bold text-green-700">{fmt(r.retireIncome)}/year</span>
                  </p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-sm font-medium text-slate-700 mb-2">Healthcare</p>
                  <p className="text-sm text-slate-600">{r.healthcareNote}</p>
                </div>
              </div>
            )}
          </div>
        </div>

        <p className="text-xs text-slate-400 mt-8">
          Estimates based on the Four Pillars Framework v3.0. Actual results depend on spending patterns, investment returns, and final policy design.
          VAT calculated at 20% on 70% of spending (basics exempt). Floor phases out at 50¢ per $1 earned above $30,000.
        </p>
      </div>
    </div>
  );
}

function HowItWorksSection() {
  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-slate-900 mb-10">How It Works</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div>
          <h3 className="text-xl font-bold text-slate-900 mb-4">For People</h3>
          <div className="space-y-4 text-slate-600 leading-relaxed">
            <p>No federal income tax. No employee FICA. You keep 100% of your paycheck.</p>
            <p>Pay 20% VAT when you spend — but groceries, rent, healthcare, and education are exempt.</p>
            <p>Receive a floor payment based on income: full $25K if you earn under $30K, phasing to zero at $80K.</p>
            <p>Free healthcare if your employer doesn't cover you.</p>
            <p>Mandatory 10% goes into YOUR personal 401(k) — not Social Security. You own it. You keep it. You pass it on.</p>
          </div>
        </div>
        <div>
          <h3 className="text-xl font-bold text-slate-900 mb-4">For Companies</h3>
          <div className="space-y-4 text-slate-600 leading-relaxed">
            <p>Health insurance continues as-is. No disruption.</p>
            <p>Employer FICA adjusts to 9% with no wage cap.</p>
            <p>Corporate tax returns to 28% (pre-2017 level).</p>
            <p>Automation tax: 50% of net labor savings from AI/robots. Automation is still profitable — just shared.</p>
            <p>Your customers now have guaranteed purchasing power. Every adult in America can buy your product.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function PoliticalSection() {
  return (
    <div className="bg-slate-50 border-y border-slate-200">
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-slate-900 mb-10">Something For Everyone</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
            <p className="text-sm font-semibold text-red-600 mb-3">FOR THE RIGHT</p>
            <p className="text-slate-600 leading-relaxed">
              No income tax. Personal 401(k) ownership — not government-controlled Social Security.
              Smaller welfare bureaucracy. US citizens only. Market-driven compensation.
              Consumer spending fuels business growth.
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
            <p className="text-sm font-semibold text-blue-600 mb-3">FOR THE LEFT</p>
            <p className="text-slate-600 leading-relaxed">
              Universal income floor. Healthcare for everyone without employer coverage.
              Companies pay 37% of revenue (up from 16%). Caregiving compensated.
              Biggest gains go to lowest earners.
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
            <p className="text-sm font-semibold text-purple-600 mb-3">FOR THE CENTER</p>
            <p className="text-slate-600 leading-relaxed">
              Real math with Monte Carlo validation. Phased 10-year transition with rollback provisions.
              Path to balanced budget. Simpler tax code. Data-driven scaling decisions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function DocumentsSection() {
  const docs = [
    { name: "Full Whitepaper", desc: "Peer-review format, 14 sections + appendices", file: "Four_Pillars_Whitepaper.md" },
    { name: "Executive Summary", desc: "One-page overview", file: "Executive_Summary.md" },
    { name: "Economic Model", desc: "Complete balance sheet and 10-year trajectory", file: "Economic_Model_Research.md" },
    { name: "17 Persona Stress Tests", desc: "From unemployed to CEO — everyone's outcome", file: "Persona_Stress_Tests.md" },
    { name: "Inflation Analysis", desc: "Why redistribution ≠ money printing", file: "Inflation_Analysis.md" },
    { name: "International Comparison", desc: "Finland, Kenya, Singapore, and more", file: "International_Comparison.md" },
    { name: "Pilot Program Design", desc: "75K participant federal demonstration", file: "Pilot_Program_Design.md" },
    { name: "Transition Plan", desc: "Year-by-year implementation roadmap", file: "Transition_Plan.md" },
  ];
  const baseUrl = "https://github.com/saccasolutions/fourpillarsproject/blob/main/docs/";
  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-slate-900 mb-3">Full Documentation</h2>
      <p className="text-lg text-slate-500 mb-10">
        Every claim is backed by data. Every number is sourced. Dig in.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {docs.map((d) => (
          <a
            key={d.file}
            href={`${baseUrl}${d.file}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between p-4 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-blue-50 transition-colors group"
          >
            <div>
              <p className="font-semibold text-slate-900 group-hover:text-blue-700">{d.name}</p>
              <p className="text-sm text-slate-500">{d.desc}</p>
            </div>
            <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-blue-500 flex-shrink-0" />
          </a>
        ))}
      </div>
      <div className="mt-8 flex gap-4">
        <a
          href="https://github.com/saccasolutions/fourpillarsproject"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-slate-600 hover:text-slate-900 font-medium"
        >
          <Github className="w-5 h-5" />
          View on GitHub
        </a>
        <a
          href="https://github.com/saccasolutions/fourpillarsproject/tree/main/models"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-slate-600 hover:text-slate-900 font-medium"
        >
          <BarChart3 className="w-5 h-5" />
          Python Models
        </a>
      </div>
    </div>
  );
}

function OneSentence() {
  return (
    <div className="bg-blue-600 text-white">
      <div className="max-w-4xl mx-auto px-6 py-16 text-center">
        <p className="text-xl md:text-2xl leading-relaxed font-light italic">
          "The Four Pillars framework eliminates income tax, replaces Social Security
          with personal investment accounts, provides every citizen a guaranteed floor
          funded by consumption and automation taxes, and reaches budget surplus within
          a decade — all while making every income level better off."
        </p>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <div className="bg-slate-900 text-slate-400">
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="flex flex-col md:flex-row justify-between items-start gap-8">
          <div>
            <p className="text-white font-bold text-lg mb-2">The Four Pillars Project</p>
            <p className="text-sm">Rob DeMaria</p>
            <p className="text-sm">robert@saccasolutions.com</p>
          </div>
          <div className="flex gap-8 text-sm">
            <a href="https://github.com/saccasolutions/fourpillarsproject" className="hover:text-white transition-colors">GitHub</a>
            <a href="https://github.com/saccasolutions/fourpillarsproject/blob/main/docs/Four_Pillars_Whitepaper.md" className="hover:text-white transition-colors">Whitepaper</a>
            <a href="https://github.com/saccasolutions/fourpillarsproject/blob/main/LICENSE-DOCS.md" className="hover:text-white transition-colors">CC BY 4.0</a>
          </div>
        </div>
        <div className="border-t border-slate-800 mt-8 pt-8 text-xs">
          Documents licensed under CC BY 4.0. Code licensed under MIT. April 2026.
        </div>
      </div>
    </div>
  );
}

// ─── Main App ───
export default function App() {
  const calculatorRef = useRef(null);
  const scrollToCalculator = () => {
    calculatorRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-white">
      <HeroSection onCalculatorClick={scrollToCalculator} />
      <StatsRow />
      <CalculatorSection calculatorRef={calculatorRef} />
      <PillarsSection />
      <HowItWorksSection />
      <ComparisonTable />
      <PoliticalSection />
      <OneSentence />
      <DocumentsSection />
      <Footer />
    </div>
  );
}
