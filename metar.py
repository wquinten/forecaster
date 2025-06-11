import calendar
from io import StringIO
import requests
import pandas as pd


def download_monthly_metars(icao: str, year: int, month: int) -> pd.DataFrame:
    """Download a month of METAR observations from Iowa State IEM.

    Parameters
    ----------
    icao : str
        Four letter ICAO station identifier.
    year : int
        Year of desired data (UTC).
    month : int
        Month of desired data (1-12, UTC).

    Returns
    -------
    pandas.DataFrame
        DataFrame of METAR observations for the given month in UTC.
        Includes all available observation fields and the raw METAR string.
    """
    last_day = calendar.monthrange(year, month)[1]
    params = {
        "station": icao,
        "data": "all",
        "year1": year,
        "month1": month,
        "day1": 1,
        "year2": year,
        "month2": month,
        "day2": last_day,
        "tz": "Etc/UTC",
        "format": "onlycomma",
        "latlon": "no",
    }
    url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text))
