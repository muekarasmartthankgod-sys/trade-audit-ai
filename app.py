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

# Custom CSS for a high-level "Command Center" UI
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e1e4e8; }
    .status-box { padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #1c3d5a; }
    </style>
    """, unsafe_allow_html=True)

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API Key not found in Streamlit Secrets.")

# --- DATA STRUCTURES (Optimized for Structured Outputs) ---
class IndividualAudit(BaseModel):
    hs_code_verified: str = Field(description="Verification status of the Harmonized System codes.")
    risk_level: str = Field(description="Risk classification: Low, Medium, High, or Critical.")
    brand_alert: str = Field(description="Analysis of counterfeit risk for brands like Samsung, Hermes, or P&G.")
    findings: List[str] = Field(description="Specific anomalies found in the manifest.")
    hardware_directive: str = Field(description="Specific scan instructions for Smiths HCVG or Nuctech MT1213 systems.")
    recommendation: str = Field(description="Final clearance recommendation.")

class ExecutiveSummary(BaseModel):
    total_consignments: int
    revenue_at_risk: str
    risk_distribution: Dict[str, float] # Percentage per category
    strategic_patterns: List[str] # Patterns like load-layering or split shipments
    green_channel_list: List[str] # Trusted traders for fast-track processing
    hardware_utilization_strategy: str # Optimization of NII fleet deployment

# --- HELPER FUNCTIONS ---
def clean_manifest_text(text: str) -> str:
    """Removes noise and limits length to prevent API context overflow."""
    cleaned = text.replace('\x00', '').strip()
    return cleaned[:12000] # Safe limit for standard manifests

def extract_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Extraction Error: {str(e)}"

def run_audit(text: str, filename: str):
    """Chief Superintendent Logic for individual manifest audit."""
    system_msg = (
        "You are a Chief Customs Superintendent with 15 years of experience. "
        "You are certified in Smiths Detection HCVG and Nuctech MT1213 DE systems. "
        "Analyze the manifest for brand counterfeiting (Hermes, Samsung)[cite: 5, 6, 7], "
        "HS code fraud, and density anomalies based on your Mechanical Engineering background[cite: 1, 14]."
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

def generate_summary(batch_data: str):
    """Director-level synthesis for terminal-wide intelligence."""
    system_msg = (
        "You are a Senior Customs Intelligence Director. Synthesize multiple audit logs "
        "into an Executive Report for Port Operators (DP World / APM Terminals). "
        "Focus on revenue leakage, throughput velocity, and Green Channel facilitation[cite: 14]."
    )
    
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Batch Audit Logs:\n{batch_data}"}
        ],
        response_format=ExecutiveSummary,
    )
    return response.choices[0].message.parsed

# --- MAIN INTERFACE ---
st.title("🚢 Global Trade Intelligence Portal")
st.caption("AI-Powered Decision Support for National Security & Revenue Protection")

with st.sidebar:
    st.header("🔐 Authentication")
    access_key = st.text_input("Chief Superintendent Access Key:", type="password")
    
    if access_key == "EXPERT-2026":
        st.success("Access Granted")
        st.divider()
        st.markdown(f"""
        **Verified Expert Profile:**
        *   **Rank:** Chief Superintendent[cite: 14]
        *   **Education:** MSc CS (Research) | BSc CS | ND Mech Eng[cite: 1, 14]
        *   **Specialization:** NII Hardware Integration (Smiths/Nuctech)[cite: 9, 10]
        """)
    else:
        st.info("Enter 'EXPERT-2026' to unlock operational features.")

if access_key == "EXPERT-2026":
    files = st.file_uploader("Upload Batch Manifests (PDF)", type=["pdf"], accept_multiple_files=True)

    if files:
        if st.button("🚀 Execute Strategic Analysis"):
            results = []
            aggregate_log = ""
            
            # Step 1: Individual Analysis
            st.subheader("📦 Consignment-Level Analysis")
            for f in files:
                with st.status(f"Auditing {f.name}...", expanded=False) as status:
                    raw_text = extract_text(f)
                    cleaned = clean_manifest_text(raw_text)
                    
                    try:
                        audit_res = run_audit(cleaned, f.name)
                        results.append((f.name, audit_res))
                        aggregate_log += f"File: {f.name} | Risk: {audit_res.risk_level} | Brand: {audit_res.brand_alert} | Findings: {audit_res.findings}\n"
                        status.update(label=f"Analysis Complete: {f.name}", state="complete")
                    except Exception as e:
                        st.error(f"Analysis failed for {f.name}: {e}")

            # Display individual results in expanders
            for name, data in results:
                with st.expander(f"Audit: {name} - Status: {data.risk_level}"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**HS Code Verification:** {data.hs_code_verified}")
                    c2.write(f"**Brand Alert:** {data.brand_alert}")
                    st.write("**Hardware Directive:**")
                    st.warning(data.hardware_directive)
                    st.write("**Detailed Findings:**")
                    for finding in data.findings:
                        st.write(f"- {finding}")

            # Step 2: Executive Summary
            if aggregate_log:
                st.divider()
                st.header("📊 Strategic Executive intelligence Report")
                with st.spinner("Synthesizing macroscopic threat patterns..."):
                    try:
                        summary = generate_summary(aggregate_log)
                        
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Revenue at Risk", summary.revenue_at_risk)
                        m2.metric("Total Audited", summary.total_consignments)
                        m3.metric("Critical Frequency", f"{summary.risk_distribution.get('Critical', 0)}%")
                        
                        col_left, col_right = st.columns(2)
                        with col_left:
                            st.subheader("📈 Identified Threat Patterns")
                            for pattern in summary.strategic_patterns:
                                st.write(f"🚩 {pattern}")
                            
                            st.subheader("⚡ Green Channel Candidates")
                            for trader in summary.green_channel_list:
                                st.success(f"✅ {trader}")

                        with col_right:
                            st.subheader("🛠 Hardware Deployment Strategy")
                            st.info(summary.hardware_utilization_strategy)
                            st.markdown(f"**NII Fleet Optimization:** Deploy **Smiths HCVG** for organic separation[cite: 10] and **Nuctech MT1213** for high-density steel penetration[cite: 9].")

                    except Exception as e:
                        st.error(f"Executive Synthesis Error: {e}")

else:
    st.warning("Locked. Please authenticate via the sidebar to begin.")

st.divider()
st.caption("Legal Disclaimer: Educational research tool only. Final clearance must be performed by a human officer[cite: 14].")
