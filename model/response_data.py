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
    LATITUDE = 'latitude',
    LONGITUDE = 'longitude',
    STATUS = 'status'


class ResponseDataValue(str, enum.Enum):
    FAILED = 'failed',
    SUCCESS = 'success'


class ParseData:
    def __init__(self, data: dict, meta_data: dict):
        self.data_list: dict = data
        self.meta_data: dict = meta_data

    def get(self) -> dict:
        parsed_data = {
            ResponseDataParam.SITE_ID.value: [],
            ResponseDataParam.SITE_NAME.value: [],
            ResponseDataParam.ADDRESS.value: [],
            ResponseDataParam.LATITUDE.value: [],
            ResponseDataParam.LONGITUDE.value: [],
            ResponseDataParam.FROM_DATE.value: [],
            ResponseDataParam.TO_DATE.value: [],
            ResponseDataParam.PM25.value: []
        }
        if self.data_list[ResponseDataParam.STATUS] == ResponseDataValue.SUCCESS:
            self.data_list: dict = self.data_list[ResponseDataParam.DATA]
            site_info = self.data_list[ResponseDataParam.SITE_INFO]
            for row in self.data_list[ResponseDataParam.TABULAR_DATA][ResponseDataParam.BODY_CONTENT]:
                parsed_data[ResponseDataParam.SITE_ID].append(site_info[ResponseDataParam.SITE_ID])
                parsed_data[ResponseDataParam.SITE_NAME].append(site_info[ResponseDataParam.SITE_NAME])
                parsed_data[ResponseDataParam.ADDRESS].append(site_info[ResponseDataParam.ADDRESS])
                parsed_data[ResponseDataParam.FROM_DATE].append(row[ResponseDataParam.FROM_DATE])
                parsed_data[ResponseDataParam.TO_DATE].append(row[ResponseDataParam.TO_DATE])
                parsed_data[ResponseDataParam.PM25].append(row[ResponseDataParam.PM25])
                parsed_data[ResponseDataParam.LATITUDE.value].append(self.meta_data[ResponseDataParam.LATITUDE])
                parsed_data[ResponseDataParam.LONGITUDE.value].append(self.meta_data[ResponseDataParam.LONGITUDE])
        else:
            parsed_data[ResponseDataParam.LATITUDE.value].append(self.meta_data[ResponseDataParam.LATITUDE])
            parsed_data[ResponseDataParam.LONGITUDE.value].append(self.meta_data[ResponseDataParam.LONGITUDE])
            for k, v in parsed_data.items():
                if len(v) == 0:
                    parsed_data[k].append(None)
        return parsed_data
