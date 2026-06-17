import streamlit as st
import pandas as pd
import pickle


# Load Model

with open("emi_collection_model.pkl", "rb") as file:
    saved_data = pickle.load(file)

model = saved_data["model"]


# Title

st.title("Smart EMI Collection Prioritization System")


# Account Type

account_type = st.selectbox(
    "Account Type",
    ["Current", "Salary", "Savings"]
)

account_map = {
    "Current": 0,
    "Salary": 1,
    "Savings": 2
}


# Loan Type

loan_type = st.selectbox(
    "Loan Type",
    ["Gold Loan", "Home Loan", "Personal Loan"]
)

loan_map = {
    "Gold Loan": 0,
    "Home Loan": 1,
    "Personal Loan": 2
}


# Loan Amount

loan_amount = st.number_input(
    "Loan Amount",
    min_value=0.0
)


# Outstanding Amount

outstanding_amount = st.number_input(
    "Outstanding Amount",
    min_value=0.0
)


# EMI Amount

emi_amount = st.number_input(
    "EMI Amount",
    min_value=0.0
)


# Payment Status

payment_status = st.selectbox(
    "Payment Status",
    ["Paid", "Pending"]
)

payment_map = {
    "Paid": 0,
    "Pending": 1
}


# Payment Delay Days

payment_delay_days = st.number_input(
    "Payment Delay Days",
    min_value=0
)


# Region

region = st.selectbox(
    "Region",
    ["Chennai", "Trichy", "Coimbatore", "Madurai"]
)

region_map = {
    "Chennai": 0,
    "Trichy": 1,
    "Coimbatore": 2,
    "Madurai": 3
}


# CIBIL Customer Score

customer_score = st.number_input(
    "CIBIL Customer Score",
    min_value=0,
    max_value=900,
    value=650
)


# CIBIL Display

if customer_score <= 500:

    st.error("CIBIL Category: High Risk")

elif customer_score <= 650:

    st.warning("CIBIL Category: Medium Risk")

else:

    st.success("CIBIL Category: Low Risk")



# Prediction

if st.button("Predict Risk Level"):

    try:

        input_data = pd.DataFrame(
            [[
                account_map[account_type],
                loan_map[loan_type],
                loan_amount,
                outstanding_amount,
                emi_amount,
                payment_map[payment_status],
                payment_delay_days,
                region_map[region],
                customer_score
            ]],
            columns=[
                "Account_Type",
                "Loan_Type",
                "Loan_Amount",
                "Outstanding_Amount",
                "EMI_Amount",
                "Payment_Status",
                "Payment_Delay_Days",
                "Region",
                "Customer_Score"
            ]
        )


        # Model Prediction

        prediction = model.predict(input_data)


        st.write("Raw Model Prediction:", prediction[0])


        # Final CIBIL Risk Logic

        if customer_score <= 500:

            risk = "High Risk"


        elif customer_score <= 650:

            risk = "Medium Risk"


        else:

            risk = "Low Risk"



        # Output

        if risk == "Low Risk":

            st.success(
                f"Predicted Risk Level : {risk}"
            )


        elif risk == "Medium Risk":

            st.warning(
                f"Predicted Risk Level : {risk}"
            )


        else:

            st.error(
                f"Predicted Risk Level : {risk}"
            )


    except Exception as e:

        st.error(f"Error: {e}")