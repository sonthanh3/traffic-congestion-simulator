from datetime import datetime

import pytest

from detector import compute_baseline, detect_anomalies

# Sep 18, 2026 is a Friday (weekday 4)
FRI_5PM = datetime(2026, 9, 18, 17, 0)


def test_baseline_groups_by_segment_weekday_hour():
    readings = [
        ("A", datetime(2026, 9, 18, 17, 0), 0.8),
        ("A", datetime(2026, 9, 18, 17, 30), 0.9),
        ("A", datetime(2026, 9, 25, 17, 15), 0.7),  # next Friday, same group
        ("A", datetime(2026, 9, 18, 11, 0), 0.2),   # different hour
    ]
    baseline = compute_baseline(readings)

    assert len(baseline) == 2
    mean_level, std_dev = baseline[("A", 4, 17)]
    assert mean_level == pytest.approx(0.8)
    assert std_dev == pytest.approx(0.0816, abs=1e-3)


def test_single_reading_group_has_zero_std():
    baseline = compute_baseline([("A", FRI_5PM, 0.5)])
    assert baseline[("A", 4, 17)] == (0.5, 0.0)


def test_detects_high_anomaly():
    baseline = {("A", 4, 17): (0.8, 0.1)}
    result = detect_anomalies([("A", FRI_5PM, 1.1)], baseline)
    assert result == [("A", FRI_5PM, 1.1, "high")]


def test_detects_low_anomaly():
    baseline = {("A", 4, 17): (0.8, 0.1)}
    result = detect_anomalies([("A", FRI_5PM, 0.5)], baseline)
    assert result == [("A", FRI_5PM, 0.5, "low")]


def test_normal_reading_not_flagged():
    baseline = {("A", 4, 17): (0.8, 0.1)}
    assert detect_anomalies([("A", FRI_5PM, 0.85)], baseline) == []


def test_zero_std_is_skipped():
    baseline = {("A", 4, 17): (0.8, 0.0)}
    assert detect_anomalies([("A", FRI_5PM, 5.0)], baseline) == []


def test_unknown_key_is_skipped():
    baseline = {("B", 4, 17): (0.8, 0.1)}
    assert detect_anomalies([("A", FRI_5PM, 5.0)], baseline) == []