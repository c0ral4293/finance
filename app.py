import streamlit as st
import yfinance as yf
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
 
# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinLens · Financial Health Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');
 
  :root {
    --bg:        #0b0f1a;
    --surface:   #111827;
    --surface2:  #1a2235;
    --border:    #1e2d45;
    --accent:    #00d4aa;
    --accent2:   #4f8ef7;
    --warn:      #f5a623;
    --danger:    #e05c5c;
    --text:      #e8edf5;
    --muted:     #6b7fa3;
    --serif:     'DM Serif Display', serif;
    --sans:      'DM Sans', sans-serif;
    --mono:      'JetBrains Mono', monospace;
  }
 
  html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg);
    color: var(--text);
  }
 
  /* hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }
 
  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
  }
  .hero-logo {
    font-family: var(--serif);
    font-size: 3rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .hero-sub {
    font-size: 0.95rem;
    color: var(--muted);
    margin-top: 0.4rem;
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
 
  /* ── Input row ── */
  .stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 1.05rem !important;
    padding: 0.7rem 1rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.15) !important;
  }
  .stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, #00b896 100%);
    color: #0b0f1a;
    border: none;
    border-radius: 8px;
    font-family: var(--sans);
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.65rem 2rem;
    cursor: pointer;
    transition: opacity 0.2s;
    width: 100%;
  }
  .stButton > button:hover { opacity: 0.85; }
 
  /* ── Metric cards ── */
  .metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
  }
  .metric-label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 500;
    margin-bottom: 0.4rem;
  }
  .metric-value {
    font-family: var(--mono);
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1;
  }
  .metric-delta {
    font-size: 0.78rem;
    margin-top: 0.35rem;
    font-weight: 500;
  }
  .delta-up   { color: var(--accent); }
  .delta-down { color: var(--danger); }
  .delta-flat { color: var(--muted);  }
 
  /* ── Section headers ── */
  .section-header {
    font-family: var(--serif);
    font-size: 1.45rem;
    color: var(--text);
    border-left: 3px solid var(--accent);
    padding-left: 0.8rem;
    margin: 2rem 0 1rem;
  }
 
  /* ── Health badge ── */
  .health-badge {
    display: inline-block;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .badge-good    { background: rgba(0,212,170,0.15); color: var(--accent); border: 1px solid rgba(0,212,170,0.35); }
  .badge-neutral { background: rgba(245,166,35,0.15); color: var(--warn);   border: 1px solid rgba(245,166,35,0.35); }
  .badge-poor    { background: rgba(224,92,92,0.15);  color: var(--danger); border: 1px solid rgba(224,92,92,0.35); }
 
  /* ── Table ── */
  .comparison-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
  }
  .comparison-table th {
    background: var(--surface2);
    color: var(--muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.72rem;
    padding: 0.7rem 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }
  .comparison-table td {
    padding: 0.65rem 1rem;
    border-bottom: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 0.85rem;
  }
  .comparison-table tr:hover td { background: var(--surface2); }
  .better  { color: var(--accent); }
  .worse   { color: var(--danger); }
  .neutral { color: var(--warn);   }
 
  /* ── Ticker chip ── */
  .ticker-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-family: var(--mono);
    font-size: 0.88rem;
    color: var(--accent2);
    margin-bottom: 1.5rem;
  }
 
  /* ── Spinner override ── */
  .stSpinner > div { border-top-color: var(--accent) !important; }
 
  /* ── Plotly chart background ── */
  .js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)
 
 
# ─── Backend Logic ────────────────────────────────────────────────────────────
 
RATIO_NAMES = [
    "Current Ratio", "Working Capital", "Debt-to-Equity",
    "Net Profit Margin", "Return on Equity", "Asset Turnover",
    "Inventory Turnover", "Operating Margin", "Gross Profit Margin",
    "Return on Assets", "P/E Ratio"
]
 
RATIO_THRESHOLDS = {
    "Current Ratio":       {"good": (1.5, None), "poor": (None, 1.0)},
    "Debt-to-Equity":      {"good": (None, 1.0), "poor": (2.0, None)},
    "Net Profit Margin":   {"good": (0.1, None), "poor": (None, 0.02)},
    "Return on Equity":    {"good": (0.15, None),"poor": (None, 0.05)},
    "Gross Profit Margin": {"good": (0.3, None), "poor": (None, 0.1)},
    "Return on Assets":    {"good": (0.05, None),"poor": (None, 0.01)},
}
 
