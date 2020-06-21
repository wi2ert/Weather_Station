"""
Data management object
"""

from data_management import owm
from database import dbo


class DataManagement:
    def __init__(self, sensornames, api_initial, wsex: dbo.Dbo, error: dbo.Dbo):
        self.sensornames = sensornames
        self.api_values = api_initial
        self.wsex = wsex
        self.error = error
        self.__reset()  # initialize all object variables
        print("Creating data management object")

    def __reset(self):
        self.t1cn = 0
        self.t2cn = 0
        self.hcn = 0
        self.pcn = 0
        self.lcn = 0
        self.ucn = 0
        self.vcn = 0
        self.icn = 0
        self.cn = 0

    def __accumulate_data(self):
        cn = self.cn  # short abbreviation
        self.api_values = owm.call_open_weather_map(self.api_values, self.error)  # update internal api_values
        data = [self.t1cn / cn, self.t2cn / cn, self.hcn / cn, self.pcn / cn, self.lcn / cn, self.ucn / cn,
                self.vcn / cn, self.icn / cn] + self.api_values[:-1]  # compile all the data in a list
        self.__reset()  # reset all the internal counters
        return data

    def add(self, t1, t2, h, p, l, u, v, i):  # add a new measurement to the data management object
        self.t1cn += t1
        self.t2cn += t2
        self.hcn += h
        self.pcn += p
        self.lcn += l
        self.ucn += u
        self.vcn += v
        self.icn += i
        self.cn += 1

    def write_to_database(self):
        data = self.__accumulate_data()
        for i, e in enumerate(self.sensornames):
            self.wsex.make_datapoint(e, data[i])  # use wildcard as type, so it doesn't get stringified
        self.wsex.write_cache()  # write all existing datapoints in memory to the database
