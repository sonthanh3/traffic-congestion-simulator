from datetime import datetime, timedelta
import random
from detector import compute_baseline, detect_anomalies
from generator import generate_readings_for_segment, inject_incidents
from models import RoadSegment
from analysis import analyze_segment, hourly_summary, plot_hourly_summary

def main():
    start = datetime(2026, 9, 7)  # a Monday
    live_start = start + timedelta(days=28)  # start live data after 28 days of historical data
    random.seed(42)  # for reproducibility
    #define road segments with their free flow speeds
    segments = [ 
        RoadSegment("Commonwealth Ave", 35),
        RoadSegment("Beacon Street", 30),
        RoadSegment("Storrow Drive", 45),
        RoadSegment("Massachusetts Ave", 30),
        RoadSegment("Tremont Street", 25),
        RoadSegment("Huntington Ave", 30),
        RoadSegment("Arlington Street", 25),
        RoadSegment("I-90", 55),
        RoadSegment("I-93", 55),
    ]    
    result = []
    segment_readings = []
    history_tuples = []
    live_tuples = []
    injected_incidents = []
    for segment in segments:
        readings = generate_readings_for_segment(segment, start)
        live = generate_readings_for_segment(segment, live_start, num_days=7)
        injected_incidents.extend(inject_incidents(live, segment))
        for r in readings:
            history_tuples.append((r.segment_name, r.timestamp, segment.percent_slower(r.speed)))
        for r in live:
            live_tuples.append((r.segment_name, r.timestamp, segment.percent_slower(r.speed)))
        analysis = analyze_segment(segment, readings)
        result.append((segment.name, analysis))
        segment_readings.append((segment, readings))
    summary = hourly_summary(segment_readings)

    print("Traffic Analysis Results:")
    for segment_name, analysis in result:
        print(f"Segment: {segment_name}")
        print(f"  Average Speed: {analysis['avg_speed']:.2f} mph")
        print(f"  Jammed Hours: {analysis['jammed_hours']}")
        print(f"  Percent Jammed: {analysis['percent_jammed']:.2f}%")
        print()

    #find the segment with the highest percent jammed
    worst = max(result, key=lambda x: x[1]['percent_jammed'])
    print(f"Worst Segment: {worst[0]} with {worst[1]['percent_jammed']:.2f}% jammed hours")

    # print hourly summary and plot it
    print("\nHourly Summary (avg % slower than normal):")
    hours = list(summary.keys())
    for i in range(0, len(hours), 4):
        row = hours[i:i+4]
        line = "  ".join(f"Hour {h:>2}: {summary[h]:>5.2f}%" for h in row)
        print(line)

    # detect anomalies in live data using historical baseline
    baseline = compute_baseline(history_tuples)
    anomalies = detect_anomalies(live_tuples, baseline)

    detected = {(seg, ts) for seg, ts, level, direction in anomalies}
    injected = set(injected_incidents)
    caught = injected & detected
    false_alarms = detected - injected

    print(f"\nIncidents injected: {len(injected)}")
    print(f"Incidents caught: {len(caught)}")
    print(f"False alarms: {len(false_alarms)}")
    plot_hourly_summary(summary)

if __name__ == "__main__":
    main()