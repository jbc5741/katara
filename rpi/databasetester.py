from datetime import datetime
from firebase import Firebase
import json
from datetime import datetime
import random

config = {
    "apiKey": "ygz7STKwh36iTYUj93trvK59HjBKe1NIBn7nY2ZK",
    "authDomain": "h2go-575f0.firebaseapp.com",
    "databaseURL": "https://h2go-575f0-default-rtdb.firebaseio.com",
    "storageBucket": ""
}
fb = Firebase(config)
db = fb.database()


# for i in range(10):
#     date = datetime.now()
#     new_minute = (date.minute + i ) % 60
#     record_date = datetime(date.year, date.month, date.day, date.hour, date.minute + i)
#     record_date_str = record_date.strftime("%Y%m%d%H%M") 
#     data = { "datetime": record_date_str, "water": random.randint(20, 120) }
#     data = json.dumps(data)
#     db.child("readings").push(data)

# for i in range(10):
#     date = datetime.now()
#     new_minute = (date.minute + i ) % 60
#     record_date = datetime(date.year, date.month, date.day, date.hour, date.minute + i)
#     record_date_str = record_date.strftime("%Y%m%d%H%M") 
#     data = { "water": random.randint(20, 120) }
#     data = json.dumps(data)
#     db.child("readings").child(record_date_str).push(data)

ref = db.child('readings').get()
x = [data for data in ref.each() if json.loads(data.val())['datetime'] == '202112061537']
y = x[0].key()
print(type("ds"))
print(y)
z = {'datetime': '202112061538', 'water': 1111}
z = json.dumps(z)
print(z)
db.child('readings').child(y).set(z)
# print(ref)  

# x[0].update({'water': 1111})


# for data in ref.each():
#     print(json.loads(data.val())['datetime'])