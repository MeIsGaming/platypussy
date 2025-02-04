import time
import random

# antiratelimit


def arl(duration, custom_delay):
    # Generate a random delay between 0 and 1 second
    random_delay = random.random() + custom_delay
    total_duration = duration + random_delay
    time.sleep(total_duration)
