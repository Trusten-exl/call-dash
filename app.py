import streamlit as st
import requests

st.set_page_config(
    page_title="Customer Call Center",
    page_icon="📞",
    layout="centered"
)

st.title("📞 Customer Call Center")
st.write("Fill in the customer information and click **Place Call**.")

with st.form("call_form"):

    phone = st.text_input(
        "Phone Number",
        placeholder="5551234567"
    )

    first_name = st.text_input("First Name")

    last_name = st.text_input("Last Name")

    service_balance = st.number_input(
        "Service Balance ($)",
        min_value=0.0,
        step=10.0
    )

    equipment_balance = st.number_input(
        "Equipment Balance ($)",
        min_value=0.0,
        step=10.0
    )

    total_balance = service_balance + equipment_balance

    st.metric(
        "Total Balance",
        f"${total_balance:,.2f}"
    )

    dpd = st.number_input(
        "Days Past Due",
        min_value=0,
        step=1
    )

    submitted = st.form_submit_button(
        "📞 Place Call",
        type="primary"
    )

if submitted:

    params = {
        "countryCode": "+1",
        "phoneNumber": phone,
        "firstName": first_name,
        "lastName": last_name,
        "serviceBalance": service_balance,
        "equipmentBalance": equipment_balance,
        "totalBalance": total_balance,
        "dpd": dpd,
    }

    url = "https://agenticai-chc-dev.exlservice.com/v1/make-call"

    try:
        response = requests.get(url, params=params, timeout=30)

        st.subheader("API Response")

        st.code(response.url)

        if response.ok:
            st.success(f"✅ Call (HTTP {response.status_code})")
        else:
            st.error(f"Request failed ({response.status_code})")

    except Exception as e:
        st.error(str(e))