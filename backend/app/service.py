from dataclasses import dataclass
from typing import Any


@dataclass
class Advice:
    area: str
    title: str
    message: str
    actions: list[str]
    confidence: float
    source: str
    escalation_required: bool
    severity: str


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(value, maximum))


def weather_advice(weather: dict[str, Any]) -> list[Advice]:
    results = []

    rainfall = float(weather.get("rainfall_mm", 0))
    humidity = float(weather.get("humidity_percent", 0))
    temperature = float(weather.get("temperature_c", 0))
    wind = float(weather.get("wind_kph", 0))

    if rainfall >= 50:
        results.append(
            Advice(
                area="weather",
                title="Heavy rainfall risk",
                message="Reported rainfall may increase flooding, erosion, and fungal-disease risk.",
                actions=[
                    "Inspect drainage channels and low-lying areas.",
                    "Check crops for standing water and root stress.",
                    "Avoid field work when soil is saturated.",
                ],
                confidence=0.86,
                source="user-provided weather observation; deterministic rule",
                escalation_required=False,
                severity="medium",
            )
        )

    if humidity >= 85 and temperature >= 18:
        results.append(
            Advice(
                area="weather",
                title="Fungal disease conditions",
                message="Reported warm, humid conditions can support fungal disease spread; this is a risk indicator, not a diagnosis.",
                actions=[
                    "Inspect leaves and stems for spots, mould, or unusual growth.",
                    "Improve airflow by removing badly damaged plant material.",
                    "Confirm treatment decisions with a local extension officer.",
                ],
                confidence=0.82,
                source="user-provided weather observations; deterministic screening rule",
                escalation_required=True,
                severity="medium",
            )
        )

    if temperature >= 35:
        results.append(
            Advice(
                area="weather",
                title="Heat stress risk",
                message="Reported high temperatures may cause crop and poultry heat stress.",
                actions=[
                    "Check water availability frequently.",
                    "Provide shade and ventilation.",
                    "Inspect plants for wilting during the hottest part of the day.",
                ],
                confidence=0.88,
                source="user-provided weather observation; deterministic rule",
                escalation_required=False,
                severity="high",
            )
        )

    if wind >= 45:
        results.append(
            Advice(
                area="weather",
                title="Strong wind risk",
                message="Reported strong winds may damage plants, structures, or poultry housing.",
                actions=[
                    "Secure greenhouse covers and lightweight equipment.",
                    "Inspect supports for tall crops.",
                    "Keep poultry housing protected from direct drafts.",
                ],
                confidence=0.84,
                source="user-provided weather observation; deterministic rule",
                escalation_required=False,
                severity="medium",
            )
        )

    return results


def crop_advice(crop: dict[str, Any]) -> list[Advice]:
    results = []

    symptoms = {str(item).strip().lower() for item in crop.get("symptoms", []) if item}
    crop_name = crop.get("crop", "crop")
    affected_percent = float(crop.get("affected_percent", 0))

    disease_signs = {
        "leaf spots",
        "yellow leaves",
        "mildew",
        "wilting",
        "lesions",
        "mould",
        "mold",
    }

    matched = symptoms.intersection(disease_signs)

    if matched:
        severity = "high" if affected_percent >= 30 else "medium"
        confidence = clamp(0.55 + len(matched) * 0.08)

        results.append(
            Advice(
                area="crop",
                title=f"Possible {crop_name} health issue",
                message=(
                    f"Observed symptoms: {', '.join(sorted(matched))}. "
                    "This is a screening result based on user-provided observations, not a confirmed diagnosis."
                ),
                actions=[
                    "Photograph affected leaves in good lighting.",
                    "Inspect nearby plants for similar symptoms.",
                    "Separate visibly affected plant material where practical.",
                    "Ask a qualified local agronomist before applying any treatment.",
                ],
                confidence=confidence,
                source="user-provided crop observations; explainable symptom rules",
                escalation_required=True,
                severity=severity,
            )
        )

    if affected_percent >= 50:
        results.append(
            Advice(
                area="crop",
                title="Widespread crop damage",
                message="A large portion of the reported crop area is affected.",
                actions=[
                    "Mark the affected field section.",
                    "Record the date, crop stage, and recent weather.",
                    "Contact an agricultural extension officer promptly.",
                ],
                confidence=0.9,
                source="user-provided farm observation",
                escalation_required=True,
                severity="high",
            )
        )

    return results


