import streamlit as st
import requests


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered",
)


# ============================================================
# 2. FASTAPI URL
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# 3. PAGE TITLE
# ============================================================

st.title("🏠 House Price Prediction")

st.write(
    "Enter the house details below and get an estimated house price."
)


# ============================================================
# 4. HOUSE INPUT FORM
# ============================================================

with st.form("house_prediction_form"):

    st.subheader("House Details")

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
    )

    bathrooms = st.number_input(
        "Bathrooms",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
    )

    kitchens = st.number_input(
        "Kitchens",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
    )

    tv_lounges = st.number_input(
        "TV Lounges",
        min_value=0,
        max_value=10,
        value=1,
        step=1,
    )

    area_sqm = st.number_input(
        "Area (square meters)",
        min_value=1.0,
        value=180.0,
        step=1.0,
    )

    location = st.text_input(
        "Location",
        placeholder="e.g. Islamabad",
    )

    submitted = st.form_submit_button(
        "🔮 Predict House Price",
        use_container_width=True,
    )


# ============================================================
# 5. SEND DATA TO FASTAPI
# ============================================================

if submitted:

    if not location.strip():
        st.error("Please enter the house location.")
        st.stop()

    payload = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "kitchens": kitchens,
        "tv_lounges": tv_lounges,
        "area_sqm": area_sqm,
        "location": location.strip(),
    }

    try:

        with st.spinner("Predicting house price..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=10,
            )

        # ====================================================
        # 6. SUCCESS RESPONSE
        # ====================================================

        if response.status_code == 200:

            result = response.json()

            predicted_price = result["prediction"]["price"]
            currency = result["prediction"]["currency"]

            st.success("Prediction completed successfully! 🎉")

            st.metric(
                label="Estimated House Price",
                value=f"{currency} {predicted_price:,.0f}",
            )

            # Optional: Show submitted details

            with st.expander("View House Details"):

                st.write(f"**Bedrooms:** {bedrooms}")
                st.write(f"**Bathrooms:** {bathrooms}")
                st.write(f"**Kitchens:** {kitchens}")
                st.write(f"**TV Lounges:** {tv_lounges}")
                st.write(f"**Area:** {area_sqm:,.0f} sqm")
                st.write(f"**Location:** {location}")

        # ====================================================
        # 7. API ERROR
        # ====================================================

        else:

            try:
                error_detail = response.json().get(
                    "detail",
                    "Unknown API error."
                )
            except Exception:
                error_detail = response.text

            st.error(
                f"Prediction failed.\n\n{error_detail}"
            )

    # ========================================================
    # 8. CONNECTION ERROR
    # ========================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI server.\n\n"
            "Make sure your FastAPI backend is running on:\n"
            "http://127.0.0.1:8000"
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ The FastAPI server took too long to respond."
        )

    except Exception as e:

        st.error(
            f"❌ Something went wrong: {str(e)}"
        )


# ============================================================
# 9. FOOTER
# ============================================================

st.divider()

st.caption(
    "House Price Prediction System • "
    "Powered by Machine Learning + FastAPI + Streamlit"
)
