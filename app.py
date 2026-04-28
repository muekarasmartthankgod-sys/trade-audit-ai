import streamlit as st
import openai
import fitz  # PyMuPDF
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- CONFIGURATION & SECRETS ---
st.set_page_config(
    page_title="Global Trade Auditor Pro | Chief Superintendent Edition", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Executive UI
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e1e4e8; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API Key not found in Streamlit Secrets.")

# --- DATA STRUCTURES (Fixed Schema for Structured Outputs) ---
class IndividualAudit(BaseModel):
    hs_code_verified: str
    risk_level: str 
    brand_alert: str 
    findings: List[str]
    hardware_directive: str 
    recommendation: str

class RiskMetrics(BaseModel):
    High: float = Field(description="Percentage of high-risk consignments")
    Medium: float = Field(description="Percentage of medium-risk consignments")
    Low: float = Field(description="Percentage of low-risk consignments")
    Critical: float = Field(description="Percentage of critical-risk consignments")

class ExecutiveSummary(BaseModel):
    total_consignments: int
    revenue_at_risk: str
    risk_distribution: RiskMetrics 
    strategic_patterns: List[str]
    green_channel_list: List[str]
    hardware_utilization_strategy: str

# --- CORE FUNCTIONS ---
def clean_text(text: str) -> str:
    return text.replace('\x00', '').strip()[:12000]

def extract_pdf_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Extraction Error: {str(e)}"

def run_individual_audit(text: str, filename: str):
    system_msg = (
        "You are a Chief Customs Superintendent with 15 years of NII experience. "
        "Analyze this manifest for HS Code fraud, brand counterfeiting (Hermes, Samsung)[cite: 5, 6, 7], "
        "and load-layering. Provide hardware directives for Smiths HCVG or Nuctech MT1213 DE[cite: 9, 10]."
    )
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Manifest ({filename}):\n{text}"}
        ],
        response_format=IndividualAudit,
    )
    return response.choices[0].message.parsed

def generate_executive_report(batch_log: str):
    if not batch_log.strip():
        return None
    system_msg = (
        "You are a Senior Customs Intelligence Director. Synthesize multiple audit logs "
        "into a Strategic Executive Report for DP World or APM Terminals. "
        "Focus on revenue protection, throughput velocity, and Green Channel facilitation."
    )
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Batch Audit Logs:\n{batch_log}"}
        ],
        response_format=ExecutiveSummary,
    )
    return response.choices[0].message.parsed

# --- MAIN UI ---
st.title("🚢 Global Trade Intelligence Portal")
st.caption("AI-Powered Decision Support for National Security & Revenue Protection")

with st.sidebar:
    st.header("🔐 Authentication")
    access_key = st.text_input("Chief Superintendent Access Key:", type="password")
    if access_key == "EXPERT-2026":
        st.success("Access Granted")
        st.divider()
        st.markdown(f"**Expert:** Smart Thankgod Muekara[cite: 14]")
        st.markdown(f"**Rank:** Chief Superintendent[cite: 14]")
        st.markdown(f"**NII Fleet:** Smiths HCVG / Nuctech MT1213[cite: 9, 10]")
    else:
        st.info("Enter 'EXPERT-2026' to begin.")

if access_key == "EXPERT-2026":
    files = st.file_uploader("Upload Manifests (PDF)", type=["pdf"], accept_multiple_files=True)
    if files:
        if st.button("🚀 Execute Strategic Analysis"):
            audit_results = []
            combined_log = ""
            
            # Step 1: Batch Individual Audits
            for f in files:
                with st.spinner(f"Auditing {f.name}..."):
                    raw_text = extract_pdf_text(f)
                    cleaned = clean_text(raw_text)
                    try:
                        res = run_individual_audit(cleaned, f.name)
                        audit_results.append((f.name, res))
                        combined_log += f"File: {f.name} | Risk: {res.risk_level} | Brand: {res.brand_alert} | Findings: {res.findings}\n"
                    except Exception as e:
                        st.error(f"Error on {f.name}: {e}")

            # Step 2: Display Individual Findings
            st.divider()
            st.subheader("📦 Consignment-Level Findings")
            for name, data in audit_results:
                with st.expander(f"Audit: {name} - [{data.risk_level}]"):
                    st.write(f"**HS Verification:** {data.hs_code_verified}")
                    st.write(f"**Brand Alert:** {data.brand_alert}")
                    st.warning(f"**Hardware Directive:** {data.hardware_directive}")
                    st.write("**Findings:**")
                    for finding in data.findings:
                        st.write(f"- {finding}")

            # Step 3: Global Executive Summary
            if combined_log:
                st.divider()
                st.header("📊 Strategic Executive Intelligence Report")
                try:
                    summary = generate_executive_report(combined_log)
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Revenue at Risk", summary.revenue_at_risk)
                    m2.metric("Total Audited", summary.total_consignments)
                    m3.metric("Critical Risk", f"{summary.risk_distribution.Critical}%")
                    
                    left, right = st.columns(2)
                    with left:
                        st.subheader("📈 Threat Patterns")
                        for p in summary.strategic_patterns:
                            st.write(f"🚩 {p}")
                        st.subheader("⚡ Green Channel")
                        for g in summary.green_channel_list:
                            st.success(f"✅ {g}")
                    with right:
                        st.subheader("🛠 NII Deployment Strategy")
                        st.info(summary.hardware_utilization_strategy)
                        st.markdown("**Optimization:** Deploy **Smiths HCVG** for organic analysis[cite: 10] and **Nuctech MT1213** for high-density penetration[cite: 9].")
                except Exception as e:
                    st.error(f"Executive Synthesis Error: {e}")
else:
    st.warning("Locked. Please authenticate via the sidebar.")

st.divider()
st.caption("Legal Disclaimer: Research purposes only. Official clearance must be verified by a human officer[cite: 14].")
