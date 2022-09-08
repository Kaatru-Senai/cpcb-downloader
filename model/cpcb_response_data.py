import enum


class ResponseDataParam(str, enum.Enum):
    DATA = 'data',
    TABULAR_DATA = 'tabularData',
    BODY_CONTENT = 'bodyContent',
    FROM_DATE = 'from date',
    TO_DATE = 'to date',
    PM25 = 'PM2.5',
    EXCEEDING = 'exceeding',
    SITE_ID = 'siteId',
    CITY = 'city',
    STATE = 'state',
    DISTRICT = 'district',
    SITE_NAME = 'siteName',
    ADDRESS = 'address',
    SITE_INFO = 'siteInfo'


class ParseData:
    def __init__(self, data: dict):
        self.data_list: dict = data[ResponseDataParam.DATA]

    def get(self) -> dict:
        site_info = self.data_list[ResponseDataParam.SITE_INFO]
        parsed_data = {
            ResponseDataParam.SITE_ID.value: [],
            ResponseDataParam.SITE_NAME.value: [],
            ResponseDataParam.STATE.value: [],
            ResponseDataParam.CITY.value: [],
            ResponseDataParam.DISTRICT.value: [],
            ResponseDataParam.ADDRESS.value: [],
            ResponseDataParam.FROM_DATE.value: [],
            ResponseDataParam.TO_DATE.value: [],
            ResponseDataParam.PM25.value: []
        }
        for row in self.data_list[ResponseDataParam.TABULAR_DATA][ResponseDataParam.BODY_CONTENT]:
            parsed_data[ResponseDataParam.SITE_ID].append(site_info[ResponseDataParam.SITE_ID])
            parsed_data[ResponseDataParam.SITE_NAME].append(site_info[ResponseDataParam.SITE_NAME])
            parsed_data[ResponseDataParam.STATE].append(site_info[ResponseDataParam.STATE])
            parsed_data[ResponseDataParam.CITY].append(site_info[ResponseDataParam.CITY])
            parsed_data[ResponseDataParam.DISTRICT].append(site_info[ResponseDataParam.DISTRICT])
            parsed_data[ResponseDataParam.ADDRESS].append(site_info[ResponseDataParam.ADDRESS])
            parsed_data[ResponseDataParam.FROM_DATE].append(row[ResponseDataParam.FROM_DATE])
            parsed_data[ResponseDataParam.TO_DATE].append(row[ResponseDataParam.TO_DATE])
            parsed_data[ResponseDataParam.PM25].append(row[ResponseDataParam.PM25])
        return parsed_data

