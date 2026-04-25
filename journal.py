import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
from datetime import datetime, date
import calendar
import os
import glob
from fpdf import FPDF
import re

# --- 1. PREMIUM UI STYLING ---
st.set_page_config(page_title="Asifahmed Khatib's Elite Journal", layout="wide")

# =========================================================
# 🔑 FULL MASTER KEY LIST (ALL 200 UNIQUE KEYS LOADED)
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
    if user_key == "":
        st.info("🗝️ Please enter your activation key to unlock.")
    else:
        st.error("❌ Invalid Key. Please contact asif.gks@gmail.com for your unique access key.")
    st.stop()

current_user_name = ACCESS_KEYS[user_key]
st.sidebar.success(f"✅ Verified: {current_user_name}")

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .net-profit-box { background: linear-gradient(145deg, #1c2128, #161b22); padding: 30px; border-radius: 15px; border: 1px solid #30363d; text-align: center; margin-bottom: 30px; }
    .profit-text-big { font-size: 48px; font-weight: 900; display: block; }
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
    .ai-point { margin-bottom: 12px; font-size: 14px; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTO-LOAD ---
try:
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    report_folder = os.path.join(desktop_path, "Trading_Reports")
    if not os.path.exists(report_folder): os.makedirs(report_folder)
    list_of_files = glob.glob(os.path.join(report_folder, "*.html"))
    latest_file = max(list_of_files, key=os.path.getctime) if list_of_files else None
except:
    latest_file = None 

st.sidebar.title("💎 Settings")
initial_deposit = st.sidebar.number_input("Initial Deposit ($)", min_value=0.0, value=1000.0, step=100.0)
source = None
if latest_file:
    with open(latest_file, 'rb') as f: source = f.read()
    st.sidebar.success(f"📂 Auto-Sync: {os.path.basename(latest_file)}")
uploaded_file = st.sidebar.file_uploader("Upload MT5 Report (HTML)", type="html")
if uploaded_file: source = uploaded_file.read()
st.sidebar.write("---")

# --- DASHBOARD ---
st.title(f"📊 {current_user_name}'s Elite Journal")
if source:
    try:
        html_str = source.decode("utf-16", errors="ignore") if b'\xff\xfe' in source else source.decode("utf-8", errors="ignore")
        live_credit = 0.0
        credit_match = re.search(r"Credit Facility:([\d\.\-\s]+)", html_str.replace('\xa0', ''))
        if credit_match: live_credit = float(credit_match.group(1).replace(' ', ''))
        all_tables = pd.read_html(StringIO(html_str), header=None)
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
            df['Trade_Idx'] = range(1, len(df) + 1)
            df['Close'] = initial_deposit + df['Profit'].cumsum()
            df['Open'] = df['Close'] - df['Profit']
            df['High'] = df[['Open', 'Close']].max(axis=1)
            df['Low'] = df[['Open', 'Close']].min(axis=1)
            net_p = float(df['Profit'].sum())
            gross_p = float(df[df['Profit'] > 0]['Profit'].sum())
            gross_l = float(df[df['Profit'] < 0]['Profit'].sum())
            pf = abs(gross_p / gross_l) if gross_l != 0 else 0.0
            win_rate = (len(df[df['Profit']>0])/len(df)*100)
            avg_win = float(df[df['Profit'] > 0]['Profit'].mean()) if not df[df['Profit'] > 0].empty else 0
            avg_loss = abs(float(df[df['Profit'] < 0]['Profit'].mean())) if not df[df['Profit'] < 0].empty else 0
            rr = (avg_win/avg_loss if avg_loss != 0 else 0)
            df['Session'] = df['Hour'].apply(lambda x: "London" if 7 <= x < 14 else "NY" if 14 <= x < 21 else "Asian")
            best_session = df.groupby('Session')['Profit'].sum().idxmax()
            best_symbol = df.groupby('Symbol')['Profit'].sum().idxmax()
            best_profit = df.groupby('Symbol')['Profit'].sum().max()
            p_class = "pos-val" if net_p >= 0 else "neg-val"
            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="net-profit-box"><span style="color:#848da0; font-size:14px;">NET PROFIT</span><span class="profit-text-big {p_class}">${net_p:,.2f}</span></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="net-profit-box"><span style="color:#848da0; font-size:14px;">TOTAL EQUITY</span><span class="profit-text-big" style="color:#58a6ff;">${initial_deposit+net_p:,.2f}</span></div>', unsafe_allow_html=True)
            col_l, col_r = st.columns([2, 1])
            with col_l:
                st.subheader("🕯️ Equity Curve")
                fig = go.Figure(data=[go.Candlestick(x=df['Trade_Idx'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], increasing_line_color='#00ffc8', decreasing_line_color='#ff4b4b')])
                fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            with col_r:
                st.subheader("🤖 AI Insights")
                st.markdown('<div class="ai-box">', unsafe_allow_html=True)
                st.write(f"🕒 **Session Focus:** Best results in **{best_session}**.")
                if rr < 1: st.write("⚠️ **Risk:** Winners smaller than losses.")
                st.write(f"💎 **Best Asset:** **{best_symbol}** (+${best_profit:,.0f}).")
                st.markdown('</div>', unsafe_allow_html=True)
            st.write("---")
            sel_month = st.sidebar.selectbox("Month", list(calendar.month_name)[1:], index=datetime.now().month-1)
            sel_month_idx = list(calendar.month_name).index(sel_month)
            daily_pnl = df.groupby('Date')['Profit'].sum().to_dict()
            weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(datetime.now().year, sel_month_idx)
            for week in weeks:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    if day != 0:
                        p = daily_pnl.get(date(datetime.now().year, sel_month_idx, day), 0)
                        style = "win" if p > 0 else "loss" if p < 0 else "neutral"
                        cols[i].markdown(f"<div class='calendar-card {style}'><div style='font-size:10px;'>{day}</div><div class='cal-amt'>${p:,.0f}</div></div>", unsafe_allow_html=True)
            st.write("---")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.markdown(f'<div class="metric-card"><div class="metric-label">Credit</div><div class="metric-value">${live_credit:,.2f}</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric-card"><div class="metric-label">Gross Win</div><div class="metric-value" style="color:#00ffc8">${gross_p:,.0f}</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="metric-card"><div class="metric-label">Gross Loss</div><div class="metric-value" style="color:#ff4b4b">${abs(gross_l):,.0f}</div></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="metric-card"><div class="metric-label">PF</div><div class="metric-value">{pf:.2f}</div></div>', unsafe_allow_html=True)
            m5.markdown(f'<div class="metric-card"><div class="metric-label">Win Rate</div><div class="metric-value">{win_rate:.1f}%</div></div>', unsafe_allow_html=True)
            st.write("---")
            c_a, c_b = st.columns(2)
            with c_a:
                st.subheader("🕒 Session Split")
                st.plotly_chart(px.pie(df, names='Session', hole=0.6, color_discrete_sequence=['#00ffc8', '#ff4b4b', '#58a6ff'], template="plotly_dark"), use_container_width=True)
            with c_b:
                st.subheader("💰 Asset Split")
                sym_p = df.groupby('Symbol')['Profit'].sum().reset_index()
                st.plotly_chart(px.bar(sym_p, x='Symbol', y='Profit', color='Profit', color_continuous_scale='RdYlGn', template="plotly_dark"), use_container_width=True)
            def create_exec_pdf():
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 18)
                pdf.cell(190, 15, "STRATEGIC TRADING AUDIT", ln=True, align='C')
                stats = [("User", f"{current_user_name}"), ("Profit", f"${net_p:,.2f}"), ("PF", f"{pf:.2f}")]
                for label, val in stats:
                    pdf.cell(95, 10, label, 1); pdf.cell(95, 10, val, 1, 1, 'R')
                return pdf.output(dest='S').encode('latin-1')
            st.sidebar.write("---")
            st.sidebar.download_button(label="📥 DOWNLOAD PDF", data=create_exec_pdf(), file_name="Elite_Audit.pdf", mime="application/pdf", use_container_width=True)
    except Exception as e: st.error(f"Error: {e}")
