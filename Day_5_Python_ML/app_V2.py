import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="TechNova Churn Predictor", page_icon="🚀", layout="centered")

# ============================================================
# LOAD MODEL, SCALER, AND METADATA
# (These are the EXACT objects saved by Section 9 of the notebook:
#  models/churn_model.pkl, models/scaler.pkl, models/model_metadata.json)
# ============================================================
MODELS_DIR = "models"

@st.cache_resource
def load_artifacts():
    model = joblib.load(os.path.join(MODELS_DIR, "churn_model.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    with open(os.path.join(MODELS_DIR, "model_metadata.json"), "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return model, scaler, metadata

try:
    model, scaler, metadata = load_artifacts()
except FileNotFoundError:
    st.error(
        "❌ Could not find the model files. Make sure the `models/` folder "
        "(containing churn_model.pkl, scaler.pkl, model_metadata.json) is in the "
        "same directory as this app."
    )
    st.stop()

# feature_names, in the EXACT order used during training (from the notebook)
feature_names = metadata["features"]  # ['Age', 'Total_Spent', 'Days_Since_Last_Order', 'Total_Orders', 'Avg_Discount', 'Avg_Profit']

# ============================================================
# HEADER
# ============================================================
st.title("🚀 TechNova Customer Churn Predictor")
st.write(
    "Enter a customer's profile below to predict whether they are likely to "
    "**churn (leave)** or remain **active**, using the trained Logistic Regression model."
)

with st.expander("ℹ️ About this model"):
    st.write(f"**Model:** {metadata['model_name']}")
    st.write(f"**Test Accuracy:** {metadata['accuracy']:.2%}")
    st.write(f"**AUC-ROC Score:** {metadata['auc_roc']:.4f}")
    st.write("**Features used (in order):**", ", ".join(feature_names))

st.divider()

# ============================================================
# USER INPUT FORM
# (Matches customer_df columns exactly, as produced by Section 5:
#  Age, Total_Spent, Days_Since_Last_Order, Total_Orders, Avg_Discount, Avg_Profit)
# ============================================================
st.subheader("📋 Customer Profile")

col1, col2 = st.columns(2)

with col1:
    Age = st.number_input(
        "Age", min_value=18, max_value=100, value=35, step=1,
        help="Customer age (cleaned range in training data: 18–100)"
    )
    Total_Spent = st.number_input(
        "Total Spent ($)", min_value=0.0, value=1500.0, step=50.0,
        help="Sum of Revenue across all of the customer's orders (lifetime spend)"
    )
    Days_Since_Last_Order = st.number_input(
        "Days Since Last Order", min_value=0, value=180, step=1,
        help="Recency: number of days since the customer's last order"
    )

with col2:
    Total_Orders = st.number_input(
        "Total Orders", min_value=0, value=5, step=1,
        help="Frequency: total number of orders placed"
    )
    Avg_Discount = st.number_input(
        "Average Discount", min_value=0.0, max_value=1.0, value=0.05, step=0.01,
        format="%.2f", help="Average discount rate applied across the customer's orders (0.0–1.0)"
    )
    Avg_Profit = st.number_input(
        "Average Profit per Order ($)", value=150.0, step=10.0,
        help="Average net profit generated per order for this customer"
    )

st.divider()

# ============================================================
# PREDICTION
# ============================================================
if st.button("🔮 Predict Churn", type="primary", use_container_width=True):

    # Build a single-row DataFrame with columns in the EXACT training order
    input_df = pd.DataFrame([{
        "Age": Age,
        "Total_Spent": Total_Spent,
        "Days_Since_Last_Order": Days_Since_Last_Order,
        "Total_Orders": Total_Orders,
        "Avg_Discount": Avg_Discount,
        "Avg_Profit": Avg_Profit,
    }])[feature_names]  # reorder to match feature_names exactly

    # Apply the SAME fitted StandardScaler used in training (transform only, no fit)
    input_scaled = scaler.transform(input_df)

    # Predict using the SAME trained Logistic Regression model
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0, 1]  # P(Churn = 1)

    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ **Likely to CHURN** — Probability: {probability:.1%}")
    else:
        st.success(f"✅ **Likely to stay ACTIVE** — Churn Probability: {probability:.1%}")

    st.progress(min(max(probability, 0.0), 1.0))

    with st.expander("🔍 See input values sent to the model"):
        st.dataframe(input_df)

st.divider()
st.caption("Model: Logistic Regression | Preprocessing: StandardScaler | Source: TechNova_Python_EDA.ipynb")
