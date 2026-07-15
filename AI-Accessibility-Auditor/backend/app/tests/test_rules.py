import pytest
from app.services.rules import run_accessibility_checks

@pytest.fixture
def broken_page():
    return {
        "headings": [],
        "images": [{"alt": None, "element_snippet": "<img>"}],
        "buttons": [{"text": "", "aria_label": "", "element_snippet": "<button></button>"}],
        "forms": [{"inputs": [{"type": "text", "name": "q", "has_label": False, "element_snippet": "<input>"}]}],
        "links": [{"text": "", "href": "/", "element_snippet": "<a></a>"}]
    }

def test_missing_alt_detected(broken_page):
    issues = run_accessibility_checks(broken_page)
    img_issues = [i for i in issues if i["type"] == "image"]
    assert len(img_issues) == 1
    assert img_issues[0]["wcag_reference"] == "1.1.1"

def test_missing_label_detected(broken_page):
    issues = run_accessibility_checks(broken_page)
    form_issues = [i for i in issues if i["type"] == "form"]
    assert len(form_issues) == 1
    assert form_issues[0]["wcag_reference"] == "1.3.1"

def test_empty_link_detected(broken_page):
    issues = run_accessibility_checks(broken_page)
    link_issues = [i for i in issues if i["type"] == "link"]
    assert len(link_issues) == 1
    assert link_issues[0]["wcag_reference"] == "2.4.4"

def test_empty_input_safe():
    assert run_accessibility_checks(None) == []
    assert run_accessibility_checks({}) == []