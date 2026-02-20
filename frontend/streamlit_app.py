import streamlit as st
import requests

st.set_page_config(
    page_title="AI Medical Claim Processor",
    page_icon="🏥",
    layout="wide"
)

# ------------------ STYLING ------------------
st.markdown("""
<style>
.result-card {
    background-color: black;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}
.approved {color: green; font-weight: bold;}
.rejected {color: red; font-weight: bold;}
.manual {color: orange; font-weight: bold;}
.low {color: green;}
.medium {color: orange;}
.high {color: red;}
</style>
""", unsafe_allow_html=True)

st.title("🏥 AI-Based Medical Claim Processing System")
st.caption("Smart Claim Validation • Fraud Detection • Explainable AI")

st.markdown("---")

# ------------------ USER SECTION ------------------
st.subheader("👤 User Information")

user_id = st.number_input("User ID", min_value=1, step=1)

st.markdown("---")

# ------------------ CLAIM FORM ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Patient & Claim Details")
    patient_age = st.number_input("Patient Age", 0, 120, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    diagnosis_code = st.text_input("Diagnosis Code", "D123")
    procedure_code = st.text_input("Procedure Code", "P456")

with col2:
    st.subheader("🏥 Policy & Admission Details")
    claim_amount = st.number_input("Claim Amount", 0, 50000)
    policy_coverage_amount = st.number_input("Policy Coverage Amount", 0, 100000)
    hospital_type = st.selectbox("Hospital Type", ["Private", "Government"])
    admission_type = st.selectbox("Admission Type", ["Emergency", "Planned"])
    previous_claim_count = st.number_input("Previous Claim Count", 0, 0)

st.markdown("---")

# ------------------ BUTTON ------------------
if st.button("🚀 Evaluate Claim", use_container_width=True):

    payload = {
        "user_id": user_id,   # 🔥 THIS WAS MISSING
        "patient_age": patient_age,
        "gender": gender,
        "diagnosis_code": diagnosis_code,
        "procedure_code": procedure_code,
        "claim_amount": claim_amount,
        "policy_coverage_amount": policy_coverage_amount,
        "hospital_type": hospital_type,
        "admission_type": admission_type,
        "previous_claim_count": previous_claim_count
    }

    try:
        response = requests.post(
    "http://localhost:9000/predict",
    json=payload
)
        

        if response.status_code == 200:
            result = response.json()

            if "claim_status" not in result:
                st.error(result.get("message", "Unknown Error"))
                st.stop()

            status = result["claim_status"]
            fraud = result["fraud_risk"]
            confidence = float(result["confidence_score"])

            status_class = (
                "approved" if status == "Approved"
                else "rejected" if status == "Rejected"
                else "manual"
            )

            fraud_class = (
                "low" if fraud == "Low"
                else "medium" if fraud == "Medium"
                else "high"
            )

            st.markdown("## 📊 Prediction Result")

            st.markdown(f"""
            <div class="result-card">
                <p>🧾 Claim Status:
                    <span class="{status_class}">{status}</span>
                </p>
                <p>🔍 Fraud Risk:
                    <span class="{fraud_class}">{fraud}</span>
                </p>
                <p>🧠 Explanation: {result["explanation"]}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 🎯 Model Confidence")
            st.progress(confidence)
            st.write(f"Confidence Score: **{confidence*100:.2f}%**")

        else:
            st.error("API Error")
            st.write(response.text)

    except Exception as e:
        st.error("Could not connect to backend API.")
        st.write(str(e))