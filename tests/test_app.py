import unittest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
import sys
import os

# Add the parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, weighted_sum

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Sample data for mocking
        self.sample_geojson = {
            "features": [
                {
                    "properties": {
                        "PedConnect_Score": 10,
                        "LSBikConnect_Score": 10,
                        "Strava_Score": 10,
                        "UCATWKUse_Score": 10,
                        "UCATBKUse_Score": 10,
                        "Bike_Ln_Score": 10,
                        "Crss_WK_Score": 10,
                        "SidWlk_Score": 10,
                        "Safety_Score": 10,
                        "Priority_Score": 0, # Placeholder
                        "Last_Priority_Score": 0, # Placeholder
                        "Difference_Score": 0 # Placeholder
                    }
                }
            ]
        }

    def test_weighted_sum(self):
        # Create a sample DataFrame
        data = {
            'A': [10, 20],
            'B': [30, 40]
        }
        df = pd.DataFrame(data)
        weights = [0.5, 0.5]

        # Test with sum_to_one=True (default)
        # Weights normalized: 0.5/1 = 0.5 each.
        # Row 1: 10*0.5 + 30*0.5 = 5 + 15 = 20
        # Row 2: 20*0.5 + 40*0.5 = 10 + 20 = 30
        result_df = weighted_sum(df, ['A', 'B'], weights, "WeightedResult")
        self.assertIn("WeightedResult", result_df.columns)
        self.assertAlmostEqual(result_df["WeightedResult"][0], 20.0)
        self.assertAlmostEqual(result_df["WeightedResult"][1], 30.0)

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if session is initialized (implicitly by checking content or behavior)
        # We can't easily check session content directly with test_client unless we use context locals
        with self.app.session_transaction() as sess:
            # This block is executed after the request? No, test_client doesn't persist session like this easily without a request.
            # But the route sets session if not present.
            pass

        # Check security headers
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn('X-Frame-Options', response.headers)
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')
        self.assertIn('Content-Security-Policy', response.headers)

    def test_revise_weights_success(self):
        # First, hit index to initialize session
        self.app.get('/')

        data = {
            "pedconnectivity": "10",
            "bikeconnectivity": "10",
            "strava": "3.75",
            "ucatsped": "12.5",
            "ucatsbicycle": "8.75",
            "bikelane": "10",
            "crosswalk": "10",
            "sidewalk": "10",
            "safety": "25"
        }
        response = self.app.post('/revise_weights', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertEqual(json_data['pedconnectivity'], 10.0)

    def test_revise_weights_failure(self):
        # First, hit index to initialize session
        self.app.get('/')

        data = {
            "pedconnectivity": "invalid", # Invalid number
            "bikeconnectivity": "10",
            "strava": "3.75",
            "ucatsped": "12.5",
            "ucatsbicycle": "8.75",
            "bikelane": "10",
            "crosswalk": "10",
            "sidewalk": "10",
            "safety": "25"
        }

        # This should abort with 400 Bad Request
        response = self.app.post('/revise_weights', data=data)
        self.assertEqual(response.status_code, 400)

    @patch('app.json.load')
    @patch('builtins.open') # We mock open as well to avoid FileNotFoundError
    def test_geojson(self, mock_open, mock_json_load):
        # Setup mocks
        mock_json_load.return_value = self.sample_geojson
        mock_open.return_value.__enter__.return_value = MagicMock()

        # Initialize session
        self.app.get('/')

        response = self.app.get('/api/network_geojson.geojson')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIn("features", data)
        self.assertEqual(len(data["features"]), 1)
        # Check if calculations happened
        props = data["features"][0]["properties"]
        self.assertIn("Priority_Score", props)
        # Weights sum to ~100. Values are all 10. So weighted sum should be 10.
        # The sum of default weights is 100.
        self.assertAlmostEqual(props["Priority_Score"], 10.0)

if __name__ == '__main__':
    unittest.main()
