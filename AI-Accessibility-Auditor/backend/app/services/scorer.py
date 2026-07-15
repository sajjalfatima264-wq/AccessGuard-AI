import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def calculate_accurate_scores(parsed_data: dict, grouped_issues: list) -> dict:
    # Filter out hidden inputs
    visible_inputs = []
    for form in parsed_data.get("forms", []):
        for inp in form.get("inputs", []):
            if inp.get("type") != "hidden":
                visible_inputs.append(inp)

    categories = {
        "images": {"total": len(parsed_data.get("images", [])), "failed": 0},
        "forms": {"total": len(visible_inputs), "failed": 0},
        "headings": {"total": len(parsed_data.get("headings", [])), "failed": 0},
        "buttons": {"total": len(parsed_data.get("buttons", [])), "failed": 0},
        "links": {"total": len(parsed_data.get("links", [])), "failed": 0},
    }

    # ROBUST MAPPING: Links singular rule output to plural category
    type_mapping = {
        "image": "images",
        "form": "forms",
        "heading": "headings",
        "button": "buttons",
        "link": "links"
    }

    for issue in grouped_issues:
        issue_type = issue.get("type")
        cat_key = type_mapping.get(issue_type)
        if cat_key and cat_key in categories:
            categories[cat_key]["failed"] += issue.get("occurrences", 1)

    category_scores = {}
    total_passed = 0
    total_failed = 0

    for cat, data in categories.items():
        if data["total"] > 0:
            passed = max(0, data["total"] - data["failed"])
            score = int((passed / data["total"]) * 100)
            category_scores[cat] = {
                "score": score,
                "total": data["total"],
                "failed": data["failed"],
            }
            total_passed += passed
            total_failed += data["failed"]
        else:
            category_scores[cat] = {"score": 100, "total": 0, "failed": 0}

    overall_total = total_passed + total_failed
    overall_score = (
        int((total_passed / overall_total) * 100) if overall_total > 0 else 100
    )

    # Debug logging for verification
    logger.info(f"--- SCORING DEBUG ---")
    logger.info(f"Total checks: {overall_total}")
    logger.info(f"Passed checks: {total_passed}")
    logger.info(f"Failed checks: {total_failed}")
    logger.info(f"Final score: {overall_score}")

    return {"overall": overall_score, "categories": category_scores}