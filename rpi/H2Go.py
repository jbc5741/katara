#! /usr/bin/python2

import time
import RPi.GPIO as GPIO
import sys
import json
import numpy as np
from datetime import datetime
from setup import setup 

# Calibrates hx711
REF_UNIT = -417
# Takes median of read_num values read by hx711 
READ_NUM = 7

HOURS = 24
UNIT_PER_HOUR = 60
water_intake = [0] * (HOURS * UNIT_PER_HOUR)
water_intake_time = [0] * (HOURS * UNIT_PER_HOUR)

# drink detection
DD_MAX_LEN = 10
dd_arr = []
DD_THRESHOLD = 0.10

db = setup.firebase_config()
hx = setup.hx711_config(REF_UNIT)

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def record_water_intake(water_intake):
    date = datetime.now()
    date_str = date.strftime("%Y%m%d%H%M")
    ref = db.reference('readings')
    ref_get = ref.get()
    x = [data for data in ref_get.each() if json.loads(data.val())['datetime'] == date_str]
    y = 0
    if len(x) > 0:
        z = json.loads(x[0].val())
        y = z['water']
    water_total  = x + y 

    final_data = {'datetime': date_str, 'water': water_total}
    final_data = json.dumps(final_data)
    if len(x) == 0:
        ref.push(final_data)
    else:
        ref.child(x[0].key()).set(final_data)


stable = False
water_level = 0
while True:
    try:
        # LOGIC TO SEE IF DRINKING OCCURRED
        weight = hx.get_weight(READ_NUM)
        if weight < 0:
            weight = 0
        dd_arr.append(weight)

        if len(dd_arr) >= DD_MAX_LEN:
            dd_arr = dd_arr[1:]
        avg = np.average(dd_arr)
        if avg > 0 and np.std(dd_arr) / avg <= DD_THRESHOLD:
            stable = True
            # Stable water level, check if water level decreased
            if avg < water_level:
                water_level = avg
                record_water_intake(avg)
        else:
            stable = False

        
        # data = { "datetime": datetime.now(), "weight": val }
        # data = json.dumps(data)
        # db.child("readings").child("weights").push(data)
        # adate = datetime.now()
        # x = adate.strftime("%Y%m%d%H%M") 
        # print(val + " " + x)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
