"""
Main file
"""

from config import config_loader, constants
from connection import connect
from client_handler import debugger, uespserv
from database import dbo
from data_management import dmo, sensors as sen
from libraries import ntpztime as ztime
import time

config = config_loader.Loader(constants.CONFIG)  # load the config defined in constants.py
ip = connect.wifi(config["wifi"]["ssid"], config["wifi"]["password"])  # connect to the internet and return local ip

debug = debugger.Debug()  # initialize a debugger object

wsex = dbo.Dbo(config["server"]["host"], config["server"]["port"], constants.DATABASE, "wsex", "device", "waarde",
               debug)  # create database object for wsex
error = dbo.Dbo(config["server"]["host"], config["server"]["port"], constants.DATABASE, "error", "source", "message",
                debug)  # create database object for error

sensors = sen.Sensors(error)  # initialize the sensors (aided by error database object)
uespserv.ComsThread(sensors, ip, debug)  # start the communications thread for server-client connections

data = dmo.DataManagement(constants.SENSOR_NAMES, constants.API_INITIAL, wsex, error)  # create the data management obj

ztime.settime(error, data.api_values[-1])  # set the time, aided by an updated timezone value

error.write_s("INFO", "Boot successful: " + ip)

me = 0
while True:
    lt = time.localtime()
    date = "{:02d}/{:02d}".format(lt[2], lt[1])
    tijd = "{:02d}:{:02d}:{:02d}".format(lt[3], lt[4], lt[5])
    if lt[4] % 10 != me:  # code inside gets run every time the minute rolls over
        sensors.measure()
        data.add(t1=sensors.tem, t2=sensors.temp, h=sensors.hum, p=sensors.pres, l=sensors.light, u=sensors.uv,
                 v=sensors.vis, i=sensors.ir)  # add current measurement to dmo
        if lt[4] % 10 == 0:  # code inside gets run every 10 minutes
            data.write_to_database()  # write the contents of the dmo to the database
            if lt[3] == 3 and lt[4] == 10:  # code inside runs once a day at 03:10
                ztime.settime(error, data.api_values[-1])  # update the current time, in case of zone change or drift
    me = lt[4] % 10  # update the variable that keeps the last minute
    time.sleep(1)
