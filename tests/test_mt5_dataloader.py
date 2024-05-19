import unittest
from unittest.mock import patch
from datetime import datetime as dt

from mt5_dataloader.mt_dataloader import MTDataLoader
from mt5_dataloader.mt_utils import MTResolutions
from mt5_dataloader.mt_utils import MTRequests

RATES = {"time": [1, 2, 3],
         "open": [1, 2, 3],
         "high": [1, 2, 3],
         "low": [1, 2, 3],
         "close": [1, 2, 3],
         "spread": [1, 2, 3]}


class TestMTDataLoader(unittest.TestCase):
    """
    Tests for the MTDataLoader class
    """
    @patch("MetaTrader5.account_info")
    def setUp(self, mock_account_info):
        # Setup 
        mock_account_info.return_value = True
        self.mt_dataloader = MTDataLoader()
        self.symbol = "GBPUSD"

    @patch("MetaTrader5.copy_rates_from_pos")
    def test_get_price_data_with_position(self, mock_rates):
        """
        Tests `get_price_data` using `pos` as request type.
        """
        # Mock values returned by MT5 Terminal
        mock_rates.return_value = RATES

        # Tests valid arguments
        result = self.mt_dataloader.get_price_data(
            symbol=self.symbol,
            resolution=MTResolutions.RESOLUTION_M15.value,  # Resolution as int
            request_type=MTRequests.POSITION.value  # Request Type as string
        )

        open_sum = result.data['open'].sum()
        self.assertEquals(open_sum, 6)

        # Tests if no rates are returned
        mock_rates.return_value = None

        result = self.mt_dataloader.get_price_data(
            symbol=self.symbol,
            resolution=MTResolutions.RESOLUTION_M15,
            request_type=MTRequests.POSITION
        )

        self.assertIsNone(result)

    @patch("MetaTrader5.copy_rates_from")
    def test_get_price_data_with_date(self, mock_rates):
        """
        Tests `get_price_data` using `date` as request_type
        """
        mock_rates.return_value = RATES

        # Tests valid arguments
        result = self.mt_dataloader.get_price_data(
            symbol=self.symbol,
            resolution=MTResolutions.RESOLUTION_M15,
            request_type=MTRequests.DATE,
            end_date=dt(2024, 1, 1)
        )

        open_sum = result.data['open'].sum()
        self.assertEquals(open_sum, 6)

        # Test No date specified
        self.assertRaises(
            ValueError,
            lambda: self.mt_dataloader.get_price_data(
                symbol=self.symbol,
                resolution=MTResolutions.RESOLUTION_M15,
                request_type=MTRequests.DATE
            )
        )

        # Tests invalid date
        self.assertRaises(
            TypeError,
            lambda: self.mt_dataloader.get_price_data(
                symbol=self.symbol,
                resolution=MTResolutions.RESOLUTION_M15,
                request_type=MTRequests.DATE,
                end_date="invalid_date"
            )
        )

    @patch("MetaTrader5.copy_rates_range")
    def test_get_price_data_with_range(self, mock_rates):
        """
        Tests `get_price_data` with `rates` as request_type
        """
        mock_rates.return_value = RATES

        # Tests valid arguments
        result = self.mt_dataloader.get_price_data(
            symbol=self.symbol,
            resolution=MTResolutions.RESOLUTION_M15,
            request_type=MTRequests.RANGE,
            start_date=dt(2024, 1, 1),
            end_date=dt(2024, 2, 1)
        )

        open_sum = result.data['open'].sum()
        self.assertEqual(open_sum, 6)

        # Tests no date specified
        self.assertRaises(
            ValueError,
            lambda: self.mt_dataloader.get_price_data(
                symbol=self.symbol,
                resolution=MTResolutions.RESOLUTION_M15,
                request_type=MTRequests.RANGE
            )
        )

        # Tests invalid dates where start_date > end_date. start_date cannot be greater than end_date
        self.assertRaises(
            ValueError,
            lambda: self.mt_dataloader.get_price_data(
                symbol=self.symbol,
                resolution=MTResolutions.RESOLUTION_M15,
                request_type=MTRequests.RANGE,
                start_date=dt(2024,2,1),
                end_date=dt(2024,1,1)
            )
        )

    def test_invalid_resolution(self):
        """
        Tests `get_price_data` with invalid resolution.
        """
        self.assertRaises(
            ValueError,
            lambda: self.mt_dataloader.get_price_data(
                symbol=self.symbol,
                resolution="50000",
                request_type=MTRequests.POSITION
            )
        )

    def test_invalid_request(self):
        """
        Tests `get_price_data` with invalid request.
        """
        self.assertRaises(
            KeyError,
            lambda: self.mt_dataloader.get_price_data(
                symbol=self.symbol,
                resolution=MTResolutions.RESOLUTION_M15,
                request_type="invalid_request"
            )
        )

    @patch("MetaTrader5.copy_rates_from_pos")
    def test_no_data_found(self, mock_rates):
        """
        Tests `get_price_data` with no data found for specified symbol.
        """
        mock_rates.side_effect = KeyError

        result = self.mt_dataloader.get_price_data(
            symbol=self.symbol,
            resolution=MTResolutions.RESOLUTION_M15,
            request_type=MTRequests.POSITION
        )

        self.assertIsNone(result)

        mock_rates.return_value = None

        result = self.mt_dataloader.get_price_data(
            symbol=self.symbol,
            resolution=MTResolutions.RESOLUTION_M15,
            request_type=MTRequests.POSITION
        )

        self.assertIsNone(result)

    def test_validate_date(self):
        """
        Tests date validation function.
        """
        self.assertTrue(self.mt_dataloader.validate_date(dt(2024, 1, 1)))
        self.assertTrue(self.mt_dataloader.validate_date(dt(2024, 1, 1, 1, 1, 1)))
        self.assertFalse(self.mt_dataloader.validate_date(1234567))