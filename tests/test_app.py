"""
Simple tests for Troll-Tove Flask app
"""
import unittest
import time
from app import app
from troll_tove import PredictionCache


class TrollToveTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
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
    
    def test_index_page_loads(self):
        """Test that index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Troll-Tove sin Sp\xc3\xa5krok', response.data)
    
    def test_glimtmodus_loads(self):
        """Test that Glimt mode loads successfully"""
        response = self.client.get('/glimtmodus')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Troll-Tove har sp\xc3\xa5dd!', response.data)
    
    def test_darkmodus_loads(self):
        """Test that Dark mode loads successfully"""
        response = self.client.get('/darkmodus')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Troll-Tove har sp\xc3\xa5dd!', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('fotball_predictions', data)
        self.assertIn('random_predictions', data)
        self.assertGreater(data['fotball_predictions'], 0)
        self.assertGreater(data['random_predictions'], 0)
    
    def test_form_submission(self):
        """Test form submission with valid data"""
        response = self.client.post('/', data={
            'navn': 'Test User',
            'sporsmal': 'Test question?'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Troll-Tove har sp\xc3\xa5dd!', response.data)
        self.assertIn(b'Test User', response.data)
    
    def test_form_validation(self):
        """Test that form handles empty/invalid input"""
        # Empty name should default to "Du"
        response = self.client.post('/', data={
            'navn': '',
            'sporsmal': 'Test?'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Du', response.data)
    
    def test_404_error_page(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)
        self.assertIn(b'Troll-Tove finner ikkje denne sida', response.data)
    
    def test_static_files_exist(self):
        """Test that static files are accessible"""
        # Test CSS file
        response = self.client.get('/static/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Troll-Tove', response.data)
        
        # Test JavaScript file
        response = self.client.get('/static/script.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'showToast', response.data)


if __name__ == '__main__':
    unittest.main()
