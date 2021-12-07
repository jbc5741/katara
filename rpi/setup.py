from firebase import Firebase
from hx711 import HX711

class setup:
    def firebase_config():
        config = {
            "apiKey": "ygz7STKwh36iTYUj93trvK59HjBKe1NIBn7nY2ZK",
            "authDomain": "h2go-575f0.firebaseapp.com",
            "databaseURL": "https://h2go-575f0-default-rtdb.firebaseio.com",
            "storageBucket": ""
        }
        fb = Firebase(config)
        return fb

    def hx711_config(ref_unit):
        hx = HX711(20, 21)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(ref_unit)
        hx.reset()
        hx.tare()
        print("Tare done! Add weight now...")
        return hx