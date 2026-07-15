def test_report_json_structure():
    # Simulates the final JSON payload sent to frontend
    report = {
        "score": {
            "overall": 85,
            "categories": {
                "images": {"score": 80, "total": 10, "failed": 2},
                "forms": {"score": 100, "total": 2, "failed": 0},
                "headings": {"score": 100, "total": 1, "failed": 0},
                "buttons": {"score": 100, "total": 5, "failed": 0},
                "links": {"score": 50, "total": 4, "failed": 2}
            }
        },
        "issues": [
            {
                "id": "img-1",
                "type": "image",
                "wcag_reference": "1.1.1",
                "level": "A",
                "severity": "Critical",
                "description": "Missing alt",
                "occurrences": 2,
                "elements": [{"element": "&lt;img&gt;", "location": "Image 1"}],
                "ai": {
                    "problem": "Missing alt text",
                    "impact_on_users": "Screen readers cannot read this.",
                    "recommended_fix": "Add alt attribute.",
                    "code_example": "&lt;img src='x' alt='text'&gt;"
                }
            }
        ]
    }
    
    # Verify required frontend keys exist
    assert "score" in report
    assert "issues" in report
    assert report["score"]["overall"] == 85
    assert report["issues"][0]["occurrences"] == 2
    assert "problem" in report["issues"][0]["ai"]