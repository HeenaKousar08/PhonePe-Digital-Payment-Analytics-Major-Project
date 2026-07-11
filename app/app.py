import streamlit as st
import pandas as pd
import plotly.express as px
import json, os, io, hashlib
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.decomposition import PCA
from scipy.stats import f_oneway, ttest_ind, chi2_contingency
from scipy.cluster.hierarchy import linkage

# ==========================================
# 1. UI CONFIGURATION (MUST BE FIRST ACTION)
# ==========================================
st.set_page_config(page_title="PhonePe Pulse Intelligence Pro", page_icon="📱", layout="wide")

# Modern Enterprise Palette Mapping
PRIMARY_COLOR = "#5F259F"    # Deep PhonePe Purple
SECONDARY_COLOR = "#7B3FE4"  # Royal Purple Accent
ACCENT_COLOR = "#A855F7"     # Electric Violet
BG_COLOR = "#F5F7FA"         # Light Soft BI Canvas Slate
TEXT_MAIN = "#1E293B"        # Dark Slate Text

# ==========================================
# 2. ADVANCED SAAS CSS ENGINE
# ==========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Main Frame Overhauls */
html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', sans-serif;
    background-color: {BG_COLOR};
    color: {TEXT_MAIN};
}}

[data-testid="stSidebarNav"] {{
    display: none !important;
}}

/* Sidebar Enterprise Transformation */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #3A106E 0%, {PRIMARY_COLOR} 100%);
    box-shadow: 4px 0px 20px rgba(0, 0, 0, 0.15);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}}

[data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {{
    color: #F8FAFC !important;
}}

/* FIXED SIDEBAR BUTTON OVERRIDES: Clear background contrast with distinct action colors */
div[data-testid="stSidebar"] button {{
    background-color: #FFFFFF !important;
    color: {PRIMARY_COLOR} !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
    transition: all 0.2s ease;
}}

div[data-testid="stSidebar"] button:hover {{
    background-color: #E63946 !important; 
    color: #FFFFFF !important;
    border-color: #E63946 !important;
    box-shadow: 0px 4px 12px rgba(230, 57, 70, 0.4) !important;
}}

/* Premium Hero Section */
.hero-banner {{
    background: linear-gradient(135deg, #3A106E 0%, {PRIMARY_COLOR} 50%, {SECONDARY_COLOR} 100%);
    border-radius: 16px;
    padding: 35px 45px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0px 12px 35px rgba(95, 37, 159, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.1);
}}

.hero-logo-box {{
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    padding: 8px 18px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -0.5px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

/* Glassmorphism Metric Processing Engine */
.bi-kpi-card {{
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0px 8px 24px rgba(148, 163, 184, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 20px;
}}

.bi-kpi-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0px 12px 30px rgba(95, 37, 159, 0.12);
    border-color: rgba(123, 63, 228, 0.4);
}}

.kpi-title {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 8px;
}}

.kpi-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {PRIMARY_COLOR};
    line-height: 1.1;
}}

.kpi-subtext {{
    font-size: 0.75rem;
    color: #94A3B8;
    margin-top: 6px;
}}

/* Premium Continuous Static Dashboard Panels */
.ai-insight-panel {{
    background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
    border-left: 6px solid {PRIMARY_COLOR};
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.02);
    margin: 20px 0;
}}

.ai-header {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {PRIMARY_COLOR};
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

/* Main Mainframe Download Button Styling */
div.stDownloadButton > button {{
    background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, {PRIMARY_COLOR} 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.4rem !important;
    font-weight: 600 !important;
    box-shadow: 0px 4px 14px rgba(95, 37, 159, 0.3) !important;
    transition: all 0.2s ease !important;
}}

div.stDownloadButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0px 6px 20px rgba(95, 37, 159, 0.45) !important;
}}

/* Tab Selection Custom UI Element */
div[data-testid="stTabs"] button {{
    font-weight: 600 !important;
    color: #64748B !important;
    background-color: transparent !important;
    border: none !important;
    padding: 12px 24px !important;
}}

div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {PRIMARY_COLOR} !important;
    border-bottom: 3px solid {PRIMARY_COLOR} !important;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SECURE CONFIGURATION & CREDENTIAL LOADER
