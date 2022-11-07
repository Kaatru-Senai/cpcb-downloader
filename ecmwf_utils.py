import os
import glob
import xarray as xr
import pandas as pd

def remove_file(parent_folder: str, extension: str):
    """
    Removes the files from operating system
    
    Args:
    parent_folder: (str) : name of the folder containing the file(s) to be removed.
    extension: (str): extension of the file(without the '.') which needs to be removed.
    """
    file_list = glob.glob(f"{parent_folder}/*.{extension}*")
    for file in file_list:
        os.remove(file)


def grib_to_csv(grib_file_path: str, csv_file_path: str):
    """
    Converts .grib file to .csv

    Args:
    grib_file_path: (str): file path of .grib file
    csv_file_path: (str): file path to store .csv file
    """
    ds = xr.open_dataset(grib_file_path)
    df = ds.to_dataframe()
    df.to_csv(csv_file_path)


def cleanup_dataframe(
                    csv_file_path: str,
                    cols_to_drop: list = ["step", "number", "surface", "valid_time"],
                    cols_to_rename: dict = {"pm2p5":"pm25", "time": "date"}):
    """
    Cleanups the csv i.e., remove unwanted columns, rename_columns.

    Args:
    csv_file_path: (str): file path to store .csv file
    cols_to_drop: (list): columns which needs to be deleted, default value caters to ecmwf data.
    cols_to_rename: (dict): columns which needs to be renamed, default value caters to ecmwf data.
                            if "pm2p5" needs to be renamed to "pm2.5", pass a dictionary as below:
                                {"pm2p5":"pm2.5"}

    """
    df = pd.read_csv(csv_file_path)
    df.drop(columns=cols_to_drop, inplace=True)
    df.rename(columns=cols_to_rename, inplace=True)

    return df
