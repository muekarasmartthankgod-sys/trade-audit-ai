import streamlit as st
import openai
import fitz  # PyMuPDF
from pydantic import BaseModel
from typing import List, Dict

# --- CONFIGURATION & SECRETS ---
st.set_page_config(
    page_title="Global Trade Auditor Pro | Intelligence Edition", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style Customization for a Professional "Command Center" Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("API Key not found. Please configure Streamlit Secrets.")

# --- DATA STRUCTURES (Pydantic for Structured Outputs) ---
class IndividualAudit(BaseModel):
    hs_code_verified: str
    risk_level: str  # Low, Medium, High, Critical
    brand_authenticity_alert: str # Specific check for Samsung, Hermes, etc.
    technical_findings: List[str]
    nii_scan_directive: str # Specific instructions for Smiths/Nuctech hardware
    recommendation: str

class ExecutiveSummary(BaseModel):
    total_consignments: int
    risk_heatmap: Dict[str, int] # e.g. {"High": 5, "Medium": 10}
    estimated_revenue_at_risk: str
    strategic_threat_patterns: List[str] # Load layering, split shipments
    green_channel_priority: List[str] # Fast-track for DP World/APM efficiency
    hardware_deployment_plan: str # How to utilize NII fleet effectively

# --- CORE LOGIC FUNCTIONS ---
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def run_individual_audit(text, filename):
    """Audits single manifest files using Chief Superintendent Logic."""
    system_prompt = (
        "You are a Chief Superintendent of Customs with 15 years of NII experience. "
        "Your expertise includes Smiths Detection HCVG and Nuctech MT1213 DE systems. "
        "Analyze this manifest for HS Code fraud, brand counterfeiting (Samsung, P&G, Hermes), "
        "and revenue evasion. Provide a specific directive for X-ray operators based on physics "
        "and mechanical density anomalies."
    )
    
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Manifest Content from {filename}: \n{text}"}
        ],
        response_format=IndividualAudit,
    )
    return response.choices[0].message.parsed

def generate_executive_report(all_results_summary):
    """Synthesizes all audits into a Strategic Terminal Report for DP World/APM."""
    system_prompt = (
        "You are a Senior Customs Intelligence Director. Synthesize individual audit findings "
        "into a Strategic Executive Report for Port Terminal Operators. Identify macroscopic "
        "threat patterns, estimate total revenue leakage, and prioritize 'Green Channel' "
        "trade facilitation to reduce port dwell time."
    )
    
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Combined Audit Data: \n{all_results_summary}"}
        ],
        response_format=ExecutiveSummary,
    )
    return response.choices[0].message.parsed

# --- UI INTERFACE ---
st.title("🚢 Global Trade Compliance Auditor Pro")
st.subheader("Decision Intelligence for National Security & Trade Facilitation")

with st.sidebar:
    st.header("🔐 Secure Access")
    access_key = st.text_input("Chief Superintendent Access Key:", type="password")
    st.divider()
    st.markdown(f"""
    **Operator Credentials:**
    - **Expert:** Smart Thankgod Muekara
    - **Rank:** Chief Superintendent
    - **NII Systems:** Smiths HCVG / Nuctech MT1213
    - **Affiliation:** University of York Research[cite: 14]
    """)

if access_key == "EXPERT-2026":
    uploaded_files = st.file_uploader(
        "Upload Manifest Documents (PDF Batch Mode)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("🚀 Execute Strategic Batch Audit"):
            all_audit_data = ""
            results_list = []

            # 1. Process Individual Files
            for uploaded_file in uploaded_files:
                with st.status(f"Analyzing {uploaded_file.name}...", expanded=False) as status:
                    raw_text = extract_text_from_pdf(uploaded_file)
                    audit = run_individual_audit(raw_text, uploaded_file.name)
                    results_list.append((uploaded_file.name, audit))
                    
                    # Log for summary
                    all_audit_data += f"FILE: {uploaded_file.name} | RISK: {audit.risk_level} | FINDINGS: {audit.technical_findings}\n"
                    status.update(label=f"Analysis Complete: {uploaded_file.name}", state="complete")

            # 2. Display Individual Results in Expanders
            st.divider()
            st.header("📦 Individual Consignment Findings")
            for name, res in results_list:
                with st.expander(f"Audit: {name} - [{res.risk_level}]", expanded=False):
                    c1, c2 = st.columns(2)
                    c1.warning(f"**HS Verification:** {res.hs_code_verified}")
                    c2.info(f"**Brand Alert:** {res.brand_authenticity_alert}")
                    
                    st.write("**Technical Findings:**")
                    for f in res.technical_findings:
                        st.write(f"- {f}")
                    
                    st.error(f"**Hardware Directive:** {res.nii_scan_directive}")

            # 3. Generate and Display Executive Summary
            st.divider()
            st.header("📊 Strategic Executive Intelligence Report")
            with st.spinner("Synthesizing terminal-wide threat patterns..."):
                exec_report = generate_executive_report(all_audit_data)

                # Summary Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Consignments", exec_report.total_consignments)
                m2.metric("Revenue at Risk", exec_report.estimated_revenue_at_risk)
                m3.metric("Critical Risks Detected", exec_report.risk_heatmap.get("Critical", 0))

                # Detailed Strategic Analysis
                col_left, col_right = st.columns(2)
                with col_left:
                    st.subheader("📈 Threat Patterns Identified")
                    for pattern in exec_report.strategic_threat_patterns:
                        st.write(f"🚩 {pattern}")
                    
                    st.subheader("⚡ Green Channel (Fast-Track)")
                    for trader in exec_report.green_channel_priority:
                        st.success(f"✅ {trader}")

                with col_right:
                    st.subheader("🛠 Hardware Deployment Strategy")
                    st.info(exec_report.hardware_deployment_plan)
                    
                    st.markdown("""
                    **NII Optimization Note:**  
                    Deploy **Smiths Detection HCVG** for organic/inorganic separation[cite: 10] 
                    and **Nuctech MT1213 DE** for high-energy penetration of dense steel loads[cite: 9].
                    """)

else:
    st.warning("Please authenticate via the sidebar to access Superintendent-level intelligence.")

st.divider()
st.caption("Legal Disclaimer: This AI Auditor is for research purposes. Official Customs clearance requires manual verification by a certified officer.")
