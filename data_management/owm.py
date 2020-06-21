"""
Open weather map api handler
"""

import urequests
from database import dbo
from config import constants


def call_open_weather_map(api_last, dbo_r: dbo.Dbo):
    t, h, p, ws, wd, c, r, tz = api_last  # use tuple unpacking
    r = 0  # clear the rain anyway
    try:
        response = urequests.get(constants.OWM_URL).json()  # call the OWM-API
        try:
            # try to get the timezone
            tz = response["timezone"]
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No timezone could be reached", "s")

        try:
            # try to get the temperature
            t = int(10 * (float(response["main"]["temp"]) - 273.15)) / 10
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No temperature could be reached", "s")

        try:
            # try to get the humidity
            h = response["main"]["humidity"]
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No humidity could be reached", "s")

        try:
            # try to get the pressure
            p = response["main"]["pressure"]
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No pressure could be reached", "s")

        try:
            # try to get the wind speed
            ws = response["wind"]["speed"]
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No wind speed could be reached", "s")

        try:
            # try to get the wind direction
            wd = response["wind"]["deg"]
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No wind direction could be reached", "s")

        try:
            # try to get the cloud coverage
            c = response["clouds"]["all"]
        except Exception as e:
            print(e)
            dbo_r.make_datapoint("API", "No clouds could be reached", "s")

        try:
            # try to get the rain (this mostly fails)
            r = response["rain"]["3h"]
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        dbo_r.make_datapoint("API", "The API could not be reached", "s")

    dbo_r.write_cache()  # write all existing datapoints (failures) to the database
    return [t, h, p, ws, wd, c, r, tz]