finder_US = {
    "technology": "XLK", "financial-services": "XLF", "healthcare": "XLV",
    "energy": "XLE", "consumer-defensive": "XLP", "consumer-cyclical": "XLY",
    "industrials": "XLI", "utilities": "XLU", "basic-materials": "XLB",
    "real-estate": "XLRE", "communication-services": "XLC",
    "financialservices": "XLF",
}
 
def get_top_companies(ticker_obj):
    info = ticker_obj.info
    sector = info.get('sectorKey', '').lower().replace(' ', '-')
    ETF = finder_US.get(sector, "")
    if not ETF:
        return []
    et = yf.Ticker(ETF)
    try:
        top = et.funds_data.top_holdings
        return [top.index[i] for i in range(min(10, len(top)))]
    except:
        return []
 
def key_items():
    names = {
        "current_assets":    ["Total Current Assets","Current Assets","Total Current Asset"],
        "current_liab":      ["Total Current Liabilities","Current Liabilities","Total Current Liability"],
        "total_liab":        ["Total Liabilities Net Minority Interest","Total Liabilities"],
        "equity":            ["Stockholders Equity","Total Stockholders Equity","Total Equity","Common Stock Equity"],
        "revenue":           ["Total Revenue","Net Sales","Net Revenue","Revenue"],
        "net_income":        ["Net Income","Net Income Common Stockholders","Net Income From Continuing Ops"],
        "average_assets":    ["Total Assets","Total Combined Assets","Net Assets","Total Assets Net Minority Interest"],
        "average_inventory": ["Inventory","Total Inventory","Finished Goods","Work In Process","Raw Materials"],
        "cost_of_revenue":   ["Cost Of Revenue","Cost Of Goods Sold","Cost Of Sales","COGS"],
        "operating_revenue": ["Operating Revenue","Total Operating Profit"],
        "operating_expenses":["Operating Expense","Total Operating Expenses","Operating Expenses"],
        "interest_expense":  ["Interest Expense","Interest Expense Non Operating"],
        "tax_provision":     ["Tax Provision","Provision For Income Tax","Income Tax Expense"],
        "Earningpershare":   ["Basic EPS","Diluted EPS","BasicEPS","DilutedEPS","Earnings Per Share"],
    }
    return list(names.keys()), list(names.values())
 
def safe(val):
    try:
        v = float(val)
        return v if not math.isnan(v) else 0.0
    except:
        return 0.0
 
def data(df, items):
    for i in items:
        if i in df.index:
            return safe(df.loc[i].iloc[0]), safe(df.loc[i].iloc[1])
    return 0.0, 0.0
 
def avg_calc(key, df, items):
    a, b, c = 0.0, 0.0, 0.0
    for i in items:
        if key != "average_inventory":
            if i in df.index:
                a = safe(df.loc[i].iloc[0])
                b = safe(df.loc[i].iloc[1])
                c = safe(df.loc[i].iloc[2]) if len(df.loc[i]) > 2 else 0.0
        else:
            if i in df.index:
                a += safe(df.loc[i].iloc[0])
                b += safe(df.loc[i].iloc[1])
                c += safe(df.loc[i].iloc[2]) if len(df.loc[i]) > 2 else 0.0
    return (a + b) / 2, (b + c) / 2
 
def history_prices(hist):
    try:
        p2024 = safe(hist.loc["2024"].iloc[-1].iloc[3])
        p2025 = safe(hist.loc["2025"].iloc[-1].iloc[3])
        return p2024, p2025
    except:
        return 0.0, 0.0
 
