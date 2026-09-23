from models import RoadSegment
from generator import generate_readings_for_segment
from analysis import analyze_segment, hourly_summary, plot_hourly_summary

def main():

        #define road segments with their free flow speeds
    segments = [ 
        RoadSegment("Commonwealth Ave", 35),
        RoadSegment("Beacon Steet", 30),
        RoadSegment("Storrow Drive", 45),
        RoadSegment("Massachusetts Ave", 30),
    ]    
    result = []
    for segment in segments:
          readings = generate_readings_for_segment(segment)
          analysis = analyze_segment(segment, readings)
          result.append((segment.name, analysis))

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

        #generate hourly summary across all segments and plot it
    summary = hourly_summary(segments)
    print("\nHourly Summary (avg % slower than normal):")
    hours = list(summary.keys())
    for i in range(0, len(hours), 4):
        row = hours[i:i+4]
        line = "  ".join(f"Hour {h:>2}: {summary[h]:>5.2f}%" for h in row)
        print(line)

    plot_hourly_summary(summary)

if __name__ == "__main__":
        main()