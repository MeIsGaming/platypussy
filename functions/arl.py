import time
import random

# antiratelimit
def arl(duration):
    random_delay = random.random()  # Generate a random delay between 0 and 1 second
    total_duration = duration + random_delay
    time.sleep(total_duration)