# ==========================================
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

USERS_FILE_PATH = os.path.join(CONFIG_DIR, "users.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

DEFAULT_USERS = {
    "admin": hash_password("admin123"),
    "faculty": hash_password("faculty123"),
    "student": hash_password("student123"),
    "kousar": hash_password("kousar@08")
}

def load_users():
    if os.path.exists(USERS_FILE_PATH):
        try:
            with open(USERS_FILE_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_USERS
    return DEFAULT_USERS

def save_users(users_dict):
    try:
        with open(USERS_FILE_PATH, 'w') as f:
            json.dump(users_dict, f, indent=4)
    except Exception as e:
        st.error(f"Error synchronizing database: {e}")

USERS_PROFILE = load_users()

# ==========================================
# 4. ENTERPRISE ROLE-BASED ACCESS GATEWAY
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""

def render_login_portal():
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.image("https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png", width=140)
            
            account_mode = st.radio("Portal Navigation", ["Sign In", "Create Account"], horizontal=True, label_visibility="collapsed")
            
            if account_mode == "Sign In":
                st.markdown("<h3 style='text-align:center; color:#5F259F; margin-top:10px;'>Administrative Sign In</h3>", unsafe_allow_html=True)
                with st.form("access_gate_form"):
                    user_input = st.text_input("Corporate Username", placeholder="e.g., admin or kousar")
                    pass_input = st.text_input("Secure Passkey", type="password", placeholder="••••••••")
                    login_clicked = st.form_submit_button("Authenticate Access", width='stretch')
                    
                    if login_clicked:
                        current_users = load_users()
                        normalized_user = user_input.strip().lower()
                        hashed_attempt = hash_password(pass_input)
                        if normalized_user in current_users and current_users[normalized_user] == hashed_attempt:
                            st.session_state.logged_in = True
                            st.session_state.username = normalized_user
                            st.rerun()
                        else:
                            st.error("Access Denied. Invalid system profile credentials.")
            
            else:
                st.markdown("<h3 style='text-align:center; color:#5F259F; margin-top:10px;'>User Registration</h3>", unsafe_allow_html=True)
                with st.form("registration_form"):
                    new_user = st.text_input("Choose Username", placeholder="Enter unique username").strip().lower()
                    new_pass = st.text_input("Create Password", type="password", placeholder="Minimum 4 characters")
                    confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Re-type password")
                    register_clicked = st.form_submit_button("Register New User", width='stretch')
                    
                    if register_clicked:
                        current_users = load_users()
                        if not new_user or not new_pass:
                            st.error("Fields cannot be processed empty.")
                        elif len(new_pass) < 4:
                            st.error("Password string verification failed minimal security thresholds.")
                        elif new_pass != confirm_pass:
                            st.error("Password confirmation mismatch validation error.")
                        elif new_user in current_users:
                            st.error("Username identity variation already registered inside system schema.")
                        else:
                            current_users[new_user] = hash_password(new_pass)
                            save_users(current_users)
                            st.success("Registration Successful! Switch tab selection to 'Sign In'.")

if not st.session_state.logged_in:
    render_login_portal()
    st.stop()

# ==========================================
# 5. DATABASE & ENGINE SECTION
# ==========================================
@st.cache_resource
def get_engine():
    username = "heena"
    password = quote_plus("Heena@08")
    return create_engine(f"mysql+pymysql://{username}:{password}@127.0.0.1:3306/phonepe")

engine = get_engine()

@st.cache_data
def load_base_data():
    df = pd.read_sql("SELECT * FROM aggregated_transaction", engine)
    df.columns = df.columns.str.strip().str.lower()
    if 'category' in df.columns: 
        df['transaction_type'] = df['category']
    if 'count' in df.columns: 
        df['transaction_count'] = df['count']
    elif 'transaction_count' in df.columns:
        df['count'] = df['transaction_count']
    df['state'] = df['state'].str.lower()
    return df

@st.cache_data
def load_district_data(state_name):
    query = text("SELECT * FROM map_transaction WHERE state = :state")
    df = pd.read_sql(query, engine, params={"state": state_name})
    df.columns = df.columns.str.strip().str.lower()
    if 'count' in df.columns and 'transaction_count' not in df.columns:
        df['transaction_count'] = df['count']
    elif 'transaction_count' in df.columns and 'count' not in df.columns:
        df['count'] = df['transaction_count']
    return df

@st.cache_data
def load_pincode_data(state_name):
    query = text("SELECT * FROM top_transaction_pincode WHERE state = :state")
    df = pd.read_sql(query, engine, params={"state": state_name})
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_base_data()

# ==========================================
# 6. FORMATTING UTILITIES
# ==========================================
def format_intl_amount(number):
    if number >= 1_000_000_000:
        return f"₹ {number / 1_000_000_000:.2f} B"
    elif number >= 1_000_000:
        return f"₹ {number / 1_000_000:.2f} M"
    elif number >= 1_000:
        return f"₹ {number / 1_000:.1f} K"
    else:
        return f"₹ {number:,.2f}"

def format_intl_qty(number):
    if number >= 1_000_000:
        return f"{number / 1_000_000:.2f} M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f} K"
    else:
        return f"{number:,}"

# ==========================================
# 7. PREMIUM ATTRACTIVE HERO BANNER OVERHAUL
# ==========================================
current_dt = datetime.now().strftime("%A, %B %d, %Y")
st.markdown(f"""
<div class="hero-banner">
    <div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <div class="hero-logo-box">🟪 PhonePe</div>
            <h1 style='margin:0; font-size:2.2rem; font-weight:700; color:white !important; letter-spacing: -0.5px;'>Pulse Intelligence</h1>
        </div>
        <p style='margin:8px 0 0 0; opacity:0.85; font-size:1.05rem; color:white !important; font-weight: 400;'>AI-Powered Transaction Analytics & Enterprise Business Intelligence Platform</p>
    </div>
    <div style='text-align: right; opacity:0.95;'>
        <div style='font-weight:600; font-size:0.95rem; letter-spacing: 0.3px;'>{current_dt}</div>
        <div style='font-size:0.8rem; font-weight:600; margin-top:6px; background:rgba(255,255,255,0.2); padding:4px 14px; border-radius:20px; display:inline-block; border: 1px solid rgba(255,255,255,0.2);'>
            👤 Operator: {st.session_state.username.title()}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown(f"""
<div style="background:rgba(255,255,255,0.08); padding:16px; border-radius:12px; margin-bottom:25px; border:1px solid rgba(255,255,255,0.12);">
    <div style="font-size:0.75rem; text-transform:uppercase; opacity:0.6; font-weight:700; letter-spacing:0.5px;">Active Profile</div>
    <div style="font-size:1.15rem; font-weight:700; margin-top:2px; color:#FFFFFF;">{st.session_state.username.title()}</div>
    <div style="font-size:0.7rem; opacity:0.5; margin-top:1px;">Authorized Data Stream Access</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🗺️ Contextual Domain Filters")
state_list = sorted(df['state'].unique())
selected_state = st.sidebar.selectbox("1. Geographic Territory", state_list)

dist_df = load_district_data(selected_state)
pin_df = load_pincode_data(selected_state)

district_list = sorted(dist_df['district'].unique()) if not dist_df.empty else []
selected_district = st.sidebar.selectbox("2. Micro District Target", ["All Districts"] + district_list)
selected_year = st.sidebar.selectbox("3. Temporal Fiscal Year", sorted(df['year'].unique()))

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Metrics Engine Target")
target_metric = st.sidebar.radio("Active Ledger Target", ["amount", "transaction_count"], 
                                format_func=lambda x: "Value (₹)" if x == "amount" else "Volume Count")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🔒 Terminate User Session", width='stretch'):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# ==========================================
# 9. VISUALS CHART ENGINE (FIXED PLOTLY OVERRIDES)
# ==========================================
def render_pro_chart(data, x, y, title, c_type, color=None):
    seq = px.colors.qualitative.Prism if color is not None else [PRIMARY_COLOR]
    
    if c_type == "Line":
        fig = px.line(data, x=x, y=y, color=color, markers=True, title=title, template="plotly_white", color_discrete_sequence=seq)
    elif c_type == "Bar":
        fig = px.bar(data, x=x, y=y, color=color, title=title, template="plotly_white", color_discrete_sequence=seq)
    elif c_type == "Area":
        fig = px.area(data, x=x, y=y, color=color, title=title, template="plotly_white", color_discrete_sequence=seq)
    else: 
        if color in data.columns and data[color].dtype != 'object':
            data[color] = data[color].astype(str)
        fig = px.scatter(data, x=x, y=y, color=color, title=title, template="plotly_white", color_discrete_sequence=seq)
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",  
        font_family="Inter",
        title_font_size=15,
        title_font_color="#1E293B",
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(bgcolor="rgba(255,255,255,0.7)", bordercolor="#E2E8F0", borderwidth=1)
    )
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0", title="")
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0", title="")
    
    # --- FIXED ASH OVERRIDES LOGIC ---
    fig.show(config={'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d'], 'displayModeBar': 'hover'})
    return fig

# ==========================================
# 10. CENTRAL RUNTIME NAVIGATION FRAMEWORK
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📉 Core Dashboard", 
    "🌍 India Heatmap", 
    "🧠 AI Analytics Hub", 
    "📊 Advanced Statistics",
    "🔮 Forecasting", 
    "📂 SQL Intelligence"
])

