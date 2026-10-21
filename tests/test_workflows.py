from workflows.xray import XRAY_STAGES


def test_workflow_has_expected_stages():
    assert len(XRAY_STAGES) >= 5
    assert XRAY_STAGES[0]["title"] == "Clinical question and referral"
    assert XRAY_STAGES[-1]["title"] == "Interpretation and report"


def test_each_stage_has_required_fields():
    required = {"title", "summary", "checks", "roles", "why"}
    for stage in XRAY_STAGES:
        assert required.issubset(stage)
        assert stage["checks"]