def build_ratios(bs, financials, hist):
    keys, items = key_items()
    d24, d25 = {}, {}
    for i, k in enumerate(keys):
        if k in ["current_assets","current_liab","total_liab","equity","average_assets","average_inventory"]:
            if k in ["average_assets","average_inventory"]:
                v25, v24 = avg_calc(k, bs, items[i])
            else:
                v25, v24 = data(bs, items[i])
        else:
            v25, v24 = data(financials, items[i])
        d24[k], d25[k] = v24, v25
 
    ob = history_prices(hist)
 
    def r(n, d): return n / d if d != 0 else 0.0
 
    ratios24 = [
        r(d24['current_assets'], d24['current_liab']),
        d24['current_assets'] - d24['current_liab'],
        r(d24['total_liab'], d24['equity']),
        r(d24['net_income'], d24['revenue']),
        r(d24['net_income'], d24['equity']),
        r(d24['revenue'], d24['average_assets']),
        r(d24['cost_of_revenue'], d24['average_inventory']),
        r(d24['operating_revenue'] - d24['operating_expenses'], d24['operating_revenue']),
        r(d24['revenue'] - d24['cost_of_revenue'], d24['revenue']),
        r(d24['net_income'], d24['average_assets']),
        r(ob[0], d24['Earningpershare']),
    ]
    ratios25 = [
        r(d25['current_assets'], d25['current_liab']),
        d25['current_assets'] - d25['current_liab'],
        r(d25['total_liab'], d25['equity']),
        r(d25['net_income'], d25['revenue']),
        r(d25['net_income'], d25['equity']),
        r(d25['revenue'], d25['average_assets']),
        r(d25['cost_of_revenue'], d25['average_inventory']),
        r(d25['operating_revenue'] - d25['operating_expenses'], d25['operating_revenue']),
        r(d25['revenue'] - d25['cost_of_revenue'], d25['revenue']),
        r(d25['net_income'], d25['average_assets']),
        r(ob[1], d25['Earningpershare']),
    ]
    return ratios24, ratios25
 
@st.cache_data(show_spinner=False)
def fetch_all(ticker_symbol):
    t = yf.Ticker(ticker_symbol)
    bs = t.balance_sheet
    fin = t.financials
    hist = t.history(period="2y")
    info = t.info
 
    orig24, orig25 = build_ratios(bs, fin, hist)
    companies = get_top_companies(t)
 
    peer_data = []
    for c in companies:
        try:
            tc = yf.Ticker(c)
            r24, r25 = build_ratios(tc.balance_sheet, tc.financials, tc.history(period="2y"))
            peer_data.append((r24, r25))
        except:
            continue
 
    # Average peers
    peer24 = [0.0] * 11
    peer25 = [0.0] * 11
    counts24 = [0] * 11
    counts25 = [0] * 11
    for r24, r25 in peer_data:
        for i in range(11):
            if r24[i] != 0:
                peer24[i] += r24[i]; counts24[i] += 1
            if r25[i] != 0:
                peer25[i] += r25[i]; counts25[i] += 1
    peer24 = [peer24[i] / counts24[i] if counts24[i] else 0 for i in range(11)]
    peer25 = [peer25[i] / counts25[i] if counts25[i] else 0 for i in range(11)]
 
    return orig24, orig25, peer24, peer25, info, companies
 
def fmt(v, name):
    if name == "Working Capital":
        if abs(v) >= 1e9: return f"${v/1e9:.2f}B"
        if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
        return f"${v:,.0f}"
    pct_ratios = {"Net Profit Margin","Return on Equity","Operating Margin",
                  "Gross Profit Margin","Return on Assets"}
    if name in pct_ratios: return f"{v*100:.1f}%"
    return f"{v:.2f}x"
 
def badge(v, name):
    th = RATIO_THRESHOLDS.get(name)
    if not th:
        return '<span class="health-badge badge-neutral">Neutral</span>'
    good_lo, good_hi = th["good"]
    poor_lo, poor_hi = th["poor"]
    if (good_lo is not None and v >= good_lo) or (good_hi is not None and v <= good_hi):
        return '<span class="health-badge badge-good">Strong</span>'
    if (poor_lo is not None and v >= poor_lo) or (poor_hi is not None and v <= poor_hi):
        return '<span class="health-badge badge-poor">Weak</span>'
    return '<span class="health-badge badge-neutral">Fair</span>'
 
def delta_class(v_orig, v_peer, name):
    inverted = {"Debt-to-Equity"}
    better = v_orig < v_peer if name in inverted else v_orig > v_peer
    if abs(v_orig - v_peer) < 0.001: return "neutral"
    return "better" if better else "worse"
 
 
# ─── UI ───────────────────────────────────────────────────────────────────────
 
st.markdown("""
<div class="hero">
  <div class="hero-logo">FinLens</div>
  <div class="hero-sub">Company Financial Health Analyzer · Peer Benchmarking</div>
</div>
""", unsafe_allow_html=True)
 
col_in, col_btn, _ = st.columns([3, 1, 3])
with col_in:
    ticker_input = st.text_input("", placeholder="Enter ticker (e.g. AAPL, MSFT, RELIANCE.NS)", label_visibility="collapsed")
