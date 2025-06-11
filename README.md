# Forecaster Utilities

This repository contains utilities for working with aviation weather data.

## Downloading METAR Data

Use `metar.download_monthly_metars` to download METAR observations for a
specific station and month from the Iowa State IEM service.

Example:

```python
from metar import download_monthly_metars

df = download_monthly_metars("KDSM", 2024, 1)
print(df.head())
```
