import streamlit as st
import pickle
import pandas as pd

# Load Model
model = pickle.load(open("emi_collection_model.pkl", "rb"))

# Title
st.title("Smart EMI Collection Prioritization System")
st.write("Predict Customer EMI Collection Risk Level")

# User Inputs
loan_amount = st.number_input("Loan Amount", min_value=0.0)
outstanding_amount = st.number_input("Outstanding Amount", min_value=0.0)
emi_amount = st.number_input("EMI Amount", min_value=0.0)
payment_delay_days = st.number_input("Payment Delay Days", min_value=0)
customer_score = st.number_input(
    "Customer Score",
    min_value=0,
    max_value=100
)

# Prediction
if st.button("Predict Risk Level"):

    input_data = pd.DataFrame(
        [[
            loan_amount,
            outstanding_amount,
            emi_amount,
            payment_delay_days,
            customer_score
        ]],
        columns=[
            "Loan_Amount",
            "Outstanding_Amount",
            "EMI_Amount",
            "Payment_Delay_Days",
            "Customer_Score"
        ]
    )

    st.write("Input columns:", input_data.columns.tolist())

    if hasattr(model, "feature_names_in_"):
        st.write("Model expects:", model.feature_names_in_.tolist())

    try:
        prediction = model.predict(input_data)

        risk_mapping = {
            0: "Low Risk",
            1: "Medium Risk",
            2: "High Risk"
        }

        st.success(
            f"Predicted Risk Level: {risk_mapping[prediction[0]]}"
        )

    except Exception as e:
        st.error(f"Error: {e}")