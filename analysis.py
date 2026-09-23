from models import RoadSegment
from generator import generate_readings_for_segment
import matplotlib.pyplot as plt

    #this function serve as getting the average speed, jammed hours and percent jammed for each segment
def analyze_segment(segment, readings):
    all_speeds = []
    for r in readings:
        all_speeds.append(r.speed)
    avg_speed = sum(all_speeds) / len(all_speeds)
    jammed_hour = 0
    for r in readings:
        label = segment.classify_congestion(r.speed)
        if label == "Jammed":
            jammed_hour += 1
    percent_jammed = (jammed_hour / len(readings)) * 100
    return {
        "avg_speed": avg_speed,
        "jammed_hours": jammed_hour,
        "percent_jammed": percent_jammed
    }

    #this function serves as average % slower than normal, per hour, across all segments. It returns a dictionary with hour as key and average % slower as value.
def hourly_summary(segment_readings):
    hourly_avg = {}
    for segment, readings in segment_readings:
        for r in readings:
            hour = r.timestamp.hour
            pct = segment.percent_slower(r.speed)

            if hour not in hourly_avg:
                hourly_avg[hour] = []
            hourly_avg[hour].append(pct)
    result = {}
    for hour, pct_list in hourly_avg.items():
        result[hour] = round(sum(pct_list) / len(pct_list), 2)
    return result

    #Matplotlib function to show line chart of congestion by hour.
def plot_hourly_summary(summary):
    hours = list(summary.keys())
    values = list(summary.values())

    plt.plot(hours, values, marker='o')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average % Slower than Normal')
    plt.title('Traffic Congestion by Hour')
    plt.grid(True)
    plt.show()