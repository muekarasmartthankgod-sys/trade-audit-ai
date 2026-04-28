import streamlit as st
import openai
import fitz  # PyMuPDF
import time
import io
from pydantic import BaseModel, Field
from typing import List

# --- CONFIGURATION ---
st.set_page_config(
    page_title="MAITA Framework | Secure Intelligence Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Customs Command Center" aesthetic
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-bottom: 4px solid #1c3d5a; }
    .stAlert { border-radius: 10px; border-left: 5px solid #1c3d5a; }
    .report-box { background-color: #ffffff; padding: 15px; border: 1px solid #dee2e6; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("API Key Missing: Please configure Streamlit Secrets.")

# --- SCHEMA DEFINITIONS ---
class RiskMetrics(BaseModel):
    High: float
    Medium: float
    Low: float
    Critical: float

class ExecutiveSummary(BaseModel):
    total_consignments: int
    revenue_at_risk: str
    risk_distribution: RiskMetrics 
    strategic_patterns: List[str]
    green_channel_list: List[str]
    hardware_utilization_strategy: str

class IndividualAudit(BaseModel):
    hs_code_verified: str
    risk_level: str 
    brand_alert: str 
    findings: List[str]
    hardware_directive: str 
    recommendation: str

# --- OPERATIONAL FUNCTIONS ---
def extract_pdf_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def run_audit_intelligence(text: str, filename: str):
    system_msg = (
        "You are a Chief Customs Superintendent (15 yrs NII exp). "
        "Analyze for HS fraud, brand protection (Samsung, Hermes), and revenue risk. "
        "Assign directives for Smiths HCVG or Nuctech MT1213 assets."
    )
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": text[:12000]}],
        response_format=IndividualAudit,
    )
    return response.choices[0].message.parsed

def synthesize_executive_report(batch_log: str):
    system_msg = (
        "You are a Senior Customs Director. Synthesize audit logs into a Strategic Report. "
        "Prioritize revenue protection under the NCS Act 2023 and throughput velocity."
    )
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": batch_log}],
        response_format=ExecutiveSummary,
    )
    return response.choices[0].message.parsed

# --- UI INTERFACE ---
st.title("🚢 MAITA: Global Trade Intelligence")
st.caption("Multimodal Automated Intelligent Trade Auditor | Regulatory Alignment: NCS Act 2023")

with st.sidebar:
    st.header("🔒 Executive Gateway")
    # Secret Key Access (No hints on UI)
    access_key = st.text_input("Enter Access Key:", type="password")
    
    if access_key == "EXPERT-2026":
        st.success("Authenticated: Chief Superintendent Mode")
        st.divider()
        st.markdown(f"**Expert:** Smart T. Muekara")
        st.markdown(f"**Certifications:** Smiths / Nuctech / UKBF")
    else:
        st.info("Authorized Personnel Only.")

if access_key == "EXPERT-2026":
    files = st.file_uploader("Batch Upload Manifests", type=["pdf"], accept_multiple_files=True)
    
    if files:
        if st.button("🚀 Start High-Velocity Audit"):
            start_time = time.time()
            audit_data = []
            log_for_synthesis = ""
            
            # Step 1: Processing
            for f in files:
                with st.spinner(f"Analyzing {f.name}..."):
                    raw_text = extract_pdf_text(f)
                    res = run_audit_intelligence(raw_text, f.name)
                    audit_data.append((f.name, res))
                    log_for_synthesis += f"File: {f.name} | Risk: {res.risk_level} | Findings: {res.findings}\n"
            
            # Step 2: Synthesis
            summary = synthesize_executive_report(log_for_synthesis)
            end_time = time.time()
            latency = round(end_time - start_time, 2)
            
            # Step 3: Display Executive Report
            st.divider()
            st.header("📊 Strategic Executive Intelligence Report")
            
            # Performance Metric
            st.toast(f"End-to-End Latency: {latency}s", icon="⚡")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Revenue at Risk", summary.revenue_at_risk)
            m2.metric("Total Audited", summary.total_consignments)
            m3.metric("Critical Frequency", f"{summary.risk_distribution.Critical}%")
            m4.metric("System Latency", f"{latency}s")

            col_l, col_r = st.columns(2)
            with col_l:
                st.subheader("📈 Identified Threat Patterns")
                for p in summary.strategic_patterns: st.write(f"🚩 {p}")
            with col_r:
                st.subheader("⚡ Green Channel Candidates")
                for g in summary.green_channel_list: st.success(f"✅ {g}")

            st.divider()
            st.subheader("🛠 NII Deployment Strategy")
            st.info(summary.hardware_utilization_strategy)

            # Step 4: Download Report Functionality
            report_content = f"""MAITA STRATEGIC AUDIT REPORT
            Generated by: Chief Superintendent Smart T. Muekara
            Legal Basis: NCS Act 2023
            --------------------------------------------------
            Latency: {latency}s
            Revenue at Risk: {summary.revenue_at_risk}
            Critical Risk: {summary.risk_distribution.Critical}%
            
            Strategic Patterns: {', '.join(summary.strategic_patterns)}
            Green Channel: {', '.join(summary.green_channel_list)}
            --------------------------------------------------
            """
            st.download_button(
                label="📥 Download Strategic Briefing (TXT)",
                data=report_content,
                file_name="MAITA_Intelligence_Report.txt",
                mime="text/plain"
            )

else:
    st.markdown("### 🔒 Access Restricted")
    st.warning("Unauthorized access to National Trade Intelligence is prohibited.")
    st.info("Please enter your Executive Access Key in the sidebar to proceed.")

st.divider()
st.caption("Disclaimer: This AI framework is a research product of the University of York.")
