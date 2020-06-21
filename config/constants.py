"""
Jup, you guessed it, this is the constants file
"""

CONFIG = "config.json"
DATABASE = "weerstathome"
SENSOR_NAMES = ["Tws1", "Tws2", "Hws", "Pws", "Lws", "Uws", "Vws", "Iws", "Tex", "Hex", "Pex", "Sex", "Dex", "Cex",
                "Rex"]
API_INITIAL = [0, 0, 0, 0, 0, 0, 0, 3600]  # [t, h, p, ws, wd, c, r, tz]
OWM_URL = "http://api.openweathermap.org/data/2.5/weather?q=Gent&appid=OwnKey"
SOCKET_PORT = 12345
NTP_URL = "pool.ntp.org"
