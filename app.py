import streamlit as st
import openai
import fitz  # PyMuPDF
from pydantic import BaseModel, Field
from typing import List, Dict

# --- CONFIGURATION & SECRETS ---
st.set_page_config(
    page_title="Global Trade Intelligence Portal | Secure Access", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Government-Grade UI Styling
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e1e4e8; }
    .stAlert { border-radius: 10px; border-left: 5px solid #1c3d5a; }
    h1 { color: #1c3d5a; }
    </style>
    """, unsafe_allow_html=True)

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API Key not found. Please configure Streamlit Secrets.")

# --- DATA STRUCTURES (Strict Schema for Executive Synthesis) ---
class RiskMetrics(BaseModel):
    High: float = Field(description="Percentage of high-risk items")
    Medium: float = Field(description="Percentage of medium-risk items")
    Low: float = Field(description="Percentage of low-risk items")
    Critical: float = Field(description="Percentage of critical-risk items")

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

# --- CORE LOGIC ---
def extract_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Extraction Error: {str(e)}"

def run_individual_audit(text: str, filename: str):
    system_msg = (
        "You are a Chief Customs Superintendent with 15 years of NII experience. "
        "Analyze for HS Code fraud, brand counterfeiting (Samsung, Hermes), "
        "and load-layering. Provide hardware directives for Smiths HCVG or Nuctech MT1213 DE."
    )
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": text[:12000]}],
        response_format=IndividualAudit,
    )
    return response.choices[0].message.parsed

def generate_executive_report(batch_log: str):
    system_msg = (
        "You are a Senior Customs Intelligence Director. Synthesize audit logs "
        "into a Strategic Executive Report for Port Operators like DP World. "
        "Focus on revenue protection and Green Channel facilitation."
    )
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": batch_log}],
        response_format=ExecutiveSummary,
    )
    return response.choices[0].message.parsed

# --- UI INTERFACE ---
st.title("🚢 Global Trade Intelligence Portal")
st.caption("Strategic AI Framework for National Security & Revenue Protection")

with st.sidebar:
    st.header("🔒 Secure Authentication")
    # THE CODE IS NO LONGER WRITTEN ON THE UI
    access_key = st.text_input("Executive Access Key:", type="password", help="Enter the key provided in your briefing document.")
    
    if access_key == "EXPERT-2026":
        st.success("Authorized: Chief Superintendent Mode")
        st.divider()
        st.markdown(f"**Operator:** S. Muekara, MSc (Inview)")
        st.markdown(f"**Certifications:** Smiths Detection / Nuctech / UKBF")
    else:
        st.info("Awaiting authorization...")

if access_key == "EXPERT-2026":
    files = st.file_uploader("Upload Shipping Manifests (Batch PDF)", type=["pdf"], accept_multiple_files=True)
    
    if files:
        if st.button("🚀 Execute Strategic Analysis"):
            audit_results = []
            combined_log = ""
            
            for f in files:
                with st.spinner(f"Analyzing {f.name}..."):
                    raw_text = extract_text(f)
                    try:
                        res = run_individual_audit(raw_text, f.name)
                        audit_results.append((f.name, res))
                        combined_log += f"File: {f.name} | Risk: {res.risk_level} | Findings: {res.findings}\n"
                    except Exception as e:
                        st.error(f"Error on {f.name}: {e}")

            # Display Results
            st.divider()
            st.subheader("📦 Consignment-Level Risk Intelligence")
            for name, data in audit_results:
                with st.expander(f"Audit: {name} - {data.risk_level}"):
                    st.write(f"**Brand Alert:** {data.brand_alert}")
                    st.warning(f"**Hardware Directive:** {data.hardware_directive}")
                    for finding in data.findings:
                        st.write(f"- {finding}")

            if combined_log:
                st.divider()
                st.header("📊 Strategic Executive Intelligence Report")
                try:
                    summary = generate_executive_report(combined_log)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Revenue at Risk", summary.revenue_at_risk)
                    m2.metric("Total Audited", summary.total_consignments)
                    m3.metric("Critical Frequency", f"{summary.risk_distribution.Critical}%")
                    
                    l, r = st.columns(2)
                    with l:
                        st.subheader("📈 Threat Patterns")
                        for p in summary.strategic_patterns: st.write(f"🚩 {p}")
                        st.subheader("⚡ Green Channel Candidates")
                        for g in summary.green_channel_list: st.success(f"✅ {g}")
                    with r:
                        st.subheader("🛠 NII Fleet Strategy")
                        st.info(summary.hardware_utilization_strategy)
                        st.markdown("Deploy **Smiths HCVG** for organic analysis and **Nuctech MT1213** for high-density penetration.")
                except Exception as e:
                    st.error(f"Synthesis Error: {e}")
else:
    # SECURE LOCKED STATE
    st.markdown("### 🔒 Restricted Access")
    st.warning("This portal is reserved for authorized Port Authorities, Terminal Operators, and Customs Leadership.")
    st.info("Please enter your unique Executive Access Key in the sidebar to view restricted intelligence reports.")

st.divider()
st.caption("Legal: Research Tool Only. Authorized by Chief Superintendent Smart Thankgod Muekara.")
