def build_advice(snapshot: dict) -> dict:
    actions: list[dict] = []
    if snapshot["rain_probability"] >= 0.7:
        actions.append({"priority": "high", "area": "weather", "action": "Inspect drainage and avoid unnecessary leaf wetting before the rain window.", "source": "weather-rule-v0"})
    if snapshot["crop_symptoms"]:
        actions.append({"priority": "medium", "area": "crops", "action": "Photograph affected leaves in daylight, isolate the pattern, and request crop-health confirmation.", "source": "crop-triage-v0"})
    if snapshot["poultry_symptoms"]:
        actions.append({"priority": "high", "area": "poultry", "action": "Separate affected birds and contact an animal-health professional if symptoms are severe or spreading.", "source": "poultry-triage-v0"})
    if not actions:
        actions.append({"priority": "low", "area": "routine", "action": "Continue scouting, record changes, and keep water, feed, and housing clean.", "source": "farm-routine-v0"})
    return {
        "location": snapshot["location"],
        "summary": f"{len(actions)} actionable observation(s) for this farm snapshot.",
        "actions": actions,
        "confidence": 0.55,
        "requires_local_verification": True,
        "model": "farmsense-rules-v0",
    }
