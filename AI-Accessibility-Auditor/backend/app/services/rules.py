import re


def _safe(val):
    return val.strip() if isinstance(val, str) else ""


def run_accessibility_checks(parsed_data: dict) -> list:
    if not parsed_data or not isinstance(parsed_data, dict):
        return []

    issues = []
    issues.extend(_check_headings(parsed_data.get("headings", [])))
    issues.extend(_check_images(parsed_data.get("images", [])))
    issues.extend(_check_buttons(parsed_data.get("buttons", [])))
    issues.extend(_check_forms(parsed_data.get("forms", [])))
    issues.extend(_check_links(parsed_data.get("links", [])))
    return issues


def _check_headings(headings: list) -> list:
    issues = []
    if not headings:
        return issues

    h1_count = sum(1 for h in headings if h.get("tag") == "h1")
    if h1_count == 0:
        issues.append({
            "id": "heading-missing-h1",
            "type": "heading",
            "wcag_reference": "1.3.1",
            "level": "A",
            "severity": "High",
            "element": "<h1>",
            "location": "Page level",
            "description": "Page is missing an <h1> heading."
        })
    elif h1_count > 1:
        issues.append({
            "id": "heading-multiple-h1",
            "type": "heading",
            "wcag_reference": "1.3.1",
            "level": "A",
            "severity": "High",
            "element": "<h1>",
            "location": "Page level",
            "description": f"Page has {h1_count} <h1> tags. There should only be one."
        })

    for idx, h in enumerate(headings):
        if not h.get("order_correct", True):
            tag = h.get("tag", "h?")
            text = _safe(h.get("text"))
            issues.append({
                "id": f"heading-hierarchy-skip-{idx}",
                "type": "heading",
                "wcag_reference": "1.3.1",
                "level": "A",
                "severity": "Medium",
                "element": f"<{tag}>",
                "location": f"<{tag}>: '{text[:30]}'",
                "description": f"Heading level skipped at <{tag}>."
            })
    return issues


def _check_images(images: list) -> list:
    issues = []
    if not images:
        return issues
    for idx, img in enumerate(images):
        alt = img.get("alt")
        alt_str = _safe(alt)
        snippet = _safe(img.get("element_snippet")) or "<img>"
        if not alt or alt_str == "" or alt_str.upper() == "MISSING":
            issues.append({
                "id": f"img-missing-alt-{idx}",
                "type": "image",
                "wcag_reference": "1.1.1",
                "level": "A",
                "severity": "Critical",
                "element": snippet[:50],
                "location": f"Image {idx + 1}",
                "description": "Image is missing alternative text (alt attribute)."
            })
    return issues


def _check_buttons(buttons: list) -> list:
    issues = []
    if not buttons:
        return issues
    for idx, btn in enumerate(buttons):
        text = _safe(btn.get("text"))
        aria_label = _safe(btn.get("aria_label"))
        snippet = _safe(btn.get("element_snippet")) or "<button>"
        if not text and (not aria_label or aria_label.upper() == "MISSING"):
            issues.append({
                "id": f"btn-empty-{idx}",
                "type": "button",
                "wcag_reference": "4.1.2",
                "level": "A",
                "severity": "Critical",
                "element": snippet[:50],
                "location": f"Button {idx + 1}",
                "description": "Button has no accessible name."
            })
    return issues


def _check_forms(forms: list) -> list:
    issues = []
    if not forms:
        return issues
    input_count = 0
    for form in forms:
        for inp in form.get("inputs", []):
            input_count += 1
            inp_type = _safe(inp.get("type")).lower()
            has_label = inp.get("has_label", False)
            inp_name = _safe(inp.get("name")) or "unknown"
            snippet = _safe(inp.get("element_snippet")) or "<input>"
            if inp_type == "hidden":
                continue
            if not has_label:
                issues.append({
                    "id": f"form-missing-label-{input_count}",
                    "type": "form",
                    "wcag_reference": "1.3.1",
                    "level": "A",
                    "severity": "High",
                    "element": snippet[:50],
                    "location": f"Input: name='{inp_name}'",
                    "description": f"Form input ('{inp_name}') has no associated <label>."
                })
    return issues


def _check_links(links: list) -> list:
    issues = []
    if not links:
        return issues
    vague_phrases = [r"^click here$", r"^read more$", r"^learn more$", r"^more$", r"^here$", r"^link$"]
    for idx, link in enumerate(links):
        text = _safe(link.get("text"))
        href = _safe(link.get("href"))
        snippet = _safe(link.get("element_snippet")) or "<a>"
        if not text:
            issues.append({
                "id": f"link-empty-{idx}",
                "type": "link",
                "wcag_reference": "2.4.4",
                "level": "A",
                "severity": "Critical",
                "element": snippet[:50],
                "location": f"Link {idx + 1}",
                "description": "Link contains no text."
            })
            continue
        if any(re.match(phrase, text.lower()) for phrase in vague_phrases):
            issues.append({
                "id": f"link-vague-{idx}",
                "type": "link",
                "wcag_reference": "2.4.4",
                "level": "A",
                "severity": "Medium",
                "element": snippet[:50],
                "location": f"Link {idx + 1}: '{text}'",
                "description": f"Link text ('{text}') is vague and does not describe the destination."
            })
    return issues