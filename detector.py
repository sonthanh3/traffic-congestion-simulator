from collections import defaultdict, defaultdict
from statistics import mean, pstdev

def compute_baseline(readings):
    grouped_levels = defaultdict(list)
    for reading in readings:
        segment_id, timestamp, level = reading
        key = (segment_id, timestamp.weekday(), timestamp.hour)
        grouped_levels[key].append(level)
    baseline = {}
    for key, levels in grouped_levels.items():
        baseline[key] = (mean(levels), pstdev(levels))
    return baseline

def detect_anomalies(readings, baseline, threshold=2.0):
    anomalies = []
    for segment_id, timestamp, level in readings:
        key = (segment_id, timestamp.weekday(), timestamp.hour)
        if key in baseline:
            mean_level, std_dev = baseline[key]
            if std_dev > 0 and abs(level - mean_level) > threshold * std_dev:
                direction = "high" if level > mean_level else "low"
                anomalies.append((segment_id, timestamp, level, direction)) 
    return anomalies