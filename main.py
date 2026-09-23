from datetime import datetime
import random
from generator import generate_readings_for_segment
from models import RoadSegment
from analysis import analyze_segment, hourly_summary, plot_hourly_summary

def main():
    start = datetime(2026, 9, 7)  # a Monday
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
    for segment in segments:
        readings = generate_readings_for_segment(segment, start)
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
    plot_hourly_summary(summary)

if __name__ == "__main__":
    main()