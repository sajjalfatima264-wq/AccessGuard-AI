def group_and_deduplicate_issues(issues: list) -> list:
    grouped = {}
    for issue in issues:
        key = f"{issue.get('wcag_reference')}-{issue.get('description')}"

        if key not in grouped:
            grouped[key] = issue.copy()
            grouped[key]["occurrences"] = 1
            grouped[key]["elements"] = [
                {"element": issue["element"], "location": issue["location"]}
            ]
        else:
            grouped[key]["occurrences"] += 1
            grouped[key]["elements"].append(
                {"element": issue["element"], "location": issue["location"]}
            )

    return list(grouped.values())