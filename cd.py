from requests_html import HTMLSession
from datetime import datetime as dt
import json
import re


class CeskeDrahy:
    API_ADDRESS = "https://www.cd.cz/spojeni-a-jizdenka/"
    API_GUID_ADDRESS = "https://www.cd.cz/spojeni-a-jizdenka/spojeni-tam/"
    API_REQUEST = {
        "ttCombination": "25",
        "isReturnOnly": "false",
        "stations[from][listID]": "1",
        "stations[from][name]": "",
        "stations[from][errorName]": "From",
        "stations[to][listID]": "1",
        "stations[to][name]": "",
        "stations[to][errorName]": "To",
        "services[bike]": "false",
        "services[children]": "false",
        "services[wheelChair]": "false",
        "services[refreshment]": "false",
        "services[carTrain]": "false",
        "services[silentComp]": "false",
        "services[ladiesComp]": "false",
        "services[powerSupply]": "false",
        "services[wiFi]": "false",
        "services[inSenior]": "false",
        "services[serviceClass]": "Class2",
        "dateTime[isReturn]": "false",
        "dateTime[date]": "",
        "dateTime[time]": "",
        "dateTime[isDeparture]": "true",
        "dateTime[dateReturn]": "",
        "dateTime[timeReturn]": "",
        "dateTime[isDepartureReturn]": "true",
        "params[onlyDirectConnections]": "false",
        "params[onlyConnWithoutRes]": "false",
        "params[useBed]": "NoLimit",
        "params[deltaPMax]": "-1",
        "params[maxChanges]": "4",
        "params[minChangeTime]": "-1",
        "params[maxChangeTime]": "240",
        "params[onlyCD]": "false",
        "params[onlyCDPartners]": "true",
        "params[historyTrain]": "false",
        "params[psgOwnTicket]": "false",
        "params[addServiceReservation]": "false",
        "params[addServiceDog]": "false",
        "params[addServiceBike]": "false",
        "params[addServiceSMS]": "false",
        "passengers[passengers][0][id]": "1",
        "passengers[passengers][0][typeID]": "5",
        "passengers[passengers][0][count]": "1",
        "passengers[passengers][0][age]": "-1",
        "passengers[passengers][0][ageState]": "0",
        "passengers[passengers][0][cardIDs]": "",
        "passengers[passengers][0][isFavourite]": "false",
        "passengers[passengers][0][isDefault]": "false",
        "passengers[passengers][0][isSelected]": "true",
        "passengers[passengers][0][nickname]": "",
        "passengers[passengers][0][phone]": "",
        "passengers[passengers][0][cardTypeID]": "0",
        "passengers[passengers][0][fullname]": "",
        "passengers[passengers][0][cardNumber]": "",
        "passengers[passengers][0][birthdate]": "",
        "passengers[passengers][0][avatar]": "",
        "passengers[passengers][0][image]": "",
    }


    def getTrains(self, station_from, station_to, departure_date, departure_time):
        user_request = {
            "stations[from][name]": station_from,
            "stations[to][name]": station_to,
            "dateTime[date]": departure_date,
            "dateTime[time]": departure_time,
            "dateTime[dateReturn]": departure_date,
            "dateTime[timeReturn]": departure_time,
        }
        self.API_REQUEST.update(user_request)

        session = HTMLSession()
        response = session.post(url=self.API_ADDRESS, data=self.API_REQUEST)

        guid = json.loads(response.text)["guid"]
        response = session.get(self.API_GUID_ADDRESS + str(guid))
        clean_json = json.loads(re.findall(r"var model = (.*)", response.text)[0][:-2])
        
        with open('carrier.json', 'w') as file:
            file.write(clean_json)

        trains = []
        for item in clean_json["list"]:
            trains.append(
                {
                    "name": item["trains"][0]["trainName"],
                    "from": item["trains"][0]["from"],
                    "to": item["trains"][0]["to"],
                    # TODO pouzivat datetime object !!!!!
                    "departure": item["trains"][0]["depTime"],
                    "arrival": item["trains"][0]["arrTime"],
                    "delay": item["trains"][0]["delay"],
                    "price": int(item["price"]["price"] / 100),
                    "currency": "CZK",
                    "vehicle_type": 'train',
                    "carrier": "CD",
                }
            )
        return trains
