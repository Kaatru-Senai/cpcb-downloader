# CPCB downloader
A tool to download data from the CPCB website.


## Getting Started
CPCB downloader is a Python Application which makes downloading data from CPCB website easy.

There is a list of stations with the respective `site id` which will be used to make request to the cpcb website. Once data from every station is downloaded, the response data will be parsed and merged into a `pandas dataframe`. At the end the dataframe will be converted into a `csv file` and saved in the working directory.


### Installing

A step by step series of examples that tell you how to get a development env running

1. Install all the requirements

```
pip install -r requirements.txt
```

2. Run the main file.
```
python main.py -fd <from-date> -td <to-date>
```

The main file takes two arguments which are `from date (fd)` and `to date (td)`. The dates are used to get data during that time period.


It will take around `8-10 minutes` for all the station's data to be downloaded.

## Authors

* **Suvindran**
* **Abhijeet Ranjan**


## License
This project is licensed under the BSD License - see the [LICENSE.md](LICENSE.md) file for details