# ---- TAB 1: CORE DASHBOARD ----
with tab1:
    if selected_district == "All Districts":
        f_df = df[(df['state'] == selected_state) & (df['year'] == selected_year)]
        header_text = f"Context Overview: {selected_state.title()}"
    else:
        f_df = dist_df[(dist_df['district'] == selected_district) & (dist_df['year'] == selected_year)]
        header_text = f"Micro District Deep Dive: {selected_district.title()}"

    st.subheader(header_text)
    
    if not f_df.empty:
        total_amt = f_df['amount'].sum()
        cnt_col = 'count' if 'count' in f_df.columns else 'transaction_count'
        total_vol = f_df[cnt_col].sum()
        avg_ticket = total_amt / total_vol if total_vol > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="bi-kpi-card">
                <div class="kpi-title">💰 Context-Specific Value</div>
                <div class="kpi-value">{format_intl_amount(total_amt)}</div>
                <div class="kpi-subtext">Selected Domain Yield</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="bi-kpi-card">
                <div class="kpi-title">📈 Context-Specific Volume</div>
                <div class="kpi-value">{format_intl_qty(total_vol)}</div>
                <div class="kpi-subtext">Selected Segment Inflows</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="bi-kpi-card">
                <div class="kpi-title">🛒 Avg. Basket Ticket Size</div>
                <div class="kpi-value">₹ {avg_ticket:,.2f}</div>
                <div class="kpi-subtext">Ticket Breakdown Value</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col_chart, col_pincode = st.columns([3, 2])
    
    with col_chart:
        chart_choice = st.selectbox("Chart Type", ["Area", "Line", "Bar"], key="t1_viz")
        year_data = df[df['state'] == selected_state].groupby('year')[target_metric].sum().reset_index()
        st.plotly_chart(render_pro_chart(year_data, 'year', target_metric, 
                                        f"Macro Dynamic Trend Over Time: {selected_state.title()}", chart_choice), 
                        width='stretch')

    with col_pincode:
        st.markdown("##### 📍 Top 10 High-Velocity Pincodes")
        if not pin_df.empty:
            top_pins = pin_df[pin_df['year'] == selected_year].sort_values(by='amount', ascending=False).head(10).copy()
            top_pins['amount'] = top_pins['amount'].apply(format_intl_amount)
            top_pins['count'] = top_pins['count'].apply(format_intl_qty)
            
            st.dataframe(top_pins[['pincode', 'count', 'amount']], 
                         width='stretch', hide_index=True)
        else:
            st.info("Pincode distribution metrics unavailable inside this selected geographical bounds.")

