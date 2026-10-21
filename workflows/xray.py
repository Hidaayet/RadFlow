"""Educational X-ray workflow content and decision rules. Not a clinical rule engine."""

XRAY_STAGES = [
    {
        "title": "Clinical question and referral",
        "summary": "An entitled referrer requests an X-ray to help answer a clinical question.",
        "checks": [
            "Correct patient identifiers and requested examination are supplied.",
            "Clinical indication and relevant history are included.",
            "Relevant previous imaging or diagnostic information is considered where available.",
        ],
        "roles": "Referrer; employer-defined referral procedures apply.",
        "why": "A clear clinical question supports an appropriate examination and helps avoid unnecessary or duplicate exposure.",
        "decision": "Is the request complete enough to assess?",
        "if_not": "Request clarification or missing information before proceeding.",
    },
    {
        "title": "Request review and justification",
        "summary": "An entitled practitioner considers whether the proposed exposure has a sufficient net benefit for this individual.",
        "checks": [
            "Review the clinical information supplied by the referrer.",
            "Consider expected diagnostic benefit against radiation detriment.",
            "Consider relevant previous imaging and suitable alternatives that use less or no ionising radiation.",
        ],
        "roles": "Practitioner; the referrer supplies relevant medical data.",
        "why": "The exposure must be justified before it occurs; a request alone is not authorisation.",
        "decision": "Is the exposure justified and authorised under the applicable procedure?",
        "if_not": "Do not expose the patient; seek clarification, consider an alternative, or decline the request as appropriate.",
    },
    {
        "title": "Patient identification and preparation",
        "summary": "Before the examination, staff confirm the patient and prepare them in line with the local procedure.",
        "checks": [
            "Use the required patient-identification checks.",
            "Confirm the examination and anatomical region against the authorised request.",
            "Explain the procedure and provide instructions appropriate to the patient.",
            "Make pregnancy-related enquiries when relevant under local policy and the clinical context.",
        ],
        "roles": "Entitled operator and other staff assigned under local procedures.",
        "why": "Correct identification, communication and preparation reduce avoidable errors and support safe practice.",
    },
    {
        "title": "Positioning and exposure optimisation",
        "summary": "The operator performs the practical aspects of the examination using an appropriate protocol and technique.",
        "checks": [
            "Confirm the correct patient, examination and anatomical region.",
            "Position and collimate appropriately for the clinical task.",
            "Select suitable exposure factors for the patient and examination according to local protocols.",
            "Follow equipment, infection-control and radiation-protection procedures.",
        ],
        "roles": "Entitled operator; employer provides protocols, training and equipment quality assurance arrangements.",
        "why": "Optimisation aims for image quality adequate for the clinical purpose while keeping exposure as low as reasonably practicable.",
    },
    {
        "title": "Image acquisition and quality review",
        "summary": "The image is acquired and assessed for diagnostic adequacy before the workflow moves on.",
        "checks": [
            "Check coverage, positioning, relevant anatomy and image quality against the examination criteria.",
            "Record and archive the examination as required by local procedures.",
            "If an image is inadequate, assess the reason and whether another image is justified under the local repeat policy.",
        ],
        "roles": "Entitled operator for practical aspects; escalation follows local procedures.",
        "why": "An inadequate image may not answer the clinical question, but a repeat exposure is not automatic.",
        "decision": "Is the image diagnostically adequate?",
        "if_not": "Review the cause and follow the local process for deciding whether additional imaging is warranted; do not repeat automatically.",
    },
    {
        "title": "Interpretation and report",
        "summary": "Images are made available to the appropriately responsible reporting professional, and findings are communicated through the clinical pathway.",
        "checks": [
            "Ensure images and relevant clinical details are available to the reporting professional.",
            "Report findings according to the service's reporting arrangements.",
            "Communicate urgent or unexpected findings through the defined escalation pathway.",
        ],
        "roles": "Radiologist or other appropriately qualified and authorised reporting professional, according to local arrangements.",
        "why": "The purpose of imaging is to inform clinical care; timely communication supports appropriate follow-up.",
    },
]

def assess_referral(is_complete: bool) -> dict:
    """Return the educational next step for referral completeness."""
    if not is_complete:
        return {
            "status": "needs_clarification",
            "can_proceed": False,
            "message": "Seek clarification or missing information before proceeding.",
        }
    return {
        "status": "ready_for_justification",
        "can_proceed": True,
        "message": "The referral can proceed to the justification stage.",
    }

def assess_justification(decision: str) -> dict:
    """Evaluate a simulated justification checkpoint."""
    if decision == "Yes":
        return {
            "status": "justified",
            "can_proceed": True,
            "message": "The simulated justification checkpoint has been passed.",
        }
    if decision == "No — exposure not justified":
        return {
            "status": "not_justified",
            "can_proceed": False,
            "message": "Do not perform the exposure. Follow the applicable process to consider an appropriate alternative or decline the request.",
        }
    return {
        "status": "not_authorised",
        "can_proceed": False,
        "message": "Do not expose the patient until the required justification and authorisation process is complete.",
    }

def assess_image_quality(is_adequate: bool) -> dict:
    """Return the educational next step after image-quality review."""
    if not is_adequate:
        return {
            "status": "review_required",
            "can_proceed": False,
            "message": "Assess the cause of inadequate image quality and whether additional imaging is justified. Do not repeat automatically.",
        }
    return {
        "status": "adequate",
        "can_proceed": True,
        "message": "Continue to image handling, interpretation and reporting.",
    }
