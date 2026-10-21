from workflows.xray import XRAY_STAGES, assess_referral, assess_justification, assess_image_quality

def test_workflow_has_six_stages():
    assert len(XRAY_STAGES) == 6
    assert XRAY_STAGES[0]["title"] == "Clinical question and referral"

def test_each_stage_has_core_content():
    for stage in XRAY_STAGES:
        assert stage["title"] and stage["summary"] and stage["checks"] and stage["roles"] and stage["why"]

def test_incomplete_referral_requires_clarification():
    result = assess_referral(False)
    assert result["can_proceed"] is False
    assert result["status"] == "needs_clarification"

def test_complete_referral_can_move_to_justification():
    result = assess_referral(True)
    assert result["can_proceed"] is True
    assert result["status"] == "ready_for_justification"

def test_justified_exposure_passes_simulated_checkpoint():
    result = assess_justification("Yes")
    assert result["can_proceed"] is True
    assert result["status"] == "justified"

def test_incomplete_authorisation_blocks_progression():
    result = assess_justification("No — process not completed")
    assert result["can_proceed"] is False
    assert result["status"] == "not_authorised"

def test_unjustified_exposure_is_blocked():
    result = assess_justification("No — exposure not justified")
    assert result["can_proceed"] is False
    assert result["status"] == "not_justified"

def test_adequate_image_can_continue():
    result = assess_image_quality(True)
    assert result["can_proceed"] is True
    assert result["status"] == "adequate"

def test_inadequate_image_requires_review_not_automatic_repeat():
    result = assess_image_quality(False)
    assert result["can_proceed"] is False
    assert result["status"] == "review_required"
    assert "Do not repeat automatically" in result["message"]
