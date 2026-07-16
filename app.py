import streamlit as st
import requests

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Customer Call Center",
    page_icon="📞",
    layout="centered"
)

st.title("📞 Customer Call Center")
st.write("Enter the customer's information and click **Place Call**.")

st.divider()

# -----------------------------------------------------------------------------
# Customer Information
# -----------------------------------------------------------------------------

phone = st.text_input(
    "Phone Number",
    placeholder="5551234567"
)

col1, col2 = st.columns(2)

with col1:
    first_name = st.text_input("First Name")

with col2:
    last_name = st.text_input("Last Name")

st.divider()

# -----------------------------------------------------------------------------
# Account Information
# -----------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    service_balance = st.number_input(
        "Service Balance ($)",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%.2f"
    )

with col2:
    equipment_balance = st.number_input(
        "Equipment Balance ($)",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%.2f"
    )

# Automatically calculate total
total_balance = service_balance + equipment_balance

st.metric(
    "Total Balance",
    f"${total_balance:,.2f}"
)

dpd = st.number_input(
    "Days Past Due",
    min_value=0,
    value=0,
    step=1
)

st.divider()

# -----------------------------------------------------------------------------
# Place Call Button
# -----------------------------------------------------------------------------

if st.button("📞 Place Call", type="primary", use_container_width=True):

    # Basic validation
    if not phone.strip():
        st.error("Please enter a phone number.")
        st.stop()

    if not first_name.strip():
        st.error("Please enter a first name.")
        st.stop()

    if not last_name.strip():
        st.error("Please enter a last name.")
        st.stop()

    params = {
        "countryCode": "+1",
        "phoneNumber": phone.strip(),
        "firstName": first_name.strip(),
        "lastName": last_name.strip(),
        "serviceBalance": f"{service_balance:.2f}",
        "equipmentBalance": f"{equipment_balance:.2f}",
        "totalBalance": f"{total_balance:.2f}",
        "dpd": dpd,
    }

    url = "https://agenticai-chc-dev.exlservice.com/v1/make-call"

    with st.spinner("Initiating call..."):

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            if response.ok:
                st.success(
                    f"✅ Call accepted successfully! (HTTP {response.status_code})"
                )

                with st.expander("Request Details"):
                    st.write("**Request URL**")
                    st.code(response.url)

                    st.write("**Response**")

                    try:
                        st.json(response.json())
                    except Exception:
                        st.write(response.text)

            else:
                st.error(
                    f"❌ Request failed (HTTP {response.status_code})"
                )

                st.code(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error:\n\n{e}")