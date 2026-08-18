# ==============================================================================
# TECHNOVA CUSTOMER CHURN PREDICTOR — STREAMLIT WEB APPLICATION
# Science in Code (SIC) Bootcamp | Day 5: Python, EDA & Machine Learning Deployment
# ==============================================================================
# Architecture: Standard Logistic Regression + StandardScaler (Scikit-Learn)
# Input Features: Age, Total_Spent, Days_Since_Last_Order, Total_Orders, Avg_Discount, Avg_Profit
# ==============================================================================

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Set browser tab title, favicon, and wide layout mode for dashboard responsiveness
st.set_page_config(
    page_title="TechNova Churn Predictor | SIC Bootcamp",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING & BRANDING
# ------------------------------------------------------------------------------
# Professional UI aesthetic with dark navy sidebar, clean cards, and gradient banners
st.markdown("""
    <style>
    /* Main app background */
    .main { background-color: #f8fafc; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    
    /* Risk Result Cards */
    .result-card {
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    .high-risk {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white !important;
    }
    .medium-risk {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white !important;
    }
    .low-risk {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: white !important;
    }
    
    /* Header Container Banner */
    .header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #4f46e5 100%);
        padding: 26px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.25);
    }
    .badge {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.88em;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 3. ROBUST ARTIFACTS LOADING (Model, Scaler, Metadata)
# ------------------------------------------------------------------------------
@st.cache_resource
def load_ml_artifacts():
    """
    Loads the trained Logistic Regression model, StandardScaler, and metadata.
    Uses directory resolution relative to this script file to ensure seamless loading.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'models')
    
    model_path = os.path.join(models_dir, 'churn_model.pkl')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    meta_path = os.path.join(models_dir, 'model_metadata.json')
    
    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        # Fallback check in current working directory
        model_path = os.path.join('models', 'churn_model.pkl')
        scaler_path = os.path.join('models', 'scaler.pkl')
        meta_path = os.path.join('models', 'model_metadata.json')
        
    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        return None, None, None
        
    # Load serialized scikit-learn model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
    return model, scaler, metadata

# Initialize artifacts
model, scaler, metadata = load_ml_artifacts()

if model is None or scaler is None:
    st.error("⚠️ Model files (`churn_model.pkl` and `scaler.pkl`) not found in `models/`. Please execute the `TechNova_Python_EDA.ipynb` notebook first.")
    st.stop()

# Extract model properties
model_name = metadata.get('model_name', 'Logistic Regression')
model_acc = metadata.get('accuracy', 0.8188)
model_auc = metadata.get('auc_roc', 0.8815)
FEATURE_COLS = metadata.get('features', ['Age', 'Total_Spent', 'Days_Since_Last_Order', 'Total_Orders', 'Avg_Discount', 'Avg_Profit'])


# ------------------------------------------------------------------------------
# 4. APPLICATION HEADER
# ------------------------------------------------------------------------------
st.markdown(f"""
    <div class="header-container">
        <h1 style="margin:0; font-size:2.4em; font-weight:800;">🔮 TechNova Customer Churn Predictor</h1>
        <p style="margin:6px 0 0; font-size:1.15em; opacity:0.95;">
            Science in Code (SIC) Bootcamp — Day 5: Python, EDA & Machine Learning Deployment
        </p>
        <span class="badge">Model: {model_name} | Accuracy: {model_acc:.2%} | AUC-ROC: {model_auc:.4f}</span>
    </div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 5. NAVIGATION TABS (Interactive Capabilities)
# ------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Single Customer Predictor", 
    "📂 Batch Customer Scoring", 
    "🧠 Model Evaluation & Feature Insights"
])


# ==============================================================================
# TAB 1: SINGLE CUSTOMER PREDICTION & RISK SIMULATION
# ==============================================================================
with tab1:
    col_input, col_output = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("### 👤 Customer Profile & Behavioral Inputs")
        st.caption("Adjust the sliders below or select a pre-configured customer profile archetype:")
        
        # Archetype Preset Selector for rapid in-class demonstrations
        preset = st.selectbox(
            "⚡ Quick Profile Archetypes",
            [
                "Custom Input", 
                "🟢 Highly Loyal Active Customer (High Spend, Recent)", 
                "🔴 At-Risk Inactive Customer (Long Recency, High Discount)", 
                "🟡 Occasional Shopper (Moderate Spend & Frequency)"
            ]
        )
        
        # Load preset default values
        if "Loyal Active" in preset:
            d_age, d_spent, d_days, d_orders, d_disc, d_profit = 38, 4500.0, 15, 12, 5.0, 220.0
        elif "At-Risk" in preset:
            d_age, d_spent, d_days, d_orders, d_disc, d_profit = 52, 600.0, 850, 2, 25.0, 15.0
        elif "Occasional" in preset:
            d_age, d_spent, d_days, d_orders, d_disc, d_profit = 32, 1800.0, 95, 4, 10.0, 85.0
        else:
            d_age, d_spent, d_days, d_orders, d_disc, d_profit = 35, 2200.0, 60, 5, 5.0, 120.0
            
        c1, c2 = st.columns(2)
        with c1:
            age = st.slider("🎂 Customer Age", min_value=18, max_value=100, value=int(d_age), help="Age in years")
            total_spent = st.number_input("💵 Total Lifetime Spent ($)", min_value=0.0, max_value=100000.0, value=float(d_spent), step=100.0)
            avg_discount_pct = st.slider("🏷️ Average Discount (%)", min_value=0.0, max_value=50.0, value=float(d_disc), step=0.5)
            avg_discount = avg_discount_pct / 100.0  # Convert percentage to decimal
            
        with c2:
            days_since = st.number_input("📅 Days Since Last Order", min_value=0, max_value=2000, value=int(d_days), step=5, help="Recency in days")
            total_orders = st.number_input("📦 Total Number of Orders", min_value=1, max_value=50, value=int(d_orders), step=1)
            avg_profit = st.number_input("📊 Avg Profit per Order ($)", min_value=-500.0, max_value=5000.0, value=float(d_profit), step=10.0)
            
        predict_btn = st.button("🚀 Calculate Churn Probability", type="primary", use_container_width=True)

    with col_output:
        st.markdown("### 📊 Prediction Results & Retention Strategy")
        
        # 1. Structure raw inputs into DataFrame matching the training feature order
        input_df = pd.DataFrame([[
            age, total_spent, days_since, total_orders, avg_discount, avg_profit
        ]], columns=FEATURE_COLS)
        
        # 2. Scale inputs using the fitted StandardScaler
        input_scaled = scaler.transform(input_df)
        
        # 3. Model Inference: Continuous Probability & Binary Classification
        churn_prob = float(model.predict_proba(input_scaled)[0][1])
        retention_prob = 1.0 - churn_prob
        
        # 4. Risk Classification & Action Recommendations
        if churn_prob >= 0.60:
            risk_label = "HIGH CHURN RISK"
            card_style = "high-risk"
            icon = "⚠️"
            rec_header = "🚨 Immediate Retention Actions Required"
            actions = [
                "**Direct VIP Outreach:** Assign a dedicated support specialist within 24-48 hours.",
                "**Comeback Offer:** Send a personalized 15% discount voucher on their most purchased category.",
                "**Friction Analysis:** Review recent transaction records for refund requests or delayed deliveries.",
                "**Free Delivery Perk:** Offer free delivery on their next two orders."
            ]
            arabic_advice = "العميل في مرحلة حرجة ومعرض للمغادرة بنسبة عالية. ينصح بالتدخل السريع وتقديم حافز مباشر لإعادة التفاعل."
        elif churn_prob >= 0.35:
            risk_label = "MODERATE RISK"
            card_style = "medium-risk"
            icon = "⚡"
            rec_header = "💡 Recommended Re-Engagement Actions"
            actions = [
                "**Targeted Newsletter:** Deliver an automated email showcasing trending tech accessories.",
                "**Rewards Reminder:** Alert the customer to expiring loyalty points or discounts.",
                "**Cross-Sell Promo:** Present bundled savings on items related to previous purchases."
            ]
            arabic_advice = "العميل في منطقة متوسطة، يتطلب تنشيط دوري وتذكير بالمكافآت قبل أن تزداد فترة الانقطاع."
        else:
            risk_label = "LOW CHURN RISK (ACTIVE & LOYAL)"
            card_style = "low-risk"
            icon = "✅"
            rec_header = "🌟 Recommended Loyalty & Growth Actions"
            actions = [
                "**VIP Program:** Enroll customer into the TechNova Premier Club.",
                "**Early Access:** Grant 24-hour early access to upcoming product sales and flash events.",
                "**Referral Incentive:** Reward $15 in store credit for every successfully referred friend."
            ]
            arabic_advice = "العميل نشط ومخلص جداً. ركز على برامج الولاء والـ Upselling لتعظيم القيمة الدائمة للعميل (CLV)."
            
        # Display Prediction Badge
        st.markdown(f"""
            <div class="result-card {card_style}">
                <h3 style="margin:0; letter-spacing:1px;">{icon} {risk_label}</h3>
                <h1 style="margin:8px 0; font-size:3.2em; font-weight:800;">{churn_prob:.1%}</h1>
                <p style="margin:0; font-size:1.1em; opacity:0.95;">Estimated Probability of Customer Churn</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Visual Progress Metric
        m1, m2 = st.columns(2)
        m1.metric("Retention Confidence", f"{retention_prob:.1%}")
        m2.metric("Churn Risk Score", f"{churn_prob:.1%}")
        st.progress(churn_prob, text=f"Churn Risk Meter: {churn_prob:.1%}")

# ==============================================================================
# TAB 2: BATCH CUSTOMER SCORING & REPORT EXPORT
# ==============================================================================
with tab2:
    st.markdown("### 📂 Batch Customer Scoring & Report Generator")
    st.caption("Upload a CSV file of customer profiles or test with sample records from the cleaned dataset.")
    
    # Locate dataset_cleaned.csv in Datasets folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_paths = [
        os.path.join(base_dir, '..', 'Datasets', 'dataset_cleaned.csv'),
        os.path.join(base_dir, 'Datasets', 'dataset_cleaned.csv'),
        os.path.join(os.getcwd(), 'Datasets', 'dataset_cleaned.csv'),
        os.path.join(os.getcwd(), 'dataset_cleaned.csv')
    ]
    sample_file = next((p for p in sample_paths if os.path.exists(p)), None)
    
    uploaded_file = st.file_uploader("Upload CSV for Batch Prediction", type=['csv'])
    
    load_sample = False
    if uploaded_file is None and sample_file:
        if st.button("📥 Load Sample Customers from TechNova Cleaned Dataset"):
            load_sample = True
            
    df_to_score = None
    if uploaded_file is not None:
        df_to_score = pd.read_csv(uploaded_file)
    elif load_sample and sample_file:
        raw_df = pd.read_csv(sample_file)
        if 'Revenue' in raw_df.columns:
            df_to_score = raw_df.groupby('CustomerID').agg(
                Age=('Age', 'max'),
                Total_Spent=('Revenue', 'sum'),
                Days_Since_Last_Order=('Days_Since_Last_Order', 'max'),
                Total_Orders=('Total_Orders', 'max'),
                Avg_Discount=('Discount', 'mean'),
                Avg_Profit=('Profit', 'mean')
            ).reset_index().head(100)
        else:
            df_to_score = raw_df.head(100)
            
    if df_to_score is not None:
        missing_cols = [c for c in FEATURE_COLS if c not in df_to_score.columns]
        if missing_cols:
            st.error(f"⚠️ The uploaded dataset is missing required feature columns: {missing_cols}")
        else:
            X_batch = df_to_score[FEATURE_COLS]
            X_batch_scaled = scaler.transform(X_batch)
            
            df_to_score['Churn_Prediction'] = model.predict(X_batch_scaled)
            df_to_score['Churn_Probability'] = model.predict_proba(X_batch_scaled)[:, 1]
            df_to_score['Risk_Tier'] = pd.cut(
                df_to_score['Churn_Probability'], 
                bins=[-0.1, 0.35, 0.60, 1.0], 
                labels=['Low Risk', 'Moderate Risk', 'High Risk']
            )
            
            st.success(f"✅ Successfully scored {len(df_to_score)} customer records!")
            
            # Batch Summary Metrics
            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Total Scored", len(df_to_score))
            b2.metric("High Risk Customers", int((df_to_score['Risk_Tier'] == 'High Risk').sum()))
            b3.metric("Moderate Risk Customers", int((df_to_score['Risk_Tier'] == 'Moderate Risk').sum()))
            b4.metric("Avg Churn Rate", f"{df_to_score['Churn_Probability'].mean():.1%}")
            
            # Display Table
            st.dataframe(
                df_to_score.style.format({
                    'Total_Spent': '${:,.2f}',
                    'Avg_Profit': '${:,.2f}',
                    'Avg_Discount': '{:.1%}',
                    'Churn_Probability': '{:.1%}'
                }),
                use_container_width=True
            )
            
            # Export CSV
            csv_export = df_to_score.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Scored Churn Report (CSV)",
                data=csv_export,
                file_name="TechNova_Customer_Churn_Scored.csv",
                mime="text/csv",
                type="primary"
            )


