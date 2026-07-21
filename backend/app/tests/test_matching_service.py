import numpy as np

from app.models.image_data import ImageData
from app.services import matching_service


def test_matching_service_uses_image_data_student_records_when_not_provided(monkeypatch):
    image_data = ImageData(image=np.zeros((10, 10, 3), dtype=np.uint8))
    image_data.student_records = [
        {"student_id": "20210001", "name": "Alice"},
    ]

    captured = {}

    def fake_match(image_data_arg, student_records, fuzzy_threshold):
        captured["records"] = student_records
        return []

    monkeypatch.setattr(matching_service.StudentMatcher, "match", fake_match)
    monkeypatch.setattr(matching_service.MatchValidator, "validate", lambda matches: ([], []))
    monkeypatch.setattr(matching_service.MatchingStatistics, "calculate", lambda image_data_arg: {})

    results = matching_service.MatchingService.process(image_data)

    assert results == []
    assert captured["records"] == image_data.student_records
