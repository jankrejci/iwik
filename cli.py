from importlib import reload

import core
core = reload(core)


REQUESTS = (
    {
        "station_from": "Brno",
        "station_to": "Česká Třebová",
        "departure_date": "9.12.2018",
        "departure_time": "17:00",
    },
    {
        "station_from": "Praha",
        "station_to": "Brno",
        # "departure_date": "9.12.2018",
        # "departure_time": "17:00",
    },
    {
        "station_from": "Litomyšl",
        "station_to": "Choceň",
        "departure_date": "9.12.2018",
        "departure_time": "13:15",
    },
    {
        "station_from": "Letohrad",
        "station_to": "Žamberk",
        "departure_date": "12.12.2018",
        "departure_time": "13:15",
    },
)


data = REQUESTS[1]

app = core.Core()
app.getTrains(**data)