# ---- TAB 2: INDIA HEATMAP ----
with tab2:
    st.subheader("🌍 National Transaction Density Heatmap")

    df['state_clean'] = df['state'].str.replace("-", " ", regex=False).str.replace("&", "and", regex=False).str.strip().str.title()
    state_mapping = {"Andaman And Nicobar Islands": "Andaman and Nicobar Islands", "Nct Of Delhi": "Delhi", "Jammu And Kashmir": "Jammu & Kashmir"}
    df['state_clean'] = df['state_clean'].replace(state_mapping)

    geo_path = os.path.join(os.path.dirname(__file__), "india_states.geojson")

    try:
        with open(geo_path) as f:
            geojson = json.load(f)

        KEY = next((k for k in ['ST_NM', 'state', 'NAME_1', 'name'] if k in geojson['features'][0]['properties']), None)

        if KEY:
            map_data = df.groupby('state_clean')[target_metric].sum().reset_index()

            fig_map = px.choropleth(map_data, geojson=geojson, featureidkey=f"properties.{KEY}", locations="state_clean", color=target_metric, color_continuous_scale="Turbo")
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)")

            st.plotly_chart(fig_map, width='stretch')

            top_map_state = map_data.sort_values(target_metric, ascending=False).iloc[0]

            st.markdown(f"""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 AUTOMATED GEOGRAPHIC MARKET INSIGHT</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    The national heatmap illustrates clear spatial variations in payment volume across territories. 
                    Currently, <b>{top_map_state['state_clean']}</b> holds the position of national volume leader, acting as a crucial indicator for high-velocity user hubs.
                </div>
            </div>
            """, unsafe_allow_html=True)

    except Exception:
        st.error("GeoJSON mapping structure missing or corrupt from root runtime directory path environment.")

