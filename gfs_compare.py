from __future__ import annotations

from datetime import timedelta

import pandas as pd
from herbie import Herbie


def _get_cycle(time: pd.Timestamp) -> pd.Timestamp:
    """Return the latest GFS cycle prior to ``time``."""
    cycle_hour = (time.hour // 6) * 6
    cycle = time.replace(hour=cycle_hour, minute=0, second=0, microsecond=0)
    if cycle > time:
        cycle -= timedelta(hours=6)
    return cycle


def compare_metar_to_gfs(df: pd.DataFrame, lead_hours: int = 2) -> pd.DataFrame:
    """Append GFS 2 m temperature to a METAR DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with observation time in ``valid`` and station
        coordinates in ``lat`` and ``lon``.
    lead_hours : int, optional
        Round the model lead time to this interval. Defaults to ``2``.

    Returns
    -------
    pandas.DataFrame
        The original DataFrame with an added ``gfs_tmp_2m`` column.
    """
    df = df.copy()
    df["valid"] = pd.to_datetime(df["valid"])
    df["valid_hour"] = df["valid"].dt.round("1H")

    temps = []
    for _, row in df.iterrows():
        valid_time = row["valid_hour"]
        cycle = _get_cycle(valid_time)
        lead = int((valid_time - cycle).total_seconds() / 3600)
        # Round forecast hour to requested interval
        lead = int(round(lead / lead_hours) * lead_hours)

        H = Herbie(cycle, model="gfs", fxx=lead, product="pgrb2.0p25")
        ds = H.xarray("TMP:2 m")
        point = ds.sel(longitude=row["lon"], latitude=row["lat"], method="nearest")
        temps.append(point.to_array().squeeze().item())

    df["gfs_tmp_2m"] = temps
    return df
