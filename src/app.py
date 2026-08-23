"""NetSage AI: Enterprise Operations Desk & Human-in-the-Loop Gateway

Clean UI with Trust-Driven Guidance Banner, Layer/Confidence Badges, and
Interactive HITL Audit Ledger.
"""

from datetime import datetime
from pathlib import Path
from engine import synthesize_diagnosis
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "cases.csv"
AUDIT_PATH = BASE_DIR / "docs" / "model_audit_log.md"

st.set_page_config(
    page_title="NetSage AI | Network Diagnostic Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Contrast Modern Design CSS
st.markdown(
    """
<style>
    /* Trust & Guide Banner */
    .trust-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px solid #4338ca;
        border-left: 6px solid #6366f1;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    .trust-badge {
        background-color: #10b981;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 6px;
    }
    .step-pill {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        color: #cbd5e1;
    }

    /* Diagnostics Badges */
    .badge-layer {
        background-color: #0284c7;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .badge-confidence {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .badge-blast-low {
        background-color: #059669;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .badge-blast-med {
        background-color: #d97706;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    .badge-blast-high {
        background-color: #dc2626;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        font-size: 13px;
    }
    
    .root-cause-card {
        background-color: #1e1b4b;
        border-left: 5px solid #6366f1;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 15px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Main Title
st.title("🛡️ NetSage AI: Network Incident & Diagnostic Desk")

if not DATA_PATH.exists():
  st.error(
      f"Dataset missing at `{DATA_PATH}`. Ensure `data/cases.csv` is present."
  )
  st.stop()

df = pd.read_csv(DATA_PATH)

# Enterprise Trust & Operational Guide Banner
st.markdown(
    """
<div class="trust-banner">
    <span class="trust-badge">🔒 100% HUMAN-VERIFIED EXECUTION</span>
    <div style="font-size: 17px; font-weight: 700; color: #ffffff; margin-bottom: 4px;">
        AI-Assisted Diagnostic Triage • Zero Autonomous Push
    </div>
    <div style="font-size: 13px; color: #94a3b8; margin-bottom: 12px;">
        NetSage AI correlates telemetry to isolate root causes and draft fixes. No configuration command executes without explicit human authorization.
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
        <div class="step-pill">
            <strong style="color: #60a5fa;">1. Ingest:</strong> Select incident ticket or paste raw Cisco CLI show output.
        </div>
        <div class="step-pill">
            <strong style="color: #34d399;">2. Analyze:</strong> Inspect AI root cause, evidence quotes, and blast radius.
        </div>
        <div class="step-pill">
            <strong style="color: #fbbf24;">3. Authorize:</strong> Review, edit CLI commands, and authorize deployment.
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar: Controls
with st.sidebar:
  st.header("⚙️ Configuration")
  api_key_input = st.text_input(
      "Google Gemini API Key (Optional)",
      type="password",
      help=(
          "Provide API key for real-time generative reasoning. Leave blank for"
          " deterministic benchmark mode."
      ),
  )

  st.divider()
  st.header("📋 Case Selector")
  selected_id = st.selectbox("Select Incident Ticket", df["case_id"].tolist())
  case_data = df[df["case_id"] == selected_id].iloc[0].to_dict()

# Workspace Tabs
tab1, tab2 = st.tabs(
    ["📁 Incident Diagnostic Console", "✍️ Real-Time Telemetry Analyzer"]
)

# --- TAB 1: Benchmark Console ---
with tab1:
  col_left, col_right = st.columns([1, 1], gap="large")

  # Left Column: Ingested Telemetry
  with col_left:
    with st.container(border=True):
      st.markdown("### 📥 Ingested Incident Telemetry")

      st.markdown(f"**Ticket ID:** `{case_data.get('case_id', 'N/A')}`")
      st.markdown(f"**Symptom:** {case_data.get('symptom', 'N/A')}")
      st.markdown(
          f"**Topology Context:** {case_data.get('topology_note', 'N/A')}"
      )

      st.markdown("**Cisco IOS CLI Show Output Capture:**")
      st.code(str(case_data.get("show_outputs", "")), language="text")

  # Right Column: Diagnostic Intelligence & Human Gate
  with col_right:
    with st.container(border=True):
      st.markdown("### 🧠 Diagnostic Intelligence")
      diag = synthesize_diagnosis(case_data, api_key_input)

      # Root Cause Callout Card
      st.markdown(
          f"""
            <div class="root-cause-card">
                <div style="font-size: 11px; color: #a5b4fc; font-weight: bold; text-transform: uppercase;">Identified Root Cause</div>
                <div style="font-size: 15px; color: #ffffff; font-weight: 600; margin-top: 2px;">{diag['root_cause']}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      # Badges Highlight Strip
      blast = diag["blast_radius"].upper()
      blast_class = (
          "badge-blast-high"
          if "HIGH" in blast or "CRITICAL" in blast
          else ("badge-blast-med" if "MED" in blast else "badge-blast-low")
      )
      conf_val = int(
          max(
              diag["confidence_score"]["deterministic_weight"],
              diag["confidence_score"]["semantic_reasoning"],
          )
          * 100
      )

      b_col1, b_col2, b_col3 = st.columns(3)
      with b_col1:
        st.markdown(
            f"**Layer:**<br><span"
            f" class='badge-layer'>{diag['osi_layer']}</span>",
            unsafe_allow_html=True,
        )
      with b_col2:
        st.markdown(
            f"**Confidence:**<br><span"
            f" class='badge-confidence'>{conf_val}%</span>",
            unsafe_allow_html=True,
        )
      with b_col3:
        st.markdown(
            f"**Blast Radius:**<br><span class='{blast_class}'>{blast}</span>",
            unsafe_allow_html=True,
        )

      st.write("")
      st.info(f"**🔍 Evidence Anchor:** `{diag['evidence_anchor']}`")
      st.caption(
          f"**🛠️ Next Diagnostic Probe:** `{diag['next_diagnostic_probe']}`"
      )

      # Proposed Fixes
      forward_text = "\n".join(diag["remediation_plan"]["forward_cli"])
      rollback_text = "\n".join(diag["remediation_plan"]["rollback_cli"])

      st.markdown("**Proposed Remediation Script (Human-Editable):**")
      edited_fix = st.text_area(
          "Remediation Plan",
          forward_text,
          height=105,
          key=f"fix_{selected_id}",
          label_visibility="collapsed",
      )

      with st.expander("🔄 View Automated Rollback Sequence"):
        st.code(rollback_text, language="cisco")

      st.markdown("#### 🔒 Human-in-the-Loop Approval Gate")
      btn1, btn2, btn3 = st.columns(3)

      def log_audit_action(
          ticket: str, layer: str, decision: str, payload: str
      ):
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        clean_payload = payload.replace("\n", "; ")
        record = (
            f"\n| {timestamp} | {ticket} | {layer} | {decision} |"
            f" `{clean_payload}` |"
        )
        with open(AUDIT_PATH, "a") as f:
          f.write(record)

      if btn1.button(
          "✅ Approve & Deploy",
          key=f"app_{selected_id}",
          use_container_width=True,
          type="primary",
      ):
        log_audit_action(selected_id, diag["osi_layer"], "ACCEPTED", edited_fix)
        st.success(
            f"Ticket {selected_id} authorized by engineer. Logged to audit"
            " trail."
        )

      if btn2.button(
          "✏️ Override Fix", key=f"over_{selected_id}", use_container_width=True
      ):
        log_audit_action(
            selected_id, diag["osi_layer"], "EDITED_OVERRIDE", edited_fix
        )
        st.warning(f"Ticket {selected_id} edited and overridden by engineer.")

      if btn3.button(
          "❌ Reject", key=f"rej_{selected_id}", use_container_width=True
      ):
        log_audit_action(
            selected_id, diag["osi_layer"], "REJECTED", "NONE - FALSE ALARM"
        )
        st.error(f"Ticket {selected_id} flagged as False Positive.")

# --- TAB 2: Live Custom Input ---
with tab2:
  with st.container(border=True):
    st.subheader("✍️ Real-Time Telemetry Diagnostic Test")
    st.caption(
        "Paste any raw Cisco IOS CLI show-command output to evaluate dynamic"
        " fault detection and confidence analysis."
    )

    custom_symptom = st.text_input(
        "Reported Symptom",
        "Hosts in VLAN 20 cannot reach the default gateway.",
    )
    custom_output = st.text_area(
        "Paste Raw Cisco CLI Show Output Here:",
        height=170,
        placeholder=(
            "Router# show ip interface brief\nGigabitEthernet0/0.20"
            " 192.168.20.1 YES manual administratively down down"
        ),
    )

    if st.button(
        "🚀 Run Live Diagnostic Analysis",
        use_container_width=True,
        type="primary",
    ):
      custom_record = {
          "case_id": "NET-LIVE-CUSTOM",
          "symptom": custom_symptom,
          "topology_note": "Dynamic Real-Time Input",
          "osi_layer": "Unknown",
          "show_outputs": custom_output,
          "expected_fault": "Custom telemetry failure state",
      }
      res = synthesize_diagnosis(custom_record, api_key_input)

      st.success(
          "Diagnostic Analysis Complete via"
          f" **{res.get('engine_mode', 'Engine')}**"
      )

      c_res1, c_res2 = st.columns(2)
      with c_res1:
        st.markdown(f"**Identified Root Cause:**\n> {res['root_cause']}")
        st.markdown(
            f"**Affected Layer:** `{res['osi_layer']}` &nbsp;|&nbsp; **Blast"
            f" Radius:** `{res['blast_radius']}`"
        )
        st.caption(f"**Evidence:** `{res['evidence_anchor']}`")
      with c_res2:
        st.markdown("**Remediation Sequence:**")
        st.code(
            "\n".join(res["remediation_plan"]["forward_cli"]), language="cisco"
        )

# Clean Audit Ledger Display
st.divider()
st.subheader("📜 Live Human Verification & Audit Log")
if AUDIT_PATH.exists():
  with open(AUDIT_PATH, "r") as f:
    lines = f.readlines()
    clean_table = "".join([l for l in lines if not l.strip().startswith("#")])
    st.markdown(clean_table)