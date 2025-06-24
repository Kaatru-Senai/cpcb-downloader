import base64
import json
from datetime import datetime


class Payload:
    datetime_format = '%d-%m-%Y T%H:%M:%SZ'

    def __init__(self, state: str, city: str, site_id: str, start_date: datetime, end_date: datetime):
        self.payload = {
            "draw": 1,
            "columns": [
                {"data": 0,
                 "name": "",
                 "searchable": True,
                 "orderable": False,
                 "search": {
                     "value": "",
                     "regex": False
                 }
                 }
            ],
            "order": [], "start": 0, "length": 6000, "search": {"value": "", "regex": False},
            "filtersToApply": {
                "parameter_list": [{"id": 0, "itemName": "PM2.5", "itemValue": "parameter_193"}],
                "criteria": "1 Hours", "reportFormat": "Tabular",
                "fromDate": f"{start_date.strftime(self.datetime_format)}",
                "toDate": f"{end_date.strftime(self.datetime_format)}", "state": f"{state}", "city": f"{city}",
                "station": f"{site_id}", "parameter": ["parameter_193"], "parameterNames": ["PM2.5"]},
            "pagination": 1}

    def generate(self) -> str:
        base64_bytes = base64.b64encode(str(json.dumps(self.payload)).encode('ascii'))
        base64_string = base64_bytes.decode("ascii")
        return base64_string
