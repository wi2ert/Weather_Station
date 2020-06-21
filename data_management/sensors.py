"""
Local Sensor reading class
"""

from machine import I2C, Pin
from dht import DHT22
from libraries.bmp180 import BMP180
from libraries.bh1750 import BH1750
from libraries.si1145 import SI1145
from database import dbo


class Sensors:
    def __init__(self, dbo_r: dbo.Dbo):
        print("Initializing sensors")
        scl = Pin(22, Pin.OUT, Pin.PULL_UP)
        sda = Pin(21, Pin.OUT, Pin.PULL_UP)
        bus = I2C(scl=scl, sda=sda, freq=100000)

        self.error = dbo_r
        self.sdht = DHT22(Pin(15, Pin.IN, Pin.PULL_UP))
        self.bmp180 = BMP180(bus)
        self.bmp180.oversample_sett = 3
        self.bmp180.baseline = 101325
        self.il = BH1750(bus)
        self.suvi = SI1145(bus)

        self.tem = 0
        self.hum = 0
        self.temp = 0
        self.pres = 0
        self.light = 0
        self.uv = 0
        self.vis = 0
        self.ir = 0

    def measure(self):
        try:
            self.sdht.measure()  # Poll sensor
            self.tem = round(self.sdht.temperature(), 1)
            self.hum = round(self.sdht.humidity(), 1)
        except Exception as e:
            print(e)
            self.error.make_datapoint("LOCAL", "DHT22: " + str(e), "s")
        try:
            self.temp = round(self.bmp180.temperature, 1)
            self.pres = round(self.bmp180.pressure / 100, 1)
        except Exception as e:
            print(e)
            self.error.make_datapoint("LOCAL", "BMP180: " + str(e), "s")
        try:
            self.light = round(self.il.luminance(BH1750.ONCE_HIRES_1), 1)
        except Exception as e:
            print(e)
            self.error.make_datapoint("LOCAL", "BH1750: " + str(e), "s")
        try:
            l = []
            while len(l) < 5:
                u = round(self.suvi.read_uv, 1)
                if u < 11000:
                    l.append(u)
            self.uv = sorted(l)[2]
            sir = self.suvi.read_ir
            svi = self.suvi.read_visible
            self.ir = round((sir>254)*4.8*(sir-254), 1)-0.5
            self.vis = round((svi>261)*51*(svi-261)-0.9*(sir>254)*(sir-254), 1)-10
        except Exception as e:
            print(e)
            self.error.make_datapoint("LOCAL", "GY1145: " + str(e), "s")
        self.error.write_cache()

    def __str__(self):
        self.measure()
        return str(self.tem) + "(C)", str(self.temp) + "(C)", str(self.hum) + "(%)", str(self.pres) + "(hPa)", str(
            self.light) + "(lux)", "UV :" + str(self.uv), "Vis :" + str(self.vis), "IR :" + str(self.ir)
