TEMPLATES = {
    "image": {
        "problem": "This image does not have an alt attribute, meaning screen readers cannot describe it to visually impaired users.",
        "impact_on_users": "As a screen reader user, I have no idea what this image shows. It could be a product photo, a chart, or decorative — I simply can't tell.",
        "recommended_fix": "Add a descriptive alt attribute to the image. If the image is decorative, use alt=\"\".",
        "code_example": '<img src="photo.jpg" alt="Team photo at the 2024 conference">'
    },
    "button": {
        "problem": "This button has no visible text, no aria-label, and no accessible name. Assistive technology cannot identify its purpose.",
        "impact_on_users": "I can see a button on screen but my screen reader just says 'button' with no context. I don't know what it does, so I can't use it.",
        "recommended_fix": "Add visible text inside the button, or provide an aria-label attribute describing the action.",
        "code_example": '<button aria-label="Submit search form">\n  <svg>...</svg>\n</button>'
    },
    "form": {
        "problem": "This form input has no associated label element. Screen readers cannot determine what information to enter.",
        "impact_on_users": "My screen reader announces 'edit text' but doesn't tell me what to type here. Is this a name field? An email? I have to guess.",
        "recommended_fix": "Add a <label> element with a for attribute matching the input's id, or use aria-labelledby.",
        "code_example": '<label for="email">Email address</label>\n<input type="email" id="email" name="email">'
    },
    "heading": {
        "problem": "The heading structure on this page does not follow a logical hierarchy, making it harder for assistive technology to navigate.",
        "impact_on_users": "I use headings to jump between sections of a page. When levels are skipped or missing, I lose my place and can't navigate efficiently.",
        "recommended_fix": "Ensure headings follow a strict hierarchy: one H1, then H2s for major sections, H3s for subsections, etc.",
        "code_example": '<h1>Page Title</h1>\n  <h2>Section One</h2>\n    <h3>Subsection</h3>\n  <h2>Section Two</h2>'
    },
    "link": {
        "problem": "This link has no descriptive text or uses vague phrasing that doesn't indicate the destination.",
        "impact_on_users": "My screen reader reads out a list of links to help me navigate. When every link says 'click here' or 'read more', I can't tell them apart.",
        "recommended_fix": "Replace vague text with descriptive text that makes sense out of context, or add an aria-label.",
        "code_example": '<a href="/report.pdf">Download the Q4 financial report (PDF)</a>'
    }
}

DEFAULT_TEMPLATE = {
    "problem": "This element does not meet WCAG accessibility requirements.",
    "impact_on_users": "This issue makes it harder for assistive technology users to understand or interact with this part of the page.",
    "recommended_fix": "Review the WCAG reference provided and apply the recommended technique for this success criterion.",
    "code_example": "N/A"
}


async def generate_ai_explanations(issues: list) -> list:
    enriched = []
    for issue in issues:
        issue_type = issue.get("type", "")
        template = TEMPLATES.get(issue_type, DEFAULT_TEMPLATE).copy()

        issue["ai"] = {
            "problem": template["problem"],
            "impact_on_users": template["impact_on_users"],
            "recommended_fix": template["recommended_fix"],
            "code_example": template["code_example"],
        }
        enriched.append(issue)
    return enriched