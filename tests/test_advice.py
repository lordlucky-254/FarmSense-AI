from backend.app.service import generate_advice


def test_weather_and_crop_advice_are_sorted_by_severity() -> None:
    body = generate_advice(
        {
            "weather": {"temperature_c": 30, "humidity_percent": 90, "rainfall_mm": 60},
            "crop": {
                "crop": "maize",
                "symptoms": ["leaf spots", "yellow leaves"],
                "affected_percent": 25,
            },
        }
    )

    advice = body["advice"]
    assert advice[0]["severity"] == "medium"
    assert advice[0]["area"] in {"weather", "crop"}
    assert any(item["title"] == "Heavy rainfall risk" for item in advice)
    assert any(item["area"] == "crop" and item["escalation_required"] for item in advice)


def test_urgent_poultry_signs_require_professional_escalation() -> None:
    body = generate_advice(
        {"poultry": {"flock_size": 50, "affected_count": 2, "symptoms": ["sudden death"]}}
    )

    poultry_advice = [item for item in body["advice"] if item["area"] == "poultry"]
    assert poultry_advice
    assert poultry_advice[0]["severity"] == "high"
    assert poultry_advice[0]["escalation_required"] is True
    assert "veterinarian" in " ".join(poultry_advice[0]["actions"])


def test_no_observations_returns_baseline_with_safety_boundary() -> None:
    body = generate_advice({})

    assert body["advice"][0]["area"] == "general"
    assert body["safety"]["chemical_or_antibiotic_dosage"] is False
    assert "no external weather provider is integrated" in body["safety"]["disclaimer"]
