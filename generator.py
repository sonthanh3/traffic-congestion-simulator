import random
from models import SpeedReading
from datetime import datetime, timedelta

#simulate speed for one hour
def generate_speed(free_flow_speed, hour):
    #rush hours
    if hour in [7, 8 , 9, 15, 16, 17, 18, 19]:
        factor = random.uniform(0.2, 0.5)
    else:
        factor = random.uniform(0.85, 1.0)
    return round(free_flow_speed * factor, 1)

# generate speed SpeedReading per hour for a segment.
def generate_readings_for_segment(segment, start, num_days = 28):
    readings = []
    for i in range(num_days * 24):
        timestamp = start + timedelta(hours=i)
        speed = generate_speed(segment.free_flow_speed, timestamp.hour)
        readings.append(SpeedReading(segment.name, speed, timestamp))
    return readings

def inject_incidents(readings, segment, num_incidents=3):
    incidents_readings = []
    for reading in random.sample(readings, num_incidents):
        #inject incident by reducing speed to 10% of free flow speed for 1 hour
        reading.speed = round(segment.free_flow_speed * 0.1, 1)
        incidents_readings.append((reading.segment_name, reading.timestamp))
    return incidents_readings