# Traffic Congestion Simulator

Simulates hourly traffic speeds on 9 Boston road segments and flags readings that are unusually congested or unusually clear compared to that road's normal pattern at the same day and hour.

## How it works

**Data generation (`generator.py`)**
Each segment has a free-flow speed. Speeds are generated hourly: during rush hours (7-9 and 15-19) a road runs at 20-50% of free flow, otherwise at 85-100%. The simulator produces two sets of data:

- **History:** 28 days of normal traffic, used to learn what "normal" looks like.
- **Live:** the 7 days that follow. Three incidents per segment are injected here by dropping speed to 10% of free flow for one hour.

**Analysis (`analysis.py`)**
Average speed, jammed hours, and percent jammed per segment, plus the average percent slower than free flow for each hour of the day, plotted with matplotlib.

**Anomaly detection (`detector.py`)**
1. `compute_baseline` groups history readings by segment, weekday, and hour, then stores the mean and standard deviation of each group.
2. `detect_anomalies` checks each live reading against its group. A reading is flagged when it deviates from the mean by more than `threshold` standard deviations (default 2.0), and is labeled `high` (more congested) or `low` (clearer than usual).

The value being compared is the percent slower than free flow. Groups with no history or zero deviation are skipped.

History and live data are kept separate on purpose. If incidents were included in the baseline, they would raise the mean and deviation of their own group and become harder to detect.

## Running

```
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install matplotlib pytest
python main.py
python -m pytest
```

`main.py` uses a fixed random seed, so results are the same on every run.

## Known limitations

- Each baseline group has only 4 readings (28 days across 7 weekdays), so the standard deviations are noisy and the detector raises many false alarms.
- An incident during rush hour is harder to catch, since speed is already low at that time.
- All segments share the same traffic pattern, and weekends have the same rush hours as weekdays.
- All data is simulated.

## Planned

- Store readings in PostgreSQL
- Expose the detector through a FastAPI endpoint
- Route around congested or anomalous segments
