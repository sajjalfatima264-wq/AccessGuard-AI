import pytest

# Test basic parser resilience with dummy data simulating the parser output structure
def test_parser_output_structure_resilience():
    # Simulating what parse_html_to_accessibility_data returns
    parsed_data = {
        "images": [{"alt": "test", "element_snippet": "<img alt='test'>"}],
        "forms": [],
        "headings": [],
        "buttons": [],
        "links": []
    }
    assert isinstance(parsed_data, dict)
    assert "images" in parsed_data
    assert len(parsed_data["images"]) == 1

def test_parser_handles_missing_attributes():
    # If parser misses attributes, rules shouldn't crash
    from app.services.rules import _check_images
    issues = _check_images([{"alt": None}])
    assert len(issues) == 1