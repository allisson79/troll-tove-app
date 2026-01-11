"""
Simple tests for Troll-Tove Flask app
"""
import unittest
import time
from app import app, PredictionCache


class TrollToveTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        # Note: test_client() may have issues with older Werkzeug versions
        # These tests verify the core logic instead
    
    def test_prediction_cache(self):
        """Test PredictionCache functionality"""
        cache = PredictionCache(max_size=2, timeout=3600)
        
        # Test set and get
        cache.set("192.168.1.1", "Test prediction")
        result = cache.get("192.168.1.1")
        self.assertEqual(result, "Test prediction")
        
        # Test cache miss
        result = cache.get("192.168.1.2")
        self.assertIsNone(result)
        
        # Test max size
        cache.set("192.168.1.2", "Prediction 2")
        cache.set("192.168.1.3", "Prediction 3")  # Should evict first entry
        
        self.assertIsNone(cache.get("192.168.1.1"))  # Evicted
        self.assertIsNotNone(cache.get("192.168.1.2"))
        self.assertIsNotNone(cache.get("192.168.1.3"))
    
    def test_prediction_cache_timeout(self):
        """Test cache timeout"""
        cache = PredictionCache(max_size=10, timeout=1)
        
        cache.set("192.168.1.1", "Test prediction")
        result = cache.get("192.168.1.1")
        self.assertEqual(result, "Test prediction")
        
        # Wait for timeout
        time.sleep(1.1)
        result = cache.get("192.168.1.1")
        self.assertIsNone(result)  # Should be expired
    
    def test_app_routes_exist(self):
        """Test that routes are registered"""
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        self.assertIn('/', rules)
        self.assertIn('/health', rules)
        self.assertIn('/glimtmodus', rules)
        self.assertIn('/darkmodus', rules)


if __name__ == '__main__':
    unittest.main()
