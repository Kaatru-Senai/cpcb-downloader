import enum
import json
from cpcb_web_data import sites


class CpcbParam(str, enum.Enum):
    STATIONS = 'stations',
    CITY_NAME = 'cityName',
    CITIES = 'cities',
    CITIES_IN_STATE = 'citiesInState',
    NAME = 'name',
    STATE_NAME = 'stateName',
    STATIONS_IN_CITY = 'stationsInCity',
    ID = 'id'


def get_site_list():
    site_list = []
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
            site_list.append(
                {
                    site_id: {
                        CpcbParam.STATE_NAME: state,
                        CpcbParam.CITY_NAME: city
                    }
                }
            )
    return site_list
