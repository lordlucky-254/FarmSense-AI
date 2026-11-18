from backend.app.service import build_advice


def test_weather_action() -> None:
    body = build_advice({"location": "Kenya", "crop": "tomato", "crop_symptoms": [], "poultry_symptoms": [], "rain_probability": 0.8, "temperature_c": 25})
    assert body["actions"][0]["area"] == "weather"


def test_advice_requires_verification() -> None:
    body = build_advice({"location": "Kenya", "crop": "tomato", "crop_symptoms": [], "poultry_symptoms": [], "rain_probability": 0, "temperature_c": 25})
    assert body["requires_local_verification"] is True
