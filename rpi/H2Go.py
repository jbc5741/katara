#! /usr/bin/python2

import time
import RPi.GPIO as GPIO
import sys
import json
import numpy as np
from datetime import datetime
from setup import setup 

# def detect(chn):
#     print(chn)

# BtnPin = 17
# # GPIO.setmode(GPIO.BOARD) 
# # GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# # GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

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
fb = setup.firebase_config()
hx = setup.hx711_config(REF_UNIT)

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def record_water_intake(prev_water_level, water_intake, fb):
    db = fb.database()
    date = datetime.now()
    date_str = date.strftime("%Y%m%d%H%M")
    ref = db.child('readings')
    ref_get = ref.get()
    x = []
    if ref_get is not None:
        x = [data for data in ref_get.each() if json.loads(data.val())['datetime'] == date_str]
    y = 0
    if len(x) > 0:
        z = json.loads(x[0].val())
        y = z['water']
    water_total  = prev_water_level - water_intake + y
    print(water_total)
    final_data = {'datetime': date_str, 'water': water_total}
    final_data = json.dumps(final_data)
    print(final_data)
    ref = fb.database().child('readings')
    if len(x) == 0:
        print("Sending new data")
        ref.push(final_data)
    else:
        print("Updating new data")
        ref.child(x[0].key()).set(final_data)
    return


date = datetime.now()
new_minute = (date.minute ) % 60
record_date = datetime(date.year, date.month, date.day, date.hour, date.minute )
record_date_str = record_date.strftime("%Y%m%d%H%M") 
data = { "datetime": record_date_str, "water": 0 }
data = json.dumps(data)
fb.database().child("readings").push(data)

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
        ss = np.std(dd_arr)
        print("water level: ", water_level)
        print("average: ",  avg)
        print("std: ",  ss)
        print()
        if avg < 20:
            ss = 0
        if avg > 0 and ss / avg <= DD_THRESHOLD:
            stable = True
            # Stable water level, check if water level decreased
            if avg < water_level - ss:
                print("sending data...")
                record_water_intake(water_level, avg, fb)
                water_level = avg
            elif avg > water_level + ss + 10: 
                water_level = avg
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
