import psycopg2
from psycopg2.extras import RealDictCursor
from secrets import pg_config
from datetime import datetime as dt
from slugify import slugify

def createTable():
    connection = psycopg2.connect(**pg_config)

    CREATE_TABLE = '''
    CREATE TABLE journeys_honza_cd (
           id SERIAL PRIMARY KEY,
           source TEXT,
           destination TEXT,
           departure_datetime TIMESTAMP,
           arrival_datetime TIMESTAMP,
           carrier TEXT,
           vehicle_type TEXT,
           price FLOAT,
           currency VARCHAR(3)
        );'''

    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE)
    cursor.commit()
    cursor.close()


def writeJourney(trains):
    values = trains.copy()
    SQL_INSERT = """
        INSERT INTO journeys_honza_cd (
            source, destination, departure_datetime,
            arrival_datetime, carrier, vehicle_type,
            price, currency)
        VALUES (%(from)s,
                %(to)s,
    		    %(departure)s,
                %(arrival)s,
                %(carrier)s,
                %(vehicle_type)s,
                %(price)s,
                %(currency)s);
    """

    connection = psycopg2.connect(**pg_config)
    values['departure'] = dt(1999, 9, 9)
    values['arrival'] = dt(1999, 9, 9)
    values['from'] = slugify(values['from'], separator='_')
    values['to'] = slugify(values['to'], separator='_')

    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(SQL_INSERT, values)
        connection.commit()


# values = {
#     'source': 'Praha',
#     'destination': 'Brno',
#     'departure_datetime': datetime(2018, 10, 21, 12, 00),
#     'arrival_datetime': datetime(2018, 10, 21, 12, 00),
#     'carrier': 'cedecko',
#     'vehicle_type': 'train',
#     'price': 222.2,
#     'currency': 'CZK'
# }