# ==============================================================================
# TAB 3: LOGISTIC REGRESSION MODEL INTERPRETABILITY & FORMULATION
# ==============================================================================
with tab3:
    st.markdown("### 🧠 Logistic Regression Architecture & Mathematical Insights")
    st.caption("Understand how the Logistic Regression model computes probabilities using learned feature weights.")
    
    col_info1, col_info2 = st.columns([1, 1], gap="large")
    
    with col_info1:
        st.markdown("#### 📋 Model Specifications")
        st.markdown(r"""
        - **Algorithm:** Logistic Regression (`sklearn.linear_model.LogisticRegression`)
        - **Optimization Solver:** L-BFGS (`max_iter=500, random_state=42`)
        - **Feature Preprocessing:** `StandardScaler` (Z-score normalization: $\mu=0, \sigma=1$)
        - **Evaluation Metrics:**
          - **Test Accuracy:** **81.88%**
          - **AUC-ROC Score:** **0.8815**
          - **Decision Threshold:** $P(\text{Churn}) \ge 0.50$
        """)
        
        st.markdown(r"""
        #### 📐 Mathematical Formulation (Sigmoid Logistic Curve)
        The probability of churn is computed using the standard Sigmoid activation function:
        $$P(\text{Churn} = 1) = \frac{1}{1 + e^{-z}}$$
        where the linear combination $z$ is given by:
        $$z = \beta_0 + \beta_1 \cdot \text{Age} + \beta_2 \cdot \text{TotalSpent} + \beta_3 \cdot \text{Recency} + \dots$$
        """)
        
    with col_info2:
        st.markdown("#### 📊 Learned Feature Coefficients ($\beta_i$)")
        
        if hasattr(model, 'coef_'):
            coef_df = pd.DataFrame({
                'Feature': FEATURE_COLS,
                'Weight': model.coef_[0]
            }).sort_values(by='Weight', ascending=False)
            
            fig, ax = plt.subplots(figsize=(8, 4.5))
            colors = ['#ef4444' if w > 0 else '#10b981' for w in coef_df['Weight']]
            sns.barplot(data=coef_df, x='Weight', y='Feature', hue='Feature', palette=colors, legend=False, ax=ax)
            ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
            ax.set_title("Logistic Regression Feature Weights", fontsize=12, fontweight='bold')
            ax.set_xlabel("Impact (Positive = Increases Churn | Negative = Increases Retention)", fontsize=10)
            st.pyplot(fig)
            
            st.info("💡 **Key Business Finding:** **Days_Since_Last_Order** is the single strongest driver of churn. Customers with high lifetime spend and order frequency show strong retention resilience.")


# ------------------------------------------------------------------------------
# 6. FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
st.caption("🎓 **Science in Code (SIC) Data Analysis Bootcamp** | TechNova Retail & Churn Analytics Project")
