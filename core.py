from redis import StrictRedis
from secrets import redis_config
from importlib import reload
from slugify import slugify
import json
from datetime import datetime as dt

import cd

cd = reload(cd)


class Core:

    redis = StrictRedis(socket_connect_timeout=3, **redis_config)

    def getTrains(
        self,
        station_from,
        station_to,
        departure_date=dt.now().strftime("%d.%m.%Y"),
        departure_time=dt.now().strftime("%H:%M"),
    ):

        journey = "journey:{station_from}_{station_to}_{departure_date}_cedecko".format(
            station_from=slugify(station_from, separator="_"),
            station_to=slugify(station_to, separator="_"),
            departure_date=dt.strptime(departure_date, "%d.%m.%Y").strftime(
                "%Y-%m-%d"
            ),
        )

        redis_data = self.redis.get(journey)
        if redis_data:
            return json.loads(redis_data)
        else:
            carrier = cd.CeskeDrahy()
            carrier_data = carrier.getTrains(
                station_from, station_to, departure_date, departure_time
            )
            self.redis.setex(journey, 60 * 60, json.dumps(carrier_data))
            return carrier_data
