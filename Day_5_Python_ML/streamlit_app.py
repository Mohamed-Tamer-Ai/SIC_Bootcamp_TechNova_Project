# ============================================================
# TECHNOVA CUSTOMER CHURN PREDICTOR — STREAMLIT WEB APPLICATION
# SIC Bootcamp | Day 5: Machine Learning Deployment
# ============================================================
# This Streamlit app loads a pre-trained Logistic Regression model
# and its StandardScaler, then provides an interactive UI for
# instructors and students to predict customer churn risk.
# ============================================================

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os


# --- PAGE CONFIGURATION ---
# Must be the FIRST Streamlit command in the script.
# Sets the browser tab title, favicon, and page layout.
st.set_page_config(
    page_title="TechNova Churn Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- CUSTOM CSS STYLING ---
# Inject custom CSS to enhance the visual appearance of the app.
# This creates a premium feel with gradient backgrounds, shadows, and spacing.
st.markdown("""
    <style>
    /* Main page background */
    .main { background-color: #f4f6f9; }
    
    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Result cards styling */
    .result-card {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .high-risk {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        color: white;
    }
    .low-risk {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)


# --- HEADER SECTION ---
# Displays the app title and a brief description using custom HTML.
st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size:2.5em;">🔮 TechNova Churn Predictor</h1>
        <p style="margin:5px 0 0; font-size:1.2em; opacity:0.9;">
            Powered by Machine Learning — Predict customer churn risk in real time
        </p>
    </div>
""", unsafe_allow_html=True)


# --- MODEL LOADING ---
# Load the pre-trained Logistic Regression model and its StandardScaler.
# Both were saved using joblib during the EDA notebook training process.
# The scaler is CRITICAL — input data must be scaled the SAME WAY as training data.
@st.cache_resource  # Cache the model so it's only loaded once (performance optimization)
def load_model():
    """Load the trained model and scaler from the models/ directory."""
    model_path = os.path.join('models', 'churn_model.pkl')
    scaler_path = os.path.join('models', 'scaler.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

try:
    model, scaler = load_model()
except FileNotFoundError:
    st.error("⚠️ Model files not found in `models/` folder. Please run the EDA notebook first.")
    st.stop()


# --- SIDEBAR: USER INPUT FORM ---
# The sidebar collects customer features needed for the prediction.
# Each input corresponds to a feature the model was trained on.
with st.sidebar:
    st.markdown("## 👤 Customer Profile")
    st.markdown("---")
    
    # Age slider: integer input between 18-100
    age = st.slider(
        "🎂 Customer Age", 
        min_value=18, max_value=100, value=35,
        help="The age of the customer in years"
    )
    
    st.markdown("---")
    st.markdown("## 🛒 Shopping Behavior")
    
    # Total lifetime spending: float input
    total_spent = st.number_input(
        "💵 Total Lifetime Spent ($)", 
        min_value=0.0, max_value=100000.0, value=2500.0, step=100.0,
        help="Total amount the customer has spent across all orders"
    )
    
    # Average discount received: percentage slider
    avg_discount = st.slider(
        "🏷️ Average Discount (%)", 
        min_value=0.0, max_value=50.0, value=5.0, step=0.5,
        help="Average discount percentage the customer received"
    ) / 100  # Convert percentage to decimal for the model
    
    # Days since last order: measures recency
    days_since = st.number_input(
        "📅 Days Since Last Order", 
        min_value=0, max_value=2000, value=60, step=5,
        help="Number of days since the customer's most recent order"
    )
    
    # Total number of distinct orders
    total_orders = st.number_input(
        "📦 Total Number of Orders", 
        min_value=1, max_value=50, value=5, step=1,
        help="How many separate orders the customer has placed"
    )
    
    # Average profit per order
    avg_profit = st.number_input(
        "📊 Avg Profit per Order ($)", 
        min_value=-500.0, max_value=5000.0, value=150.0, step=10.0,
        help="Average profit generated per order from this customer"
    )
    
    st.markdown("---")
    
    # Predict button: triggers the ML prediction
    predict_btn = st.button(
        "🚀 Predict Churn Risk", 
        use_container_width=True, 
        type="primary"
    )


# --- MAIN CONTENT: CUSTOMER SUMMARY METRICS ---
# Display the entered values as metric cards for quick visual reference.
st.markdown("### 📋 Customer Summary")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("🎂 Age", f"{age} yrs")
col2.metric("💵 Total Spent", f"${total_spent:,.0f}")
col3.metric("🏷️ Avg Discount", f"{avg_discount:.0%}")
col4.metric("📅 Last Order", f"{days_since} days")
col5.metric("📦 Orders", f"{total_orders}")
col6.metric("📊 Avg Profit", f"${avg_profit:,.0f}")

st.markdown("---")


# --- PREDICTION LOGIC ---
# When the user clicks the predict button, we:
# 1. Create a DataFrame from the input values (matching the training feature order)
# 2. Scale the input using the SAME StandardScaler used during training
# 3. Get the model's prediction (0 or 1) and probability
# 4. Display the result with rich formatting
if predict_btn:
    with st.spinner("🔄 Analyzing customer profile..."):
        
        # Step 1: Prepare input data as a DataFrame
        # IMPORTANT: Column order must EXACTLY match the training features
        input_data = pd.DataFrame([[
            age, total_spent, days_since, total_orders, avg_discount, avg_profit
        ]], columns=['Age', 'Total_Spent', 'Days_Since_Last_Order', 
                     'Total_Orders', 'Avg_Discount', 'Avg_Profit'])
        
        # Step 2: Scale the input using the saved scaler
        input_scaled = scaler.transform(input_data)
        
        # Step 3: Get prediction and probability
        prediction = model.predict(input_scaled)[0]
        churn_probability = model.predict_proba(input_scaled)[0][1]
        retention_probability = 1 - churn_probability
    
    # Step 4: Display Results
    st.markdown("### 🤖 Prediction Results")
    
    if prediction == 1:
        # HIGH RISK — Customer is likely to churn
        st.markdown(f"""
            <div class="result-card high-risk">
                <h2 style="margin:0;">⚠️ HIGH CHURN RISK</h2>
                <h1 style="margin:10px 0; font-size:3em;">{churn_probability:.1%}</h1>
                <p style="font-size:1.1em;">Probability of churning</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show recommended actions in an expander
        with st.expander("📌 Recommended Retention Actions", expanded=True):
            st.markdown("""
            **Immediate Actions Required:**
            1. 📧 Send a personalized retention email with a **15-20% discount** on their favorite category
            2. 📞 Schedule a customer success call within the next **48 hours**
            3. 🎁 Offer a **loyalty reward** or free shipping on the next order
            4. 📊 Review their order history for any unresolved complaints
            """)
    else:
        # LOW RISK — Customer is likely to stay
        st.markdown(f"""
            <div class="result-card low-risk">
                <h2 style="margin:0;">✅ LOW CHURN RISK</h2>
                <h1 style="margin:10px 0; font-size:3em;">{retention_probability:.1%}</h1>
                <p style="font-size:1.1em;">Probability of retention</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📌 Recommended Engagement Actions", expanded=True):
            st.markdown("""
            **Keep This Customer Happy:**
            1. ✉️ Continue regular marketing newsletters
            2. 🏆 Consider enrolling them in the **VIP loyalty program**
            3. 📦 Offer early access to new product launches
            4. 🎯 Cross-sell complementary products based on purchase history
            """)

    # --- PROBABILITY BREAKDOWN ---
    # Show a visual probability bar for both outcomes
    st.markdown("---")
    st.markdown("### 📊 Probability Breakdown")
    prob_col1, prob_col2 = st.columns(2)
    prob_col1.metric("Retention Probability", f"{retention_probability:.1%}")
    prob_col2.metric("Churn Probability", f"{churn_probability:.1%}")
    
    # Progress bar visualization
    st.progress(retention_probability, text=f"Retention confidence: {retention_probability:.1%}")


# --- FOOTER ---
st.markdown("---")
st.caption("🏫 SIC Bootcamp — TechNova Churn Predictor | Built with Streamlit + Scikit-Learn")