# ---- TAB 3: AI ANALYTICS HUB ----
with tab3:
    st.subheader("🧠 Multi-Dimensional Cluster Segmentation")
    if not dist_df.empty:
        cluster_df = dist_df.groupby('district').agg({'amount': 'sum', 'count': 'sum'}).reset_index()
        X = StandardScaler().fit_transform(cluster_df[['amount', 'count']])
        cluster_df['cluster'] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
        
        st.plotly_chart(render_pro_chart(cluster_df, 'count', 'amount', "District Structural Tier Separation Clustering", "Scatter", color='cluster'), width='stretch')
        
        st.markdown("""
        <div class="ai-insight-panel">
            <div class="ai-header">🤖 K-MEANS UNSUPERVISED METRIC INFERENCE</div>
            <div style="font-size:0.95rem; line-height:1.5;">
                Districts are categorized into three operational segments based on flow velocity and underlying volume. 
                High-yield clusters grouped near the top right suggest ideal environments for prioritizing high-impact merchant onboarding and resource deployment.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Agglomerative Hierarchical Analytics Lineage")
        if len(cluster_df) >= 2:
            linked = linkage(cluster_df[['amount', 'count']], method='ward')
            st.success("Hierarchical clustering matrix linkages parsed and resolved successfully.")
            fig_dendro = px.bar(cluster_df.sort_values(by='amount', ascending=False), x='district', y='amount', title="Volume Hierarchical Profile Segmentation View")
            st.plotly_chart(fig_dendro, width='stretch')
            
            st.markdown("""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 LINKAGE STRUCTURAL ANALYSIS</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    This linkage framework assesses structural similarity markers across commercial districts. 
                    Tracking these localized customer similarities helps identify regions displaying consistent digital behaviors.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Insufficient entries inside contextual slice to establish linkage chains.")
    else:
        st.info("No district metrics loaded for execution of structural clustering modules.")

# ---- TAB 4: ADVANCED STATISTICS ----
with tab4:
    st.subheader("📊 Scientific Hypothesis Verification & Statistical Hub")

    stat1, stat2, stat3, stat4, stat5 = st.tabs([
        "🔬 Analysis of Variance (ANOVA)",
        "🧪 Two-Sample T-Test",
        "🧮 Chi-Square Independence Matrix",
        "📈 Multivariable Regression Line",
        "🧬 Dimension Variance Decomp (PCA)"
    ])

    # ANOVA
    with stat1:
        top_states = df.groupby("state")["amount"].sum().sort_values(ascending=False).head(10).index
        groups = [df[df["state"] == s]["amount"].dropna() for s in top_states]

        if len(groups) > 1 and all(len(g) > 1 for g in groups):
            f_stat, p_val = f_oneway(*groups)
            c1, c2 = st.columns(2)
            c1.metric("F-Distribution Ratio Score", f"{f_stat:.4f}" if not np.isnan(f_stat) else "N/A")
            c2.metric("P-Value Probability Alpha", f"{p_val:.8f}" if not np.isnan(p_val) else "N/A")

            if not np.isnan(p_val) and p_val < 0.05:
                st.success("Significant Variance Found: True.")
            
            st.markdown("""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 SIGNIFICANCE TESTING FEEDBACK</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    The F-statistic gauges revenue variance differences among the top ten regions. 
                    A low P-value (&lt;0.05) confirms that these performance variances represent structurally significant differences rather than random noise, 
                    supporting the use of distinct, regionalized product frameworks.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Data matrices too sparse across cross-sections to determine variance ratios.")

    # T-TEST
    with stat2:
        state_totals = df.groupby("state")["amount"].sum().sort_values()
        bottom = state_totals.head(10).index
        top = state_totals.tail(10).index

        g1 = df[df["state"].isin(top)]["amount"].dropna()
        g2 = df[df["state"].isin(bottom)]["amount"].dropna()

        if len(g1) > 1 and len(g2) > 1:
            t_stat, p_val = ttest_ind(g1, g2, equal_var=False)
            c1, c2 = st.columns(2)
            c1.metric("T-Value Coefficient Matrix", f"{t_stat:.4f}" if not np.isnan(t_stat) else "N/A")
            c2.metric("P-Value Confidence Limit", f"{p_val:.8f}" if not np.isnan(p_val) else "N/A")
            
            st.markdown("""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 GAUSSIAN TWO-SAMPLE GAP INFERENCE</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    This two-sample comparison measures the structural variance gap between the highest and lowest performing state clusters. 
                    The calculated t-statistic provides a metric for the digital gap, indicating locations where infrastructure support is needed most.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Insufficient entries inside target extreme groupings to establish distribution variances.")

    # CHI-SQUARE
    with stat3:
        if 'transaction_type' in df.columns:
            contingency_table = pd.crosstab(df['state'], df['transaction_type'])
            if not contingency_table.empty and contingency_table.size > 4:
                chi2, p, dof, exp = chi2_contingency(contingency_table)
                cx1, cx2 = st.columns(2)
                cx1.metric("Chi-Square Test Score Statistic", f"{chi2:.2f}")
                cx2.metric("Asymptotic P-Value Value", f"{p:.8f}")
                
                st.markdown("""
                <div class="ai-insight-panel">
                    <div class="ai-header">🤖 CATEGORICAL DISTRIBUTION ANALYSIS</div>
                    <div style="font-size:0.95rem; line-height:1.5;">
                        This test evaluates whether preference for payment categories is statistically linked to geographic location. 
                        A significant p-value implies that consumer choice profiles change based on regional trends, suggesting that merchant onboarding choices should be tailored to local demand.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Cross-tabulation framework results are flat.")
        else:
            st.info("Categorical transactional descriptors missing from loaded dataset columns.")

    # REGRESSION
    with stat4:
        reg_df = df[["year", "quarter", "transaction_count", "amount"]].dropna()
        if len(reg_df) > 10:
            X_reg = reg_df[["year", "quarter", "transaction_count"]]
            y_reg = reg_df["amount"]

            X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
            model_linear = LinearRegression()
            model_linear.fit(X_train, y_train)

            score = r2_score(y_test, model_linear.predict(X_test))
            st.metric("R² Score Coefficient (Explained Variance Mapping)", f"{score:.4f}")
            st.progress(float(max(0.0, min(score, 1.0))))
            
            st.markdown("""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 REGRESSION MODEL ESTIMATION FEEDBACK</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    The $R^2$ score indicates how well changes in transaction timing and volume explain overall transacted value. 
                    A higher value suggests stronger financial consistency, offering dependable parameters for quarterly cash flow projections.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Feature sets row count insufficient to construct standard split-sample linear lines.")

    # PCA
    with stat5:
        pca_features = df[["year", "quarter", "transaction_count", "amount"]].dropna()

        if len(pca_features) > 5:
            scaled = StandardScaler().fit_transform(pca_features)
            pca = PCA()
            pca.fit(scaled)

            pca_df = pd.DataFrame({
                "Component": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
                "Variance Ratio": pca.explained_variance_ratio_ * 100
            })

            fig_pca = px.bar(pca_df, x="Component", y="Variance Ratio", title="Information Retention Ratio by Principal Components", template="plotly_white", color_discrete_sequence=[PRIMARY_COLOR])
            st.plotly_chart(fig_pca, width='stretch')
            
            st.markdown("""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 ORTHOGONAL DIMENSIONAL VARIANCE ANALYSIS</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    PCA condenses multiple operational variables down into primary underlying factors. 
                    The scree bar distribution charts the information retention rate per principal component, highlighting the primary metrics influencing core ledger growth.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Data footprint density too low to resolve structural eigenvector matrix reductions.")

# ---- TAB 5: FORECASTING (UPGRADED EXECUTIVE LAYOUT) ----
with tab5:
    st.subheader("🔮 Predictive Revenue Forecasting Engine")
    
    # 1. Cleaner Controls Area
    forecast_model = st.radio("Select Mathematical Engine Strategy", ["Polynomial Regression", "ARIMA Modeling Engine"], horizontal=True, key="engine_select")
    t4_choice = st.selectbox("Projection Presentation Mode", ["Line", "Area"], key="t4_select")
    
    all_y = df.groupby('year')[target_metric].sum().reset_index()
    
    if len(all_y) >= 2:
        last_recorded_year = int(all_y["year"].max())
        future_years = list(range(last_recorded_year + 1, last_recorded_year + 7))
        future = pd.DataFrame({'year': future_years})
        
        poly_pipeline = make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(all_y[['year']], all_y[target_metric])
        hist_predictions = poly_pipeline.predict(all_y[['year']])
        calculated_mae = mean_absolute_error(all_y[target_metric], hist_predictions)
        
        if "Polynomial" in forecast_model:
            future[target_metric] = poly_pipeline.predict(future)
        else:
            try:
                from statsmodels.tsa.arima.model import ARIMA
                ts_model = ARIMA(all_y[target_metric].values, order=(1, 1, 0))
                model_fit = ts_model.fit()
                future[target_metric] = model_fit.forecast(steps=len(future_years))
            except Exception:
                slope, intercept = np.polyfit(all_y['year'].values, all_y[target_metric].values, 1)
                future[target_metric] = [slope * y + intercept for y in future_years]
                
        # Calculate dynamic metrics for the executive row
        last_hist_val = all_y[target_metric].iloc[-1]
        final_fore_val = future[target_metric].iloc[-1]
        growth_pct = ((final_fore_val - last_hist_val) / last_hist_val) * 100
        growth_label = "Positive Expansion" if growth_pct > 0 else "Corrective Flatline"

        # 2. Executive Metric Display Row
        st.markdown("<br>", unsafe_allow_html=True)
        cm1, cm2, cm3 = st.columns(3)
        cm1.metric("Growth Trend Direction", growth_label, f"{growth_pct:+.2f}%")
        cm2.metric(f"Horizon Value Projection ({future_years[-1]})", format_intl_amount(final_fore_val) if target_metric == 'amount' else format_intl_qty(final_fore_val))
        cm3.metric("Active Forecasting Engine", forecast_model.split()[0])
        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Large Clear Visual Chart Block
        combined = pd.concat([all_y.assign(Status='Historical'), future.assign(Status='Forecast')])
        st.plotly_chart(render_pro_chart(combined, 'year', target_metric, f"Forward Trend Projections: Year Horizon {future_years[-1]}", t4_choice, color='Status'), width='stretch')
        
        # 4. Standard Business Expander
        st.markdown(f"""
        <div class="ai-insight-panel">
            <div class="ai-header">🤖 TIME-SERIES PREDICTIVE INSIGHTS PANEL</div>
            <div style="font-size:0.95rem; line-height:1.5;">
                Based on historical growth trends, future performance projections indicate a <b>{"steady expansion" if growth_pct > 0 else "market correction"}</b> trajectory over the upcoming fiscal periods through to <b>{future_years[-1]}</b>. These indicators provide helpful guideboards for managing regional market expectations and scaling processing capacities.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Insufficient continuous historical baseline timelines to fit structural auto-regressive prediction pathways.")

# ---- TAB 6: SQL INTELLIGENCE (SUB-TABBED DATA SEPARATION) ----
with tab6:
    st.subheader("📂 Real-Time Database Analytical Queries")
    t5_choice = st.selectbox("Visual Aggregation Mode Style", ["Bar", "Line"], key="t5_style")
    
    top_states_raw = pd.read_sql("SELECT state, SUM(amount) as total FROM aggregated_transaction GROUP BY state ORDER BY total DESC LIMIT 10", engine)
    cat_perf_raw = pd.read_sql("SELECT category, SUM(amount) as total FROM aggregated_transaction GROUP BY category ORDER BY total DESC", engine)

    # Clean multi-tab architecture separating data views
    sql_subtab1, sql_subtab2 = st.tabs(["🗺️ Geographic Performance Analysis", "🏷️ Product Stream Split Analysis"])

    # Subtab 1: State Performance Matrix
    with sql_subtab1:
        st.markdown("##### **Top Contributing Jurisdictions**")
        if not top_states_raw.empty:
            st.plotly_chart(render_pro_chart(top_states_raw, 'state', 'total', "Top 10 High-Revenue States Summary", t5_choice), width='stretch')
            
            # Display only top 5 rows to minimize screen clutter
            top_states_disp = top_states_raw.copy()
            top_states_disp['total'] = top_states_disp['total'].apply(format_intl_amount)
            st.dataframe(top_states_disp.head(5), width='stretch', hide_index=True)
            
            st.markdown("#### 📋 Complete States Dataset Result Matrix")
            st.dataframe(top_states_disp, width='stretch', hide_index=True)

            st.markdown(f"""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 GEOGRAPHIC LEDGER INTERPRETATION</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    Geographic transaction logs show that <b>{top_states_raw.iloc[0]['state'].title()}</b> contributes the highest overall volume to ledger inflows. Focusing resource allocation on these key areas helps ensure strong investment returns.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Subtab 2: Category Stream Performance Matrix
    with sql_subtab2:
        st.markdown("##### **Product Stream Categorical Split**")
        if not cat_perf_raw.empty:
            st.plotly_chart(render_pro_chart(cat_perf_raw, 'category', 'total', "Transaction Volume Split by Product Stream", t5_choice), width='stretch')
            
            # Display only top 5 rows to minimize screen clutter
            cat_perf_disp = cat_perf_raw.copy()
            cat_perf_disp['total'] = cat_perf_disp['total'].apply(format_intl_amount)
            st.dataframe(cat_perf_disp.head(5), width='stretch', hide_index=True)
            
            st.markdown("#### 📋 Complete Categories Dataset Result Matrix")
            st.dataframe(cat_perf_disp, width='stretch', hide_index=True)

            st.markdown(f"""
            <div class="ai-insight-panel">
                <div class="ai-header">🤖 SEGMENT BREAKDOWN INTERPRETATION</div>
                <div style="font-size:0.95rem; line-height:1.5;">
                    Product performance logs indicate that <b>{cat_perf_raw.iloc[0]['category'].title()}</b> transactions serve as the primary driver of platform value. Aligning marketing campaigns with these user preferences supports consistent platform engagement.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 11. ENTERPRISE FOOTER CONTROL BAR
# ==========================================
st.sidebar.markdown("---")
st.sidebar.write("📤 **Data Export Framework**")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📩 Download Complete Dataset Report", data=csv, file_name=f"PhonePe_Insights_{selected_year}.csv", mime='text/csv')
st.sidebar.caption("Data Source: Multi-Level PhonePe Analytics (MySQL Enterprise)")

st.markdown(f"""
<hr style="border-color:rgba(0,0,0,0.05); margin-top:50px;">
<div style="text-align:center; color:#94A3B8; font-size:0.85rem; padding:10px 0; font-weight:500;">
    <b>PhonePe Pulse Enterprise Portal v6.0</b> | Built with Python • SQL • Streamlit • Machine Learning Frameworks <br>
    &copy; 2026 <b>Heena Kousar</b> | All Rights Reserved
</div>
""", unsafe_allow_html=True)