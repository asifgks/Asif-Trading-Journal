import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
from datetime import datetime, date
import calendar
import re

# --- 1. PREMIUM UI STYLING ---
st.set_page_config(page_title="Elite Trading Journal", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .net-profit-box { background: linear-gradient(145deg, #1c2128, #161b22); padding: 25px; border-radius: 15px; border: 1px solid #30363d; text-align: center; margin-bottom: 20px; }
    .profit-text-big { font-size: 32px; font-weight: 900; display: block; }
    .pos-val { color: #00ffc8; text-shadow: 0 0 20px rgba(0,255,200,0.2); }
    .neg-val { color: #ff4b4b; text-shadow: 0 0 20px rgba(255,75,75,0.2); }
    .metric-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .metric-label { color: #848da0; font-size: 12px; text-transform: uppercase; font-weight: 600; }
    .metric-value { color: #f0f6fc; font-size: 22px; font-weight: 700; margin-top: 5px; }
    .calendar-card { border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 10px; border: 1px solid #30363d; min-height: 95px; }
    .win { background-color: rgba(6, 78, 59, 0.5); color: #10b981; border-color: #10b981; }
    .loss { background-color: rgba(69, 26, 26, 0.5); color: #ef4444; border-color: #ef4444; }
    .neutral { background-color: #1c2128; color: #848da0; }
    .cal-amt { font-size: 20px !important; font-weight: 900 !important; margin-top: 8px; letter-spacing: -0.5px; }
    .ai-box { background: rgba(88, 166, 255, 0.05); border: 1px solid #58a6ff; padding: 25px; border-radius: 15px; margin-top: 10px; }
    .ai-header { color: #58a6ff; font-weight: 800; font-size: 18px; margin-bottom: 15px; border-bottom: 1px solid #30363d; padding-bottom: 5px; }
    .ai-point { margin-bottom: 20px; font-size: 14px; line-height: 1.6; border-bottom: 1px solid #21262d; padding-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🔑 FULL MASTER KEY LIST (ALL 200 UNIQUE KEYS RESTORED)
# =========================================================
ACCESS_KEYS = {
    "ASIF-XJ92-71": "Asifahmed Khatib", "ASIF-BK44-09": "Elite Member", "ASIF-91PT-K2": "Elite Member",
    "ASIF-QL77-X1": "Elite Member", "ASIF-M52R-BB": "Elite Member", "ASIF-22KW-L9": "Elite Member",
    "ASIF-HN81-V4": "Elite Member", "ASIF-Z09Q-M3": "Elite Member", "ASIF-TRD8-KP": "Elite Member",
    "ASIF-71VL-NW": "Elite Member", "ASIF-Y02X-B1": "Elite Member", "ASIF-44MZ-Q8": "Elite Member",
    "ASIF-RK99-PL": "Elite Member", "ASIF-52GT-X0": "Elite Member", "ASIF-11WR-M9": "Elite Member",
    "ASIF-88NZ-V2": "Elite Member", "ASIF-33CQ-L1": "Elite Member", "ASIF-HX01-Z7": "Elite Member",
    "ASIF-MN82-W4": "Elite Member", "ASIF-55BQ-K0": "Elite Member", "ASIF-V77X-L2": "Elite Member",
    "ASIF-40MT-P1": "Elite Member", "ASIF-61ZK-B9": "Elite Member", "ASIF-12KW-N5": "Elite Member",
    "ASIF-89PL-X3": "Elite Member", "ASIF-22MV-Q1": "Elite Member", "ASIF-77GT-B4": "Elite Member",
    "ASIF-01XJ-Z9": "Elite Member", "ASIF-55MK-L2": "Elite Member", "ASIF-99RK-V4": "Elite Member",
    "ASIF-10TR-N1": "Elite Member", "ASIF-44HX-Z3": "Elite Member", "ASIF-81NV-L4": "Elite Member",
    "ASIF-22ZK-M9": "Elite Member", "ASIF-33CQ-X1": "Elite Member", "ASIF-77VN-L2": "Elite Member",
    "ASIF-01BQ-Z7": "Elite Member", "ASIF-55GT-W4": "Elite Member", "ASIF-88MV-K0": "Elite Member",
    "ASIF-11KW-X3": "Elite Member", "ASIF-40NZ-M9": "Elite Member", "ASIF-61XJ-L2": "Elite Member",
    "ASIF-99RK-Z7": "Elite Member", "ASIF-22TR-P1": "Elite Member", "ASIF-77BQ-M9": "Elite Member",
    "ASIF-01NX-Z3": "Elite Member", "ASIF-55ZK-V4": "Elite Member", "ASIF-88MT-L1": "Elite Member",
    "ASIF-11VL-X2": "Elite Member", "ASIF-44CQ-M9": "Elite Member", "ASIF-B981-L4": "Elite Member",
    "ASIF-X223-K9": "Elite Member", "ASIF-M001-Z0": "Elite Member", "ASIF-Q992-B1": "Elite Member",
    "ASIF-V007-X1": "Elite Member", "ASIF-K881-M3": "Elite Member", "ASIF-Z442-L9": "Elite Member",
    "ASIF-P110-N5": "Elite Member", "ASIF-W773-X2": "Elite Member", "ASIF-N552-V4": "Elite Member",
    "ASIF-J011-Z7": "Elite Member", "ASIF-H882-L1": "Elite Member", "ASIF-C339-X9": "Elite Member",
    "ASIF-L661-B4": "Elite Member", "ASIF-R228-N5": "Elite Member", "ASIF-T441-V2": "Elite Member",
    "ASIF-G779-Z3": "Elite Member", "ASIF-Y002-L1": "Elite Member", "ASIF-M993-X7": "Elite Member",
    "ASIF-P448-B1": "Elite Member", "ASIF-ALPHA-01": "Elite Member", "ASIF-BETA-99": "Elite Member",
    "ASIF-GAMMA-77": "Elite Member", "ASIF-DELTA-22": "Elite Member", "ASIF-EPS-110": "Elite Member",
    "ASIF-ZETA-44": "Elite Member", "ASIF-ETA-881": "Elite Member", "ASIF-THETA-07": "Elite Member",
    "ASIF-IOTA-332": "Elite Member", "ASIF-KAPPA-55": "Elite Member", "ASIF-OMEGA-00": "Elite Member",
    "ASIF-SIGMA-92": "Elite Member", "ASIF-PI-3141": "Elite Member", "ASIF-RHO-228": "Elite Member",
    "ASIF-TAU-773": "Elite Member", "ASIF-PHI-161": "Elite Member", "ASIF-CHI-009": "Elite Member",
    "ASIF-PSI-442": "Elite Member", "ASIF-NEO-881": "Elite Member", "ASIF-EXO-552": "Elite Member",
    "ASIF-ZEN-101": "Elite Member", "ASIF-MAX-992": "Elite Member", "ASIF-LUX-773": "Elite Member",
    "ASIF-VEX-442": "Elite Member", "ASIF-NEX-011": "Elite Member", "ASIF-CORE-92": "Elite Member",
    "ASIF-GRID-33": "Elite Member", "ASIF-FLOW-11": "Elite Member", "ASIF-SYNC-88": "Elite Member",
    "ASIF-LINK-44": "Elite Member", "ASIF-ELITE-101": "Elite Member", "ASIF-PRIME-77": "Elite Member",
    "ASIF-APEX-221": "Elite Member", "ASIF-VANT-990": "Elite Member", "ASIF-EDGE-441": "Elite Member",
    "ASIF-TRAD-882": "Elite Member", "ASIF-BOLT-113": "Elite Member", "ASIF-FIRE-007": "Elite Member",
    "ASIF-AERO-449": "Elite Member", "ASIF-BLUE-772": "Elite Member", "ASIF-GOLD-991": "Elite Member",
    "ASIF-SILV-443": "Elite Member", "ASIF-IRON-884": "Elite Member", "ASIF-PLAT-115": "Elite Member",
    "ASIF-RUBY-006": "Elite Member", "ASIF-EMER-448": "Elite Member", "ASIF-ONYX-771": "Elite Member",
    "ASIF-OPAL-992": "Elite Member", "ASIF-JADE-441": "Elite Member", "ASIF-TIGER-88": "Elite Member",
    "ASIF-EAGLE-11": "Elite Member", "ASIF-SHARK-44": "Elite Member", "ASIF-LION-777": "Elite Member",
    "ASIF-WOLF-992": "Elite Member", "ASIF-HAWK-441": "Elite Member", "ASIF-BEAR-882": "Elite Member",
    "ASIF-BULL-113": "Elite Member", "ASIF-FALC-007": "Elite Member", "ASIF-PANT-449": "Elite Member",
    "ASIF-STRL-772": "Elite Member", "ASIF-MOON-991": "Elite Member", "ASIF-STAR-443": "Elite Member",
    "ASIF-SUN-884": "Elite Member", "ASIF-SKY-115": "Elite Member", "ASIF-SEA-006": "Elite Member",
    "ASIF-WIND-448": "Elite Member", "ASIF-ROCK-771": "Elite Member", "ASIF-DARK-992": "Elite Member",
    "ASIF-LITE-441": "Elite Member", "ASIF-VIBE-88": "Elite Member", "ASIF-CODE-11": "Elite Member",
    "ASIF-DATA-44": "Elite Member", "ASIF-INFO-777": "Elite Member", "ASIF-TECH-992": "Elite Member",
    "ASIF-GLOW-441": "Elite Member", "ASIF-BEAM-882": "Elite Member", "ASIF-RAYS-113": "Elite Member",
    "ASIF-GLNT-007": "Elite Member", "ASIF-SHNE-449": "Elite Member", "ASIF-BOLD-772": "Elite Member",
    "ASIF-WISE-991": "Elite Member", "ASIF-TRUE-443": "Elite Member", "ASIF-REAL-884": "Elite Member",
    "ASIF-PURE-115": "Elite Member", "ASIF-FAST-006": "Elite Member", "ASIF-SLIK-448": "Elite Member",
    "ASIF-SMRT-771": "Elite Member", "ASIF-COOL-992": "Elite Member", "ASIF-EPIC-441": "Elite Member",
    "ASIF-HERO-88": "Elite Member", "ASIF-KING-11": "Elite Member", "ASIF-LORD-44": "Elite Member",
    "ASIF-CHMP-777": "Elite Member", "ASIF-BOSS-992": "Elite Member", "ASIF-MAST-441": "Elite Member",
    "ASIF-ACE-882": "Elite Member", "ASIF-PRO-113": "Elite Member", "ASIF-GURU-007": "Elite Member",
    "ASIF-WIZ-449": "Elite Member", "ASIF-MYST-772": "Elite Member", "ASIF-RARE-991": "Elite Member",
    "ASIF-UNQ-443": "Elite Member", "ASIF-SOLO-884": "Elite Member", "ASIF-DUO-115": "Elite Member",
    "ASIF-TRIO-006": "Elite Member", "ASIF-QUAD-448": "Elite Member", "ASIF-PENT-771": "Elite Member",
    "ASIF-HEXA-992": "Elite Member", "ASIF-HEPT-441": "Elite Member", "ASIF-OCTA-88": "Elite Member",
    "ASIF-NONA-11": "Elite Member", "ASIF-DECA-44": "Elite Member", "ASIF-CENT-777": "Elite Member",
    "ASIF-MILL-992": "Elite Member", "ASIF-BILL-441": "Elite Member", "ASIF-TRIL-882": "Elite Member",
    "ASIF-QUAT-113": "Elite Member", "ASIF-QUINT-007": "Elite Member", "ASIF-SEXT-449": "Elite Member",
    "ASIF-SEPT-772": "Elite Member", "ASIF-OCT-991": "Elite Member", "ASIF-NOV-443": "Elite Member",
    "ASIF-DEC-884": "Elite Member", "ASIF-JAN-115": "Elite Member", "ASIF-FEB-006": "Elite Member",
    "ASIF-MAR-448": "Elite Member", "ASIF-APR-771": "Elite Member", "ASIF-MAY-992": "Elite Member",
    "ASIF-JUN-441": "Elite Member", "ASIF-JUL-88": "Elite Member", "ASIF-AUG-11": "Elite Member"
}

st.sidebar.title("🔐 Access Control")
user_key = st.sidebar.text_input("Enter Activation Key", type="password")

if user_key not in ACCESS_KEYS:
    if user_key == "": st.info("🗝️ Please enter your activation key to unlock.")
    else: st.error("❌ Invalid Key. Contact asif.gks@gmail.com")
    st.stop()

current_user_name = ACCESS_KEYS[user_key]
st.sidebar.success(f"✅ Verified: {current_user_name}")

# --- 2. SETTINGS ---
st.sidebar.title("💎 Global Settings")
initial_deposit_val = st.sidebar.number_input("Starting Balance ($)", min_value=0.0, value=1000.0)

uploaded_file = st.sidebar.file_uploader("Upload MT5 Report (HTML)", type="html")

# --- 3. DATA PROCESSING ---
st.title("📊 Elite Trading Journal")

if uploaded_file:
    try:
        source = uploaded_file.read()
        raw_content = source.decode("utf-16", errors="ignore") if b'\xff\xfe' in source else source.decode("utf-8", errors="ignore")
        clean_html = raw_content.replace('\xa0', ' ').replace('&nbsp;', ' ')
        
        # --- BRUTE FORCE CREDIT DISCOVERY ---
        live_credit = 0.0
        clean_str = re.sub(r'<[^>]*>', ' ', clean_html)
        credit_pattern = re.search(r"Credit\s*Facility[:\s]*(-?[\d\s,]+\.?\d*)", clean_str, re.IGNORECASE)
        if credit_pattern:
            try: live_credit = abs(float(credit_pattern.group(1).replace(' ', '').replace(',', '')))
            except: pass

        all_tables = pd.read_html(StringIO(clean_html), header=None)
        trades_list = []
        for table in all_tables:
            for idx, row in table.iterrows():
                row_str = [str(val).strip().lower() for val in row.values]
                if any(s in row_str for s in ['buy', 'sell']) and 'balance' not in row_str:
                    try:
                        p_idx = -3 if 'out' in row_str or 'in/out' in row_str else -2
                        profit_num = float(str(row.values[p_idx]).replace(' ', '').replace(',', '').replace('\xa0', ''))
                        trade_time = pd.to_datetime(row.values[0])
                        trades_list.append({'Time': trade_time, 'Date': trade_time.date(), 'Symbol': row.values[2], 'Profit': profit_num, 'Hour': trade_time.hour})
                    except: continue

        if trades_list:
            df = pd.DataFrame(trades_list).sort_values('Time')
            net_p = float(df['Profit'].sum())
            df['Trade_Idx'] = range(1, len(df) + 1)
            
            calc_start = initial_deposit_val - net_p
            df['Close_Balance'] = calc_start + df['Profit'].cumsum()
            df['Open_Balance'] = df['Close_Balance'] - df['Profit']
            
            total_equity = initial_deposit_val + live_credit
            
            gross_p = float(df[df['Profit'] > 0]['Profit'].sum())
            gross_l = float(df[df['Profit'] < 0]['Profit'].sum())
            pf = abs(gross_p / gross_l) if gross_l != 0 else 0.0
            win_rate = (len(df[df['Profit']>0])/len(df)*100)
            avg_win = df[df['Profit'] > 0]['Profit'].mean() if not df[df['Profit'] > 0].empty else 0
            avg_loss = abs(df[df['Profit'] < 0]['Profit'].mean()) if not df[df['Profit'] < 0].empty else 0
            rr = (avg_win/avg_loss if avg_loss != 0 else 0)
            
            # --- UI HEADER (TRIPLE BALANCE) ---
            p_class = "pos-val" if net_p >= 0 else "neg-val"
            h1, h2, h3, h4 = st.columns(4)
            with h1: st.markdown(f'<div class="net-profit-box"><span style="color:#848da0; font-size:12px;">NET PROFIT</span><span class="profit-text-big {p_class}">${net_p:,.2f}</span></div>', unsafe_allow_html=True)
            with h2: st.markdown(f'<div class="net-profit-box"><span style="color:#848da0; font-size:12px;">ACTUAL BALANCE</span><span class="profit-text-big" style="color:#f0f6fc;">${initial_deposit_val:,.2f}</span></div>', unsafe_allow_html=True)
            with h3: st.markdown(f'<div class="net-profit-box"><span style="color:#848da0; font-size:12px;">XM CREDIT</span><span class="profit-text-big" style="color:#ffb700;">${live_credit:,.2f}</span></div>', unsafe_allow_html=True)
            with h4: st.markdown(f'<div class="net-profit-box"><span style="color:#848da0; font-size:12px;">TOTAL EQUITY</span><span class="profit-text-big" style="color:#58a6ff;">${total_equity:,.2f}</span></div>', unsafe_allow_html=True)

            # --- MAIN DASHBOARD ---
            col_main, col_side = st.columns([2, 1])
            with col_main:
                st.subheader("🕯️ Equity Candlestick")
                fig = go.Figure(data=[go.Candlestick(x=df['Trade_Idx'], open=df['Open_Balance'], high=df[['Open_Balance', 'Close_Balance']].max(axis=1), low=df[['Open_Balance', 'Close_Balance']].min(axis=1), close=df['Close_Balance'], increasing_line_color='#00ffc8', decreasing_line_color='#ff4b4b')])
                fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            with col_side:
                best_sym = df.groupby('Symbol')['Profit'].sum().idxmax()
                st.subheader("🏆 Top Performer")
                st.markdown(f"""<div style="background:#1c2128; padding:20px; border-radius:12px; border-left:5px solid #00ffc8; margin-bottom:20px;"><h3 style="margin:0; color:#848da0; font-size:14px;">BEST SYMBOL</h3><h2 style="margin:5px 0; color:#f0f6fc;">{best_sym}</h2><p style="margin:0; color:#00ffc8; font-weight:bold;">+ High Probability Edge</p></div>""", unsafe_allow_html=True)
                
                # --- DEEP STRATEGIC AI AUDIT ---
                st.subheader("🤖 Strategic AI Audit")
                st.markdown('<div class="ai-box">', unsafe_allow_html=True)
                hourly_pnl = df.groupby('Hour')['Profit'].sum()
                best_hour = hourly_pnl.idxmax()
                st.markdown(f'<div class="ai-point">🕒 <b>Temporal Efficiency:</b> Capital productivity peaks at <b>{best_hour}:00</b>. Strategic concentration in this window is recommended.</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="ai-point">⚖️ <b>Risk Architecture:</b> Profit Factor of <b>{pf:.2f}</b>. Scores above 1.5 confirm sustainable system health.</div>', unsafe_allow_html=True)
                if rr < 1: st.markdown(f'<div class="ai-point">⚠️ <b>Math Warning:</b> Negative R:R detected. Individual losses currently outsize gains.</div>', unsafe_allow_html=True)
                else: st.markdown(f'<div class="ai-point">✅ <b>Positive Expectancy:</b> Edge confirmed with an R:R of <b>{rr:.2f}</b>.</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Footer Analysis
            st.write("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="metric-card"><div class="metric-label">Gross Win</div><div class="metric-value" style="color:#00ffc8">${gross_p:,.0f}</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric-card"><div class="metric-label">Gross Loss</div><div class="metric-value" style="color:#ff4b4b">${abs(gross_l):,.0f}</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="metric-card"><div class="metric-label">Profit Factor</div><div class="metric-value">{pf:.2f}</div></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="metric-card"><div class="metric-label">Win Rate</div><div class="metric-value">{win_rate:.1f}%</div></div>', unsafe_allow_html=True)

            st.write("---")
            c_pie, c_bar = st.columns(2)
            with c_pie:
                st.subheader("🕒 Session Split")
                df['Session'] = df['Hour'].apply(lambda x: "London" if 7 <= x < 14 else "NY" if 14 <= x < 21 else "Asian")
                st.plotly_chart(px.pie(df, names='Session', hole=0.6, color_discrete_sequence=['#00ffc8', '#ff4b4b', '#58a6ff'], template="plotly_dark"), use_container_width=True)
            with c_bar:
                st.subheader("💰 Asset Performance")
                sym_p = df.groupby('Symbol')['Profit'].sum().reset_index()
                st.plotly_chart(px.bar(sym_p, x='Symbol', y='Profit', color='Profit', color_continuous_scale='RdYlGn', template="plotly_dark"), use_container_width=True)

    except Exception as e: st.error(f"Error: {e}")
else:
    st.info(f"👋 Welcome {current_user_name}. Please upload your MT5 Report to begin.")
