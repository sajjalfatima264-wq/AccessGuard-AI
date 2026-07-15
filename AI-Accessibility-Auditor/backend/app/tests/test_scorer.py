import pytest
from app.services.scorer import calculate_accurate_scores

@pytest.fixture
def parsed_data():
    return {
        "images": [{"alt": "ok"}, {"alt": None}, {"alt": None}],
        "forms": [{"inputs": [{"type": "text", "name": "a", "has_label": True}, {"type": "text", "name": "b", "has_label": False}, {"type": "hidden", "name": "csrf", "has_label": False}]}],
        "headings": [{"tag": "h1", "text": "Title"}, {"tag": "h3", "text": "Skip", "order_correct": False}],
        "buttons": [{"text": "Click"}, {"text": "", "aria_label": ""}],
        "links": [{"text": "Good link"}, {"text": "click here"}]
    }

@pytest.fixture
def grouped_issues():
    return [
        {"type": "image", "occurrences": 2},
        {"type": "form", "occurrences": 1},
        {"type": "heading", "occurrences": 1},
        {"type": "button", "occurrences": 1},
        {"type": "link", "occurrences": 1}
    ]

def test_overall_score(parsed_data, grouped_issues):
    result = calculate_accurate_scores(parsed_data, grouped_issues)
    # 5 passed / 11 total = 45%
    assert result["overall"] == 45

def test_image_category_score(parsed_data, grouped_issues):
    result = calculate_accurate_scores(parsed_data, grouped_issues)
    # 1 passed / 3 total images = 33%
    assert result["categories"]["images"]["score"] == 33
    assert result["categories"]["images"]["failed"] == 2

def test_failures_reduce_score(parsed_data, grouped_issues):
    result = calculate_accurate_scores(parsed_data, grouped_issues)
    # If there are failures, it MUST NOT be 100
    assert result["overall"] < 100

def test_empty_page_scores_100():
    empty = {"images": [], "forms": [], "headings": [], "buttons": [], "links": []}
    result = calculate_accurate_scores(empty, [])
    assert result["overall"] == 100

def test_hidden_inputs_not_counted():
    data = {"images": [], "forms": [{"inputs": [{"type": "hidden", "name": "csrf", "has_label": False}]}], "headings": [], "buttons": [], "links": []}
    result = calculate_accurate_scores(data, [])
    assert result["categories"]["forms"]["total"] == 0