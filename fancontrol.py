#!/usr/bin/env python3

import time

from gpiozero import OutputDevice


ON_THRESHOLD = 68 # (degrees Celsius) Fan ON
OFF_THRESHOLD = 45  # (degress Celsius) Fan OFF
SLEEP_INTERVAL = 3  # (seconds) How often the temp is checked
GPIO_PIN = 14


def get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp_str = f.read()

    try:
        return int(temp_str) / 1000
    except (IndexError, ValueError,) as e:
        raise RuntimeError('Could not parse temperature output.') from e

if __name__ == '__main__':
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()
			
        elif fan.value and temp < OFF_THRESHOLD:
            fan.off()

        time.sleep(SLEEP_INTERVAL)
