import streamlit as st
from workflows.xray import XRAY_STAGES

st.set_page_config(page_title="RadFlow | X-ray workflow", page_icon="🩻", layout="wide")

st.title("🩻 RadFlow")
st.subheader("Diagnostic X-ray workflow navigator")
st.caption("Educational prototype • UK IR(ME)R framework • Not for clinical decision-making")

st.info("Follow a conventional diagnostic X-ray request from referral through image review and reporting. Local procedures and professional judgement always apply.")

st.sidebar.header("Workflow")
st.sidebar.write("**Modality:** Plain-film X-ray")
st.sidebar.write("**Scope:** Request → report")
selected = st.sidebar.radio(
    "Explore a stage",
    options=list(range(len(XRAY_STAGES))),
    format_func=lambda i: f"{i + 1}. {XRAY_STAGES[i]['title']}",
    key="stage_index",
)

left, right = st.columns([2, 1], gap="large")
stage = XRAY_STAGES[selected]
with left:
    st.markdown(f"### Stage {selected + 1}: {stage['title']}")
    st.write(stage["summary"])
    st.markdown("**Key checks**")
    for item in stage["checks"]:
        st.markdown(f"- {item}")
    if stage.get("decision"):
        st.warning(f"Decision point: {stage['decision']}")
    if stage.get("if_not"):
        st.markdown(f"**If not satisfied:** {stage['if_not']}")
with right:
    st.markdown("### Responsibility")
    st.write(stage["roles"])
    st.markdown("### Why it matters")
    st.write(stage["why"])
    st.progress((selected + 1) / len(XRAY_STAGES), text=f"Stage {selected + 1} of {len(XRAY_STAGES)}")

previous_col, next_col = st.columns(2)
with previous_col:
    if selected > 0 and st.button("← Previous stage", use_container_width=True):
        st.session_state.stage_index = selected - 1
        st.rerun()
with next_col:
    if selected < len(XRAY_STAGES) - 1 and st.button("Next stage →", use_container_width=True):
        st.session_state.stage_index = selected + 1
        st.rerun()


with st.expander("Scope and limitations"):
    st.markdown("""
    - This is a learning and portfolio project, not a hospital-approved workflow.
    - IR(ME)R is a UK regulatory framework; it should not be presented as Tunisian law.
    - The practitioner is responsible for justification; authorisation demonstrates that justification has taken place.
    - The operator performs only practical aspects for which they are entitled and follows local procedures.
    - Pregnancy-related enquiries and actions depend on the individual, examination, clinical context, and local procedures.
    - An imperfect image does not automatically justify repeating an exposure. The need for additional imaging must be assessed under local procedures.
    """)

st.markdown("---")
st.caption("Reference: UK Government, Guidance to the Ionising Radiation (Medical Exposure) Regulations 2017, updated 2024. See docs/references.md in the repository.")
