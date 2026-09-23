import random
from models import SpeedReading

    #simulate speed for one hour
def generate_speed(free_flow_speed, hour):

        #rush hours
    if hour in [7, 8 , 9, 15, 16, 17, 18, 19]:
        factor = random.uniform(0.2, 0.5)
    else:
        factor = random.uniform(0.85, 1.0)
    return round(free_flow_speed * factor, 1)

    # generate speed SpeedReading per hour for a segment.
def generate_readings_for_segment(segment, num_hours = 24):
    readings = []
    for hour in range(num_hours):
        speed = generate_speed(segment.free_flow_speed, hour)
        reading = SpeedReading(segment.name, speed, hour)
        readings.append(reading)
    return readings