with col_btn:
    st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)
    analyze = st.button("Analyze →")
 
if analyze and ticker_input:
    ticker_symbol = ticker_input.strip().upper()
 
    with st.spinner(f"Fetching data for {ticker_symbol}…"):
        try:
            orig24, orig25, peer24, peer25, info, companies = fetch_all(ticker_symbol)
        except Exception as e:
            st.error(f"Could not fetch data: {e}")
            st.stop()
 
    # ── Company header ──────────────────────────────────────────────────────
    name   = info.get("longName", ticker_symbol)
    sector = info.get("sector", "N/A")
    mktcap = info.get("marketCap", 0)
    mktcap_str = f"${mktcap/1e9:.1f}B" if mktcap >= 1e9 else f"${mktcap/1e6:.0f}M"
 
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1.5rem; margin-bottom:1rem; flex-wrap:wrap;">
      <div>
        <div style="font-family:var(--serif); font-size:1.9rem; color:var(--text)">{name}</div>
        <div style="color:var(--muted); font-size:0.85rem; margin-top:0.2rem">{sector} · Market Cap {mktcap_str}</div>
      </div>
      <div class="ticker-chip">📈 {ticker_symbol}</div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Tabs ────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Peer Comparison", "📈 Trend Charts"])
 
    with tab1:
        st.markdown('<div class="section-header">FY 2025 Key Ratios</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        highlight = ["Current Ratio","Net Profit Margin","Return on Equity",
                     "Debt-to-Equity","Gross Profit Margin","P/E Ratio",
                     "Return on Assets","Asset Turnover"]
        idx_map = {n: i for i, n in enumerate(RATIO_NAMES)}
        for j, rname in enumerate(highlight):
            i = idx_map[rname]
            v25 = orig25[i]; v24 = orig24[i]
            delta_v = v25 - v24
            delta_pct = (delta_v / abs(v24) * 100) if v24 != 0 else 0
            cls = "delta-up" if delta_pct >= 0 else "delta-down"
            arrow = "▲" if delta_pct >= 0 else "▼"
            with cols[j % 4]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:1rem">
                  <div class="metric-label">{rname}</div>
                  <div class="metric-value">{fmt(v25, rname)}</div>
                  <div class="metric-delta {cls}">{arrow} {abs(delta_pct):.1f}% vs FY24</div>
                  <div style="margin-top:0.5rem">{badge(v25, rname)}</div>
                </div>
                """, unsafe_allow_html=True)
 
        # Summary table all ratios
        st.markdown('<div class="section-header">All Ratios · FY24 vs FY25</div>', unsafe_allow_html=True)
        rows = ""
        for i, rname in enumerate(RATIO_NAMES):
            v24, v25 = orig24[i], orig25[i]
            chg = v25 - v24
            chg_pct = (chg / abs(v24) * 100) if v24 != 0 else 0
            arrow = "▲" if chg_pct >= 0 else "▼"
            cls   = "better" if chg_pct >= 0 else "worse"
            rows += f"""
            <tr>
              <td style="color:var(--text); font-family:var(--sans); font-weight:500">{rname}</td>
              <td>{fmt(v24, rname)}</td>
              <td>{fmt(v25, rname)}</td>
              <td class="{cls}">{arrow} {abs(chg_pct):.1f}%</td>
              <td>{badge(v25, rname)}</td>
            </tr>"""
        st.markdown(f"""
        <table class="comparison-table">
          <thead><tr>
            <th>Ratio</th><th>FY 2024</th><th>FY 2025</th><th>Change</th><th>Health</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
 
    with tab2:
        st.markdown('<div class="section-header">Company vs Sector Peers (FY 2025)</div>', unsafe_allow_html=True)
        if companies:
            peers_str = "  ·  ".join(companies[:8])
            st.markdown(f'<p style="color:var(--muted); font-size:0.82rem; margin-bottom:1.2rem">Peers: {peers_str}</p>', unsafe_allow_html=True)
 
        rows = ""
        for i, rname in enumerate(RATIO_NAMES):
            if rname == "Working Capital": continue
            vo = orig25[i]; vp = peer25[i]
            dc = delta_class(vo, vp, rname)
            arrow = "▲" if vo > vp else ("▼" if vo < vp else "–")
            rows += f"""
            <tr>
              <td style="color:var(--text); font-family:var(--sans); font-weight:500">{rname}</td>
              <td style="color:var(--accent2); font-weight:600">{fmt(vo, rname)}</td>
              <td style="color:var(--muted)">{fmt(vp, rname)}</td>
              <td class="{dc}">{arrow} {dc.capitalize()}</td>
            </tr>"""
        st.markdown(f"""
        <table class="comparison-table">
          <thead><tr>
            <th>Ratio</th>
            <th>{ticker_symbol}</th>
            <th>Sector Avg</th>
            <th>vs Peers</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
 
        # Radar chart
        st.markdown('<div class="section-header">Radar · Multi-Dimensional Health</div>', unsafe_allow_html=True)
        radar_ratios = ["Current Ratio","Net Profit Margin","Return on Equity",
                        "Gross Profit Margin","Return on Assets","Asset Turnover"]
        r_idx = [RATIO_NAMES.index(r) for r in radar_ratios]
 
        def norm(vals, idxs):
            result = []
            for i in idxs:
                v = vals[i]
                result.append(min(max(v, -2), 5))
            return result
 
        orig_r = norm(orig25, r_idx)
        peer_r = norm(peer25, r_idx)
 
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=orig_r + [orig_r[0]], theta=radar_ratios + [radar_ratios[0]],
            fill='toself', name=ticker_symbol,
            line_color='#00d4aa', fillcolor='rgba(0,212,170,0.15)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=peer_r + [peer_r[0]], theta=radar_ratios + [radar_ratios[0]],
            fill='toself', name='Sector Avg',
            line_color='#4f8ef7', fillcolor='rgba(79,142,247,0.1)'
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, showticklabels=False, gridcolor='#1e2d45', linecolor='#1e2d45'),
                angularaxis=dict(tickfont=dict(color='#6b7fa3', size=11), gridcolor='#1e2d45', linecolor='#1e2d45'),
            ),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#6b7fa3'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=60, r=60, t=40, b=40),
            height=420
        )
        st.plotly_chart(fig_radar, use_container_width=True)
 
    with tab3:
        st.markdown('<div class="section-header">FY24 → FY25 Trend</div>', unsafe_allow_html=True)
        plot_ratios = [
            ("Net Profit Margin","Return on Equity"),
            ("Gross Profit Margin","Return on Assets"),
            ("Current Ratio","Debt-to-Equity"),
            ("Asset Turnover","P/E Ratio"),
        ]
        for pair in plot_ratios:
            col1, col2 = st.columns(2)
            for rname, col in zip(pair, [col1, col2]):
                i = RATIO_NAMES.index(rname)
                v24, v25 = orig24[i], orig25[i]
                color = '#00d4aa' if v25 >= v24 else '#e05c5c'
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=['FY 2024', 'FY 2025'], y=[v24, v25],
                    mode='lines+markers',
                    line=dict(color=color, width=2.5),
                    marker=dict(size=8, color=color),
                    fill='tozeroy', fillcolor=f'rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.08)',
                    name=rname
                ))
                fig.add_trace(go.Scatter(
                    x=['FY 2024', 'FY 2025'], y=[peer24[i], peer25[i]],
                    mode='lines+markers',
                    line=dict(color='#4f8ef7', width=1.5, dash='dot'),
                    marker=dict(size=6, color='#4f8ef7'),
                    name='Sector Avg'
                ))
                fig.update_layout(
                    title=dict(text=rname, font=dict(color='#e8edf5', size=13)),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,24,39,0.6)',
                    xaxis=dict(tickfont=dict(color='#6b7fa3'), gridcolor='#1e2d45', linecolor='#1e2d45'),
                    yaxis=dict(tickfont=dict(color='#6b7fa3'), gridcolor='#1e2d45', linecolor='#1e2d45'),
                    legend=dict(font=dict(color='#6b7fa3', size=10), bgcolor='rgba(0,0,0,0)'),
                    margin=dict(l=40, r=20, t=40, b=30),
                    height=260,
                )
                with col:
                    st.plotly_chart(fig, use_container_width=True)
 
elif not ticker_input and analyze:
    st.warning("Please enter a ticker symbol.")
else:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: var(--muted);">
      <div style="font-size:3rem; margin-bottom:1rem">📊</div>
      <div style="font-size:1.1rem; font-weight:500">Enter a ticker symbol above to begin analysis</div>
      <div style="font-size:0.85rem; margin-top:0.5rem">Supports global tickers · US, NSE, LSE and more</div>
    </div>
    """, unsafe_allow_html=True)