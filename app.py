import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# --- 1. DATA STRUCTURE ---
class AuditIssue(BaseModel):
    field: str
    severity: str
    description: str

class ShippingAuditReport(BaseModel):
    hs_code: str
    country_of_origin: str
    destination_country: str
    goods_description: str
    total_value: float
    is_compliant: bool
    sanctions_risk: str
    audit_findings: List[AuditIssue]

# --- 2. AUTHENTICATION & INITIALIZATION ---
st.set_page_config(page_title="Global Trade Auditor", page_icon="🚢")

# Securely get API Key from Streamlit Secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("API Key not found. Please configure Streamlit Secrets.")

# --- 3. UI LAYOUT ---
st.title("🚢 Global Trade Compliance Auditor")
st.markdown("Automated AI auditing for shipping documents and customs declarations.")

# Sidebar for Access Control & Legal
with st.sidebar:
    st.header("Access Control")
    access_key = st.text_input("Enter your E-book Access Key:", type="password")
    
    st.markdown("---")
    st.caption("""
    **LEGAL DISCLAIMER:** This tool is for educational purposes only. 
    AI-generated audits may contain errors. Always verify with a 
    certified Customs Broker. The developer is not liable for fines.
    """)

# --- 4. CORE LOGIC ---
if access_key == "EXPERT-2026": # Match this to your E-book key
   uploaded_files = st.file_uploader("Upload shipping documents (PDF)", type=["pdf"], accept_multiple_files=True)

    if uploaded_file and st.button("Run Global Audit"):
        with st.spinner("Analyzing document against global trade standards..."):
            try:
                # Extract Text
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                raw_text = "".join([page.get_text() for page in doc])

                # AI Audit Request
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": "You are a Global Customs Auditor. Audit the following text for HS Code accuracy, sanctions, and value consistency."},
                        {"role": "user", "content": raw_text}
                    ],
                    response_format=ShippingAuditReport,
                )
                
                report = completion.choices[0].message.parsed

                # --- 5. DISPLAY RESULTS ---
                st.success("Audit Complete!")
                
                col1, col2 = st.columns(2)
                col1.metric("Compliance Status", "PASS" if report.is_compliant else "FLAGGED")
                col2.metric("Sanctions Risk", report.sanctions_risk)

                st.subheader("Extracted Details")
                st.write(f"**HS Code:** {report.hs_code}")
                st.write(f"**Description:** {report.goods_description}")
                st.write(f"**Value:** {report.total_value}")

                if report.audit_findings:
                    st.subheader("⚠️ Audit Findings")
                    for issue in report.audit_findings:
                        st.warning(f"**{issue.field} ({issue.severity}):** {issue.description}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    if access_key:
        st.error("Invalid Access Key. Please check your E-book.")
    else:
        st.info("Please enter your Access Key in the sidebar to begin.")
