import cdsapi
import ecmwf_utils as utils
import pandas as pd
import os
import xarray as xr
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CDS_URL = os.getenv('CDS_URL')
CDS_KEY = os.getenv('CDS_KEY')
cds_client = cdsapi.Client(url=CDS_URL, key=CDS_KEY, progress=False)

def create_folders(list_of_folders: list=['temp_files', 'Downloaded_csv']): #ch
    """
    Creates the directories to store data as per the project structure.
    The function checks if the requrired directories are present in the
    current working directory, if not, they are created using the os module.
    
    Args:
    list_of_folders: (list) :List of names of folders to create or check.

    """
    for folder in list_of_folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    
def download_data(
                from_date: str,
                to_date: str,
                id: str,
                forecast_lead_time: list=['0'],
                data_from_hour: str="00:00",
                data_download_format: str='grib',
                bounding_box: list=[38, 68, 7, 98],
                data_download_home_path: str="downloaded_data",
                output_data_home_path: str="output_data",
                _FORECASTED_VARIABLES: list = ["particulate_matter_2.5um"],
                _PRODUCT: str="cams-global-atmospheric-composition-forecasts",
                _TYPE: str="forecast",
                _DATE_TIME_FORMAT: str="%Y-%m-%d",
                _QUERY_DELAY: int=1):
    """
    The function downloads the data from ECMWF(more details in README.md) for given
    time range.

    Args:
    from_date: (str) :  Date from which data is required
                        Format: "%Y-%m-%d" or "YYYY-MM-DD"
                        Example: "2022-11-26" 

    to_date: (str)  :   Date till which data is required
                        Format: "%Y-%m-%d" or "YYYY-MM-DD"
                        Example: "2022-11-31" 

    forecast_lead_time: (list) : Future prediction hour list
                                 Format: ['str', 'str']
                                 Example: ['0', '1', '2', '3']

    data_from_hour: (str) : ECMWF returns data from either midnight or 12:00 (noon time)
                            Options: "00:00" or "12:00"
                                  
    data_download_format: (str) : Format in which data needs to be returned.
                                  Options: "grib", "netcdf_zip"

    bounding_box: (list) : Geographical bounding box of query area, should be passed as list of coords.
                           Format: [north_latitude, west_longitude, south_latitude, east_longitude]
                           Example: [38, 68, 7, 98] 

    data_download_home_path: (str) : Folder path to download the .grib and .csv files which are downloaded from
                                     ECMWF servers.
                                     Example: "downloaded_data"

    output_data_home_path: (str) :  Folder path to store final, processed data.
                                    Example: "output_data"

    _FORECASTED_VARIABLES: (list) : List of variables which needs to be forecasted.
                                    Format: ['str']
                                    Example: [
                                            "particulate_matter_1um",
                                            "particulate_matter_2.5um",
                                            "particulate_matter_10um"
                                            ]

    _PRODUCT: (str) : ECMWF data product we want to use
                      Example: "cams-global-atmospheric-composition-forecasts"

    _TYPE: (str) : Type of ECMWF proudct we want to use
                   Example: "forecast"

    _DATE_TIME_FORMAT: (str) : Format of datetime objects passed
                               Format: "%Y-%m-%d" or "YYYY-MM-DD"
                               Example: "2022-11-26"

    _QUERY_DELAY: (int): ECMWF publishes data at a delay of 1 day. To ensure
                         that the input date fields take into account the delay in publishing,
                         this parameter is used.
"""

    try:
        from_date_valid = datetime.strptime(from_date, _DATE_TIME_FORMAT)
        to_date_valid = datetime.strptime(to_date, _DATE_TIME_FORMAT)
        now_time = datetime.now() - timedelta(days=_QUERY_DELAY)
        if (from_date_valid <= to_date_valid < now_time):
            cds_download_date = from_date + "/" + to_date
        else:
            print('[-] Error')
            print('    Input date fields are not correct')
            return

    except ValueError as err:
        print('[-] Error')
        print(f'    {err}')
        return 

    try:
        count = 0
        for lead in forecast_lead_time:
            csv_path = f"{data_download_home_path}/{from_date}_{lead}.csv"
            grib_path = f"{data_download_home_path}/{from_date}_{lead}.grib"

            cds_client.retrieve(
                _PRODUCT,
                {
                    'date': cds_download_date,
                    'type': _TYPE,
                    'format': data_download_format,
                    'variable': _FORECASTED_VARIABLES,
                    'time': data_from_hour,
                    'leadtime_hour':lead,
                    'area': bounding_box,
                },
                grib_path)    # name of the .grib file
            
            utils.grib_to_csv(grib_file_path=grib_path, csv_file_path=csv_path)
            output = utils.cleanup_dataframe(csv_file_path=csv_path)
            output["pm25"] =  1e+9 * output["pm25"]
            output.rename(columns={"pm25": f"hour_{int(lead)}"}, inplace=True)
            
            if count == 0:
                data = output[["date", "latitude","longitude"]]
            
            output.drop(columns=["latitude","longitude", "date"], inplace=True)
            data = pd.concat([data, output], axis=1)

            utils.remove_file(parent_folder= "downloaded_data", extension="grib")
            utils.remove_file(parent_folder="downloaded_data", extension="csv")
            
            count += 1

        data.to_csv(f"{output_data_home_path}/{id}.csv", index=False) #ch
        print('[+] Download complete')

    except Exception as err:
        print('[-] Error')
        print(f'    {err}')




        

def ecmwf_data_download(f_date, t_date, id):#ch
    create_folders()
    download_data(
                from_date=f_date,#ch
                to_date=t_date,#ch
                process_id = id,#ch
                forecast_lead_time=['0', '1', '2'],
                data_from_hour="00:00",
                data_download_format='grib',
                bounding_box=[38, 68, 7, 98],
                data_download_home_path="downloaded_data",
                output_data_home_path="output_data",
                _FORECASTED_VARIABLES=["particulate_matter_2.5um"],
                _PRODUCT="cams-global-atmospheric-composition-forecasts",
                _TYPE="forecast",
                _DATE_TIME_FORMAT="%Y-%m-%d",
                _QUERY_DELAY=1)