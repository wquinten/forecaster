import pandas as pd
from unittest import TestCase, mock
import metar

class TestDownloadMetars(TestCase):
    def test_download_monthly_metars(self):
        sample_csv = (
            "station,valid,tmpf,metar\n"
            "KAAA,2024-01-01 00:00,0.1,example1\n"
            "KAAA,2024-01-01 01:00,0.2,example2\n"
        )
        with mock.patch('metar.requests.get') as mget:
            mget.return_value.status_code = 200
            mget.return_value.text = sample_csv
            df = metar.download_monthly_metars('KAAA', 2024, 1)
        self.assertEqual(len(df), 2)
        self.assertIn('metar', df.columns)