def poultry_advice(poultry: dict[str, Any]) -> list[Advice]:
    results = []

    symptoms = {str(item).strip().lower() for item in poultry.get("symptoms", []) if item}
    count = int(poultry.get("affected_count", 0))
    flock_size = int(poultry.get("flock_size", 0))

    urgent_signs = {
        "difficulty breathing",
        "sudden death",
        "severe diarrhoea",
        "weakness",
        "loss of appetite",
        "neurological signs",
    }

    matched = symptoms.intersection(urgent_signs)

    if matched:
        results.append(
            Advice(
                area="poultry",
                title="Poultry health escalation required",
                message=(
                    f"Reported signs: {', '.join(sorted(matched))}. "
                    "The cause cannot be confirmed by this system."
                ),
                actions=[
                    "Separate visibly sick birds where safe.",
                    "Limit unnecessary movement between poultry groups.",
                    "Clean and disinfect shared equipment.",
                    "Contact a veterinarian or livestock extension officer urgently.",
                ],
                confidence=0.9,
                source="user-provided poultry observations; triage rules",
                escalation_required=True,
                severity="high",
            )
        )

    if flock_size > 0 and count / flock_size >= 0.2:
        results.append(
            Advice(
                area="poultry",
                title="Multiple birds affected",
                message="A significant portion of the flock may be affected, based on the reported counts.",
                actions=[
                    "Record affected and deceased bird counts.",
                    "Check feed, water, ventilation, and temperature.",
                    "Seek professional veterinary guidance.",
                ],
                confidence=0.88,
                source="user-provided flock counts; deterministic triage rule",
                escalation_required=True,
                severity="high",
            )
        )

    return results


def activity_advice(activity: dict[str, Any]) -> list[Advice]:
    results = []

    last_irrigation_days = activity.get("days_since_irrigation")
    last_inspection_days = activity.get("days_since_inspection")

    if last_irrigation_days is not None and int(last_irrigation_days) >= 7:
        results.append(
            Advice(
                area="activity",
                title="Irrigation check due",
                message="The farm activity log has not recorded irrigation recently.",
                actions=[
                    "Check soil moisture before irrigating.",
                    "Inspect irrigation lines and storage tanks.",
                    "Record the next irrigation activity.",
                ],
                confidence=0.72,
                source="user-provided farm activity log",
                escalation_required=False,
                severity="low",
            )
        )

    if last_inspection_days is not None and int(last_inspection_days) >= 5:
        results.append(
            Advice(
                area="activity",
                title="Crop inspection overdue",
                message="Regular field inspection has not been recorded recently.",
                actions=[
                    "Inspect representative plants across the field.",
                    "Record symptoms, location, and affected percentage.",
                    "Upload clear images for a more useful screening result.",
                ],
                confidence=0.8,
                source="user-provided farm activity log",
                escalation_required=False,
                severity="low",
            )
        )

    return results


def generate_advice(payload: dict[str, Any]) -> dict[str, Any]:
    advice: list[Advice] = []

    advice.extend(weather_advice(payload.get("weather", {})))
    advice.extend(crop_advice(payload.get("crop", {})))
    advice.extend(poultry_advice(payload.get("poultry", {})))
    advice.extend(activity_advice(payload.get("activity", {})))

    if not advice:
        advice.append(
            Advice(
                area="general",
                title="No immediate risk detected",
                message="There is not enough evidence to generate a specific warning.",
                actions=[
                    "Continue routine crop and poultry inspections.",
                    "Record weather and farm activities.",
                    "Add clear observations when requesting advice.",
                ],
                confidence=0.5,
                source="FarmSense baseline rules",
                escalation_required=False,
                severity="low",
            )
        )

    severity_order = {"high": 0, "medium": 1, "low": 2}
    advice.sort(key=lambda item: severity_order[item.severity])

    return {
        "advice": [
            {
                "area": item.area,
                "title": item.title,
                "message": item.message,
                "actions": item.actions,
                "confidence": round(item.confidence, 2),
                "source": item.source,
                "escalation_required": item.escalation_required,
                "severity": item.severity,
            }
            for item in advice
        ],
        "model": {
            "name": "FarmSense Explainable Advisory Engine",
            "version": "2.0.0",
            "type": "deterministic-rules",
        },
        "safety": {
            "disclaimer": (
                "This system provides screening support only. "
                "Verify crop and animal-health decisions with local experts. "
                "Weather inputs are supplied by the requester; no external weather provider is integrated."
            ),
            "chemical_or_antibiotic_dosage": False,
        },
    }
