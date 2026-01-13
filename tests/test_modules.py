"""
Unit tests for Troll-Tove modules
"""
import unittest
import time
import os
from troll_tove import (
    load_predictions_from_file,
    PredictionSelector,
    ToneFormatter,
    PredictionCache,
    IPValidator
)


class TestPredictions(unittest.TestCase):
    """Test prediction loading and selection logic"""
    
    def test_load_predictions_from_file(self):
        """Test loading predictions from file"""
        predictions = load_predictions_from_file("spaadommer_fotball.txt")
        self.assertIsInstance(predictions, list)
        self.assertGreater(len(predictions), 0)
    
    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file returns fallback"""
        predictions = load_predictions_from_file("nonexistent.txt")
        self.assertIsInstance(predictions, list)
        self.assertEqual(len(predictions), 1)
        self.assertIn("mista spådomsboka", predictions[0])
    
    def test_prediction_selector_init(self):
        """Test PredictionSelector initialization"""
        fotball = ["Glimt vinn 3-1"]
        random_pred = ["Det blir kaos"]
        selector = PredictionSelector(fotball, random_pred)
        
        self.assertEqual(selector.fotball_predictions, fotball)
        self.assertEqual(selector.random_predictions, random_pred)
    
    def test_prediction_selector_get_all(self):
        """Test getting all predictions"""
        fotball = ["Glimt vinn"]
        random_pred = ["Kaos"]
        selector = PredictionSelector(fotball, random_pred)
        
        all_preds = selector.get_all_predictions()
        self.assertEqual(len(all_preds), 2)
        self.assertIn("Glimt vinn", all_preds)
        self.assertIn("Kaos", all_preds)
    
    def test_prediction_selector_count(self):
        """Test prediction counting"""
        fotball = ["A", "B"]
        random_pred = ["C", "D", "E"]
        selector = PredictionSelector(fotball, random_pred)
        
        counts = selector.count_predictions()
        self.assertEqual(counts["fotball"], 2)
        self.assertEqual(counts["random"], 3)
        self.assertEqual(counts["total"], 5)


class TestToneFormatter(unittest.TestCase):
    """Test tone and text formatting"""
    
    def test_format_standard_intro(self):
        """Test standard intro formatting"""
        intro = ToneFormatter.format_standard_intro("Test")
        self.assertIn("Test", intro)
        self.assertIn("Troll-Tove", intro)
        self.assertIn("kula", intro)
    
    def test_format_glimt_intro(self):
        """Test Glimt intro formatting"""
        intro = ToneFormatter.format_glimt_intro("du jævel")
        self.assertIn("Du Jævel", intro)  # title() case
        self.assertIn("Aspmyra", intro)
    
    def test_format_dark_intro(self):
        """Test dark intro formatting"""
        intro = ToneFormatter.format_dark_intro("kompis")
        self.assertIn("kompis", intro)
        self.assertIn("Mørke", intro)
        self.assertIn("dystert", intro)
    
    def test_sanitize_user_name_valid(self):
        """Test sanitizing valid user name"""
        name = ToneFormatter.sanitize_user_name("Test User")
        self.assertEqual(name, "Test User")
    
    def test_sanitize_user_name_empty(self):
        """Test sanitizing empty user name"""
        name = ToneFormatter.sanitize_user_name("")
        self.assertEqual(name, "Du")
    
    def test_sanitize_user_name_too_long(self):
        """Test sanitizing too long user name"""
        name = ToneFormatter.sanitize_user_name("a" * 200)
        self.assertEqual(name, "Du")
    
    def test_sanitize_question_valid(self):
        """Test sanitizing valid question"""
        question = ToneFormatter.sanitize_question("Test question?")
        self.assertEqual(question, "Test question?")
    
    def test_sanitize_question_too_long(self):
        """Test sanitizing too long question"""
        question = ToneFormatter.sanitize_question("a" * 600)
        self.assertEqual(len(question), 500)


class TestPredictionCache(unittest.TestCase):
    """Test caching logic"""
    
    def test_cache_set_and_get(self):
        """Test basic cache set and get"""
        cache = PredictionCache(max_size=10, timeout=3600)
        cache.set("192.168.1.1", "Test prediction")
        
        result = cache.get("192.168.1.1")
        self.assertEqual(result, "Test prediction")
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = PredictionCache()
        result = cache.get("192.168.1.1")
        self.assertIsNone(result)
    
    def test_cache_max_size(self):
        """Test cache respects max size"""
        cache = PredictionCache(max_size=2, timeout=3600)
        
        cache.set("192.168.1.1", "Prediction 1")
        cache.set("192.168.1.2", "Prediction 2")
        cache.set("192.168.1.3", "Prediction 3")
        
        # First entry should be evicted
        self.assertIsNone(cache.get("192.168.1.1"))
        self.assertIsNotNone(cache.get("192.168.1.2"))
        self.assertIsNotNone(cache.get("192.168.1.3"))
    
    def test_cache_timeout(self):
        """Test cache timeout"""
        cache = PredictionCache(max_size=10, timeout=1)
        
        cache.set("192.168.1.1", "Test prediction")
        self.assertEqual(cache.get("192.168.1.1"), "Test prediction")
        
        time.sleep(1.1)
        self.assertIsNone(cache.get("192.168.1.1"))
    
    def test_cache_size(self):
        """Test cache size method"""
        cache = PredictionCache()
        self.assertEqual(cache.size(), 0)
        
        cache.set("192.168.1.1", "Test")
        self.assertEqual(cache.size(), 1)
    
    def test_cache_clear(self):
        """Test cache clear"""
        cache = PredictionCache()
        cache.set("192.168.1.1", "Test")
        cache.clear()
        
        self.assertEqual(cache.size(), 0)
        self.assertIsNone(cache.get("192.168.1.1"))
    
    def test_cleanup_expired(self):
        """Test cleanup of expired entries"""
        cache = PredictionCache(max_size=10, timeout=1)
        
        cache.set("192.168.1.1", "Test 1")
        cache.set("192.168.1.2", "Test 2")
        
        time.sleep(1.1)
        
        removed = cache.cleanup_expired()
        self.assertEqual(removed, 2)
        self.assertEqual(cache.size(), 0)


class TestIPValidator(unittest.TestCase):
    """Test IP validation logic"""
    
    def test_validate_simple_ip(self):
        """Test validating simple IP"""
        ip = IPValidator.extract_and_validate(None, "192.168.1.1")
        self.assertEqual(ip, "192.168.1.1")
    
    def test_validate_forwarded_for(self):
        """Test validating X-Forwarded-For header"""
        ip = IPValidator.extract_and_validate("10.0.0.1", "192.168.1.1")
        self.assertEqual(ip, "10.0.0.1")
    
    def test_validate_forwarded_for_list(self):
        """Test validating X-Forwarded-For with comma-separated list"""
        ip = IPValidator.extract_and_validate("10.0.0.1, 192.168.1.1", "127.0.0.1")
        self.assertEqual(ip, "10.0.0.1")
    
    def test_validate_invalid_ip(self):
        """Test validating invalid IP returns 'unknown'"""
        ip = IPValidator.extract_and_validate(None, "not-an-ip")
        self.assertEqual(ip, "unknown")
    
    def test_validate_ipv6(self):
        """Test validating IPv6 address"""
        ip = IPValidator.extract_and_validate(None, "::1")
        self.assertEqual(ip, "::1")


if __name__ == '__main__':
    unittest.main()
