class SpeedReading:

        # 1 speed measurement for a segment at a given hour.
    def __init__(self, segment_name, speed, timestamp):
        self.segment_name = segment_name
        self.speed = speed
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.segment_name} at {self.timestamp:%a %Y-%m-%d %H:%M}: {self.speed} mph"

class RoadSegment:

        # a road with a normal free flow speed, used to judge congestion.
    def __init__(self, name, free_flow_speed):
        self.name = name
        self.free_flow_speed = free_flow_speed

        # classify a speed as normal / slow / jammed based on % slower than normal.
    def classify_congestion(self, speed):      
        percent_slower = (self.free_flow_speed - speed) / self.free_flow_speed * 100
        if percent_slower < 25:
            return "Normal"
        elif percent_slower < 60:
            return "Slow"
        else:
            return "Jammed"

        # calculate % slower than normal for a given speed.
    def percent_slower(self, speed):
        return (self.free_flow_speed - speed) / self.free_flow_speed * 100