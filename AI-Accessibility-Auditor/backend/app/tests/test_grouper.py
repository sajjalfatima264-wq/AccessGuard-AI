from app.services.grouper import group_and_deduplicate_issues


def test_dedup_identical_issues():
    issues = [
        {"wcag_reference": "1.1.1", "description": "Missing alt", "element": "<img>", "location": "Image 1"},
        {"wcag_reference": "1.1.1", "description": "Missing alt", "element": "<img>", "location": "Image 2"},
        {"wcag_reference": "1.1.1", "description": "Missing alt", "element": "<img>", "location": "Image 3"},
    ]
    grouped = group_and_deduplicate_issues(issues)
    assert len(grouped) == 1
    assert grouped[0]["occurrences"] == 3
    assert len(grouped[0]["elements"]) == 3


def test_different_issues_stay_separate():
    issues = [
        {"wcag_reference": "1.1.1", "description": "Missing alt", "element": "<img>", "location": "Image 1"},
        {"wcag_reference": "4.1.2", "description": "No button name", "element": "<button>", "location": "Button 1"},
    ]
    grouped = group_and_deduplicate_issues(issues)
    assert len(grouped) == 2


def test_empty_list():
    assert group_and_deduplicate_issues([]) == []


def test_preserves_original_fields():
    issues = [
        {
            "id": "img-1",
            "type": "image",
            "wcag_reference": "1.1.1",
            "level": "A",
            "severity": "Critical",
            "description": "Missing alt",
            "element": "<img>",
            "location": "Image 1"
        }
    ]
    grouped = group_and_deduplicate_issues(issues)
    assert grouped[0]["id"] == "img-1"
    assert grouped[0]["type"] == "image"
    assert grouped[0]["severity"] == "Critical"
    