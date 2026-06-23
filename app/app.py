import streamlit as st
import pandas as pd
import plotly.express as px
import json, os, io, hashlib
import numpy as np
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================================
# 1. UI CONFIGURATION (MUST BE FIRST ACTION)
# ==========================================
st.set_page_config(page_title="PhonePe Intelligence Pro", page_icon="📱", layout="wide")

PRIMARY_COLOR = "#5F259F" 
SECONDARY_COLOR = "#F4F7F9" 

# ==========================================
# 2. GLOBAL CSS CUSTOM INJECTIONS
# ==========================================
st.markdown(f"""
<style>
/* --- HIDE AUTOMATIC MULTIPAGE SIDEBAR NAVIGATION MENU --- */
[data-testid="stSidebarNav"] {{
    display: none !important;
}}

/* Main Background */
[data-testid="stAppViewContainer"] {{
    background-color: {SECONDARY_COLOR};
}}

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {{
    background-color: {PRIMARY_COLOR};
}}


/* Sidebar Text and Labels to White */
[data-testid="stSidebar"] .stMarkdown,  
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] label {{
    color: white !important;
}}

/* DOWNLOAD BUTTON STYLING */
div.stDownloadButton > button {{
    background-color: white !important;
    color: black !important; 
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    width: 100%;
}}

div.stDownloadButton > button p {{
    color: black !important;
    font-weight: normal !important;
}}

div.stDownloadButton > button:hover {{
    background-color: #f0f0f0 !important;
    border-color: {PRIMARY_COLOR};
}}

/* Metric Card Styling */
.stMetric {{
    background: white; 
    padding: 20px; 
    border-radius: 10px; 
    border: 1px solid #E0E0E0;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
}}

.insight-box {{
    background-color: #ffffff; padding: 20px; border-radius: 8px;
    border-left: 5px solid {PRIMARY_COLOR}; margin: 15px 0;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}}

h1, h2, h3 {{color: {PRIMARY_COLOR};}}
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

# Fixed local baseline configurations
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
        st.error(f"Error synchronization database: {e}")

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
                    login_clicked = st.form_submit_button("Authenticate Access", use_container_width=True)
                    
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
                    register_clicked = st.form_submit_button("Register New User", use_container_width=True)
                    
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
    else:
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

# --- BRANDING HEADER ---
st.markdown("""
<div style='text-align:center'>
<img src="https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png" width="160">
<h2 style='margin-top: -10px; font-weight: 700;'>AI-Powered Transaction Insights Platform</h2>
</div>
<hr style="margin-bottom: 25px;">
""", unsafe_allow_html=True)

# ==========================================
# 7. EXECUTIVE INTELLIGENCE SUMMARY BAR
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("States Analysed", df["state"].nunique())
with col2:
    st.metric("Total Transactions", format_intl_qty(df["transaction_count"].sum()))
with col3:
    st.metric("Aggregate Value", format_intl_amount(df["amount"].sum()))
with col4:
    st.metric("Transaction Categories", df["transaction_type"].nunique() if "transaction_type" in df.columns else df["category"].nunique())

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 8. SIDEBAR CONTROLS (FIXED ACCESSIBLE TEXT)
# ==========================================
st.sidebar.markdown(f"### 👤 Active Profile: **{st.session_state.username.title()}**")
st.sidebar.markdown("---")

state_list = sorted(df['state'].unique())
selected_state = st.sidebar.selectbox("🗺️ 1. State Context Selection", state_list)

dist_df = load_district_data(selected_state)
pin_df = load_pincode_data(selected_state)

district_list = sorted(dist_df['district'].unique()) if not dist_df.empty else []
selected_district = st.sidebar.selectbox("🔍 2. District Filter", ["All Districts"] + district_list)

selected_year = st.sidebar.selectbox("📅 3. Fiscal Year Focus", sorted(df['year'].unique()))

st.sidebar.markdown("---")
target_metric = st.sidebar.radio("📊 Target Display Metric", ["amount", "transaction_count"], 
                                format_func=lambda x: "Value (₹)" if x == "amount" else "Volume Count")

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
if st.sidebar.button("🔒 Terminate User Session", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
    
# ==========================================
# 9. VISUALS CHART ENGINE
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
    
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
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
            st.metric("Context-Specific Value", format_intl_amount(total_amt))
        with c2:
            st.metric("Context-Specific Volume", format_intl_qty(total_vol))
        with c3:
            st.metric("Avg. Basket Ticket Size", f"₹ {avg_ticket:,.2f}")

    st.markdown("---")
    col_chart, col_pincode = st.columns([3, 2])
    
    with col_chart:
        chart_choice = st.selectbox("Chart Type", ["Area", "Line", "Bar"], key="t1_viz")
        year_data = df[df['state'] == selected_state].groupby('year')[target_metric].sum().reset_index()
        st.plotly_chart(render_pro_chart(year_data, 'year', target_metric, 
                                        f"Macro Dynamic Trend Over Time: {selected_state.title()}", chart_choice), 
                        use_container_width=True)

    with col_pincode:
        st.markdown("##### 📍 Top 10 High-Velocity Pincodes")
        if not pin_df.empty:
            top_pins = pin_df[pin_df['year'] == selected_year].sort_values(by='amount', ascending=False).head(10).copy()
            top_pins['amount'] = top_pins['amount'].apply(format_intl_amount)
            top_pins['count'] = top_pins['count'].apply(format_intl_qty)
            
            st.dataframe(top_pins[['pincode', 'count', 'amount']], 
                         use_container_width=True, hide_index=True)
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

            fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0))

            st.plotly_chart(fig_map, use_container_width=True)

            

            top_map_state = map_data.sort_values(target_metric, ascending=False).iloc[0]

            

            with st.expander("💡 View Geographic Market Insight", expanded=True):

                st.markdown(f"""

                The national heatmap illustrates clear spatial variations in payment volume across territories. 

                Currently, **{top_map_state['state_clean']}** holds the position of national volume leader, acting as a crucial indicator for high-velocity user hubs.

                """)

    except Exception:

        st.error("GeoJSON mapping structure missing or corrupt from root runtime directory path environment.")
# ---- TAB 3: AI ANALYTICS HUB ----
with tab3:
    st.subheader("🧠 Multi-Dimensional Cluster Segmentation")
    if not dist_df.empty:
        cluster_df = dist_df.groupby('district').agg({'amount': 'sum', 'count': 'sum'}).reset_index()
        X = StandardScaler().fit_transform(cluster_df[['amount', 'count']])
        cluster_df['cluster'] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
        
        st.plotly_chart(render_pro_chart(cluster_df, 'count', 'amount', "District Structural Tier Separation Clustering", "Scatter", color='cluster'), use_container_width=True)
        
        with st.expander("💡 View K-Means Diagnostic Insights", expanded=True):
            st.markdown("""
            Districts are categorized into three operational segments based on flow velocity and underlying volume. 
            High-yield clusters grouped near the top right suggest ideal environments for prioritizing high-impact merchant onboarding and resource deployment.
            """)
        
        with st.expander("📊 Agglomerative Hierarchical Analytics Lineage"):
            from scipy.cluster.hierarchy import linkage
            if len(cluster_df) >= 2:
                linked = linkage(cluster_df[['amount', 'count']], method='ward')
                st.success("Hierarchical clustering matrix linkages parsed and resolved successfully.")
                fig_dendro = px.bar(cluster_df.sort_values(by='amount', ascending=False), x='district', y='amount', title="Volume Hierarchical Profile Segmentation View")
                st.plotly_chart(fig_dendro, use_container_width=True)
                
                with st.expander("💡 View Hierarchical Structural Insight"):
                    st.markdown("""
                    This linkage framework assesses structural similarity markers across commercial districts. 
                    Tracking these localized customer similarities helps identify regions displaying consistent digital behaviors.
                    """)
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
        from scipy.stats import f_oneway
        top_states = df.groupby("state")["amount"].sum().sort_values(ascending=False).head(10).index
        groups = [df[df["state"] == s]["amount"].dropna() for s in top_states]

        if len(groups) > 1 and all(len(g) > 1 for g in groups):
            f_stat, p_val = f_oneway(*groups)
            c1, c2 = st.columns(2)
            c1.metric("F-Distribution Ratio Score", f"{f_stat:.4f}" if not np.isnan(f_stat) else "N/A")
            c2.metric("P-Value Probability Alpha", f"{p_val:.8f}" if not np.isnan(p_val) else "N/A")

            if not np.isnan(p_val) and p_val < 0.05:
                st.success("Significant Variance Found: True.")
            
            with st.expander("💡 View ANOVA Business Insights", expanded=True):
                st.markdown("""
                The F-statistic gauges revenue variance differences among the top ten regions. 
                A low P-value (<0.05) confirms that these performance variances represent structurally significant differences rather than random noise, 
                supporting the use of distinct, regionalized product frameworks.
                """)
        else:
            st.warning("Data matrices too sparse across cross-sections to determine variance ratios.")

    # T-TEST
    with stat2:
        from scipy.stats import ttest_ind
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
            
            with st.expander("💡 View T-Test Business Insights", expanded=True):
                st.markdown("""
                This two-sample comparison measures the structural variance gap between the highest and lowest performing state clusters. 
                The calculated t-statistic provides a metric for the digital gap, indicating locations where infrastructure support is needed most.
                """)
        else:
            st.warning("Insufficient entries inside target extreme groupings to establish distribution variances.")

    # CHI-SQUARE
    with stat3:
        from scipy.stats import chi2_contingency
        if 'transaction_type' in df.columns:
            contingency_table = pd.crosstab(df['state'], df['transaction_type'])
            if not contingency_table.empty and contingency_table.size > 4:
                chi2, p, dof, exp = chi2_contingency(contingency_table)
                cx1, cx2 = st.columns(2)
                cx1.metric("Chi-Square Test Score Statistic", f"{chi2:.2f}")
                cx2.metric("Asymptotic P-Value Value", f"{p:.8f}")
                
                with st.expander("💡 View Categorical Distribution Insights", expanded=True):
                    st.markdown("""
                    This test evaluates whether preference for payment categories is statistically linked to geographic location. 
                    A significant p-value implies that consumer choice profiles change based on regional trends, suggesting that merchant onboarding choices should be tailored to local demand.
                    """)
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
            
            with st.expander("💡 View Regression Pipeline Insights", expanded=True):
                st.markdown("""
                The $R^2$ score indicates how well changes in transaction timing and volume explain overall transacted value. 
                A higher value suggests stronger financial consistency, offering dependable parameters for quarterly cash flow projections.
                """)
        else:
            st.warning("Feature sets row count insufficient to construct standard split-sample linear lines.")

    # PCA
    with stat5:
        from sklearn.decomposition import PCA
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
            st.plotly_chart(fig_pca, use_container_width=True)
            
            with st.expander("💡 View Structural Dimensionality Insights", expanded=True):
                st.markdown("""
                PCA condenses multiple operational variables down into primary underlying factors. 
                The scree bar distribution charts the information retention rate per principal component, highlighting the primary metrics influencing core ledger growth.
                """)
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
        st.plotly_chart(render_pro_chart(combined, 'year', target_metric, f"Forward Trend Projections: Year Horizon {future_years[-1]}", t4_choice, color='Status'), use_container_width=True)
        
        # 4. Standard Business Expander
        with st.expander("💡 View Predictive Intelligence Insights", expanded=True):
            st.markdown(f"Based on historical growth trends, future performance projections indicate a **{'steady expansion' if growth_pct > 0 else 'market correction'}** trajectory over the upcoming fiscal periods through to **{future_years[-1]}**. These indicators provide helpful guideboards for managing regional market expectations and scaling processing capacities.")
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
            st.plotly_chart(render_pro_chart(top_states_raw, 'state', 'total', "Top 10 High-Revenue States Summary", t5_choice), use_container_width=True)
            
            # Display only top 5 rows to minimize screen clutter
            top_states_disp = top_states_raw.copy()
            top_states_disp['total'] = top_states_disp['total'].apply(format_intl_amount)
            st.dataframe(top_states_disp.head(5), use_container_width=True, hide_index=True)
            
            with st.expander("📋 View Complete States Dataset Result Matrix"):
                st.dataframe(top_states_disp, use_container_width=True, hide_index=True)

            with st.expander("💡 View Regional Data Insights", expanded=True):
                st.markdown(f"Geographic transaction logs show that **{top_states_raw.iloc[0]['state'].title()}** contributes the highest overall volume to ledger inflows. Focusing resource allocation on these key areas helps ensure strong investment returns.")

    # Subtab 2: Category Stream Performance Matrix
    with sql_subtab2:
        st.markdown("##### **Product Stream Categorical Split**")
        if not cat_perf_raw.empty:
            st.plotly_chart(render_pro_chart(cat_perf_raw, 'category', 'total', "Transaction Volume Split by Product Stream", t5_choice), use_container_width=True)
            
            # Display only top 5 rows to minimize screen clutter
            cat_perf_disp = cat_perf_raw.copy()
            cat_perf_disp['total'] = cat_perf_disp['total'].apply(format_intl_amount)
            st.dataframe(cat_perf_disp.head(5), use_container_width=True, hide_index=True)
            
            with st.expander("📋 View Complete Categories Dataset Result Matrix"):
                st.dataframe(cat_perf_disp, use_container_width=True, hide_index=True)

            with st.expander("💡 View Product Stream Insights", expanded=True):
                st.markdown(f"Product performance logs indicate that **{cat_perf_raw.iloc[0]['category'].title()}** transactions serve as the primary driver of platform value. Aligning marketing campaigns with these user preferences supports consistent platform engagement.")
# ==========================================
# 11. FOOTER CONTROL BAR
# ==========================================
st.sidebar.markdown("---")
st.sidebar.write("📤 **Data Export Framework**")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📩 Download Complete Dataset Report", data=csv, file_name=f"PhonePe_Insights_{selected_year}.csv", mime='text/csv')
st.sidebar.caption("Data Source: Multi-Level PhonePe Analytics (MySQL Enterprise)")
st.markdown("<hr><center style='color:#777777; font-size:13px;'>Developed by Heena Kousar | Advanced Management Edition v5.0</center>", unsafe_allow_html=True)