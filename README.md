# Forecaster Utilities

This repository contains utilities for working with aviation weather data.

## Installation

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Downloading METAR Data

Use `metar.download_monthly_metars` to download METAR observations for a
specific station and month from the Iowa State IEM service.

Example:

```python
from metar import download_monthly_metars

df = download_monthly_metars("KDSM", 2024, 1)
print(df.head())
```

## Comparing to GFS

Use `gfs_compare.compare_metar_to_gfs` to append GFS model temperature to a
DataFrame of METAR observations. The function rounds each observation time to
nearest hour, finds the latest GFS cycle before that time, and reads the 2 m
temperature forecast using Herbie. The lead time can be adjusted with the
`lead_hours` parameter (2 by default).

Example:

```python
from metar import download_monthly_metars
from gfs_compare import compare_metar_to_gfs

metars = download_monthly_metars("KDSM", 2024, 1)
metars["lat"] = 41.534
metars["lon"] = -93.660
comp = compare_metar_to_gfs(metars)
print(comp[["valid", "gfs_tmp_2m"]].head())
```
