import enum
import json

from cpcb_stations_info import cpcb_station_locations
from cpcb_web_data import sites


class CpcbParam(str, enum.Enum):
    STATIONS = 'stations',
    CITY_NAME = 'cityName',
    CITIES = 'cities',
    CITIES_IN_STATE = 'citiesInState',
    NAME = 'name',
    STATE_NAME = 'stateName',
    STATIONS_IN_CITY = 'stationsInCity',
    ID = 'id',
    LATITUDE = 'latitude',
    LONGITUDE = 'longitude'


key = "Station Name"
default = {
    'Station Name': 'Marhatal, Jabalpur - MPPCB',
    'latitude': 23.1608938,
    'longitude': 79.9497702
}


def get_site_list():
    site_list = []
    state: str = ''
    cpcb_web_data = json.loads(sites)
    for place in cpcb_web_data[CpcbParam.STATIONS]:
        city = place[CpcbParam.CITY_NAME]
        for states in cpcb_web_data[CpcbParam.CITIES]:
            for i in states[CpcbParam.CITIES_IN_STATE]:
                if i[CpcbParam.NAME] == city:
                    state = states[CpcbParam.STATE_NAME]
                    break
        for station in place[CpcbParam.STATIONS_IN_CITY]:
            site_id = station[CpcbParam.ID]
            address = station[CpcbParam.NAME]
            cpcb_station = next(filter(lambda d: d.get(key) == address, cpcb_station_locations), None)
            if not cpcb_station:
                cpcb_station = default
            site_list.append(
                {
                    site_id: {
                        CpcbParam.STATE_NAME.value: state,
                        CpcbParam.CITY_NAME.value: city,
                        CpcbParam.LATITUDE.value: cpcb_station[CpcbParam.LATITUDE],
                        CpcbParam.LONGITUDE.value: cpcb_station[CpcbParam.LONGITUDE]
                    }
                }
            )
    return site_list


if __name__ == '__main__':
    print(len(get_site_list()))
