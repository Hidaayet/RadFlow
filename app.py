import streamlit as st
from workflows.xray import XRAY_STAGES, assess_referral, assess_justification, assess_image_quality

st.set_page_config(page_title="RadFlow | X-ray", page_icon="🩻", layout="wide")
st.title("🩻 RadFlow")
st.subheader("Diagnostic X-ray workflow navigator")
st.write("An educational prototype for exploring a conventional diagnostic X-ray workflow using the UK IR(ME)R framework as a reference.")
st.warning("Educational only — not a clinical decision-support tool. Follow applicable law, local procedures, and instructions of appropriately authorised staff.")

with st.expander("About this prototype"):
    st.markdown("- Demonstrates a workflow and example decision paths.\n- Does not verify real-world credentials, authorise exposures, or replace local policy.\n- IR(ME)R is a UK regulatory framework; do not assume it is Tunisian law.")

tab_workflow, tab_simulator, tab_roles = st.tabs(["Workflow overview", "Decision-path simulator", "Roles and principles"])

with tab_workflow:
    st.header("X-ray workflow")
    for i, stage in enumerate(XRAY_STAGES, start=1):
        with st.expander(f"{i}. {stage['title']}", expanded=(i == 1)):
            st.write(stage["summary"])
            st.markdown("**Checks**")
            for check in stage["checks"]:
                st.markdown(f"- {check}")
            st.markdown(f"**Roles:** {stage['roles']}")
            st.markdown(f"**Why it matters:** {stage['why']}")
            if stage.get("decision"):
                st.markdown(f"**Decision point:** {stage['decision']}")
                st.markdown(f"**If the checkpoint is not met:** {stage['if_not']}")

with tab_simulator:
    st.header("Educational decision-path simulator")
    st.caption("Use fictional scenarios only. This does not assess a real patient.")
    referral_complete = st.radio("1. Is the referral complete enough to assess?", ["Yes", "No — clarification is needed"], key="referral")
    referral_result = assess_referral(referral_complete == "Yes")
    if not referral_result["can_proceed"]:
        st.warning(referral_result["message"])
        st.stop()
    st.success(referral_result["message"])

    justification = st.radio(
        "2. For this simulation, has an appropriately entitled practitioner completed the justification and authorisation process?",
        ["Yes", "No — process not completed", "No — exposure not justified"],
        key="justification",
    )
    justification_result = assess_justification(justification)
    if not justification_result["can_proceed"]:
        if justification_result["status"] == "not_justified":
            st.error(justification_result["message"])
        else:
            st.warning(justification_result["message"])
        st.stop()
    st.success(justification_result["message"])
    st.info("Continue only within the relevant local procedure and the operator's scope of practice. Confirm identity, examination, preparation and protocol.")

    image_quality = st.radio("3. After acquisition, are the images diagnostically adequate?", ["Yes", "No — review is needed"], key="image_quality")
    image_result = assess_image_quality(image_quality == "Yes")
    if image_result["can_proceed"]:
        st.success(image_result["message"])
    else:
        st.warning(image_result["message"])

with tab_roles:
    st.header("Roles and safety principles")
    st.markdown("""
- **Employer:** establishes procedures, protocols, training and entitlement arrangements.
- **Referrer:** supplies relevant clinical information and requests the examination.
- **Practitioner:** justifies the individual exposure and authorises it under applicable arrangements.
- **Operator:** carries out practical aspects of the exposure within their entitlement.
- **Reporting professional:** interprets images and communicates findings under the service's arrangements.
""")
    st.markdown("### Core principles")
    st.markdown("- Justification must be completed before the exposure.\n- Optimisation aims for image quality adequate for the clinical purpose while limiting exposure appropriately.\n- An inadequate image does not automatically mean another exposure is warranted.\n- Urgent or unexpected findings should follow the defined communication and escalation pathway.")

st.divider()
st.caption("RadFlow portfolio prototype · Verify all content against current authoritative guidance and applicable local requirements before reuse.")
