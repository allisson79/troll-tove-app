"""
Tests for OpenAI integration in Troll-Tove app
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import os
from troll_tove import OpenAIGenerator


class TestOpenAIGenerator(unittest.TestCase):
    """Test OpenAI generator functionality"""
    
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            generator = OpenAIGenerator()
            self.assertFalse(generator.is_enabled())
            self.assertIsNone(generator.api_key)
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch('openai.OpenAI') as mock_openai:
                generator = OpenAIGenerator()
                self.assertTrue(generator.is_enabled())
                self.assertEqual(generator.api_key, "test-key")
                mock_openai.assert_called_once()
    
    def test_default_configuration(self):
        """Test default configuration values"""
        with patch.dict(os.environ, {}, clear=True):
            generator = OpenAIGenerator()
            self.assertEqual(generator.model, "gpt-4o-mini")
            self.assertEqual(generator.max_tokens, 220)
            self.assertEqual(generator.temperature, 0.8)
            self.assertEqual(generator.timeout, 30)
    
    def test_custom_configuration(self):
        """Test custom configuration via environment"""
        env_vars = {
            "OPENAI_MODEL": "gpt-4",
            "OPENAI_MAX_TOKENS": "500",
            "OPENAI_TEMPERATURE": "0.5",
            "OPENAI_TIMEOUT": "60"
        }
        with patch.dict(os.environ, env_vars, clear=True):
            generator = OpenAIGenerator()
            self.assertEqual(generator.model, "gpt-4")
            self.assertEqual(generator.max_tokens, 500)
            self.assertEqual(generator.temperature, 0.5)
            self.assertEqual(generator.timeout, 60)
    
    def test_fallback_when_disabled(self):
        """Test that fallback is called when OpenAI is disabled"""
        generator = OpenAIGenerator()
        
        fallback_called = False
        def mock_fallback():
            nonlocal fallback_called
            fallback_called = True
            return "Fallback prediction"
        
        result = generator.generate_prediction(
            mode="standard",
            user_name="Test",
            user_question="Test question",
            fallback=mock_fallback
        )
        
        self.assertTrue(fallback_called)
        self.assertEqual(result, "Fallback prediction")
    
    @patch('openai.OpenAI')
    def test_generate_standard_prediction(self, mock_openai_class):
        """Test generating standard mode prediction"""
        # Setup mock
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "AI generated prediction"
        mock_response.usage.total_tokens = 100
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = OpenAIGenerator()
            
            result = generator.generate_prediction(
                mode="standard",
                user_name="Test User",
                user_question="What will happen?",
                fallback=lambda: "Fallback"
            )
            
            self.assertEqual(result, "AI generated prediction")
            mock_client.chat.completions.create.assert_called_once()
            
            # Check that the call included proper parameters
            call_args = mock_client.chat.completions.create.call_args
            self.assertEqual(call_args.kwargs['model'], 'gpt-4o-mini')
            self.assertEqual(call_args.kwargs['max_tokens'], 220)
            self.assertEqual(call_args.kwargs['temperature'], 0.8)
    
    @patch('openai.OpenAI')
    def test_generate_glimt_prediction(self, mock_openai_class):
        """Test generating Glimt mode prediction"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Glimt AI prediction"
        mock_response.usage.total_tokens = 100
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = OpenAIGenerator()
            
            result = generator.generate_prediction(
                mode="glimt",
                user_name="du jævel",
                user_question="Hvordan går det med Glimt?",
                fallback=lambda: "Fallback"
            )
            
            self.assertEqual(result, "Glimt AI prediction")
            
            # Check prompt includes Glimt-specific content
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            user_message = messages[1]['content']
            self.assertIn("Glimt", user_message)
            self.assertIn("fotball", user_message)
    
    @patch('openai.OpenAI')
    def test_generate_dark_prediction(self, mock_openai_class):
        """Test generating dark mode prediction"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Dark AI prediction"
        mock_response.usage.total_tokens = 100
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = OpenAIGenerator()
            
            result = generator.generate_prediction(
                mode="dark",
                user_name="kompis",
                user_question="Hva bringer mørket?",
                fallback=lambda: "Fallback"
            )
            
            self.assertEqual(result, "Dark AI prediction")
            
            # Check prompt includes dark-specific content
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            user_message = messages[1]['content']
            self.assertIn("mørk", user_message)
            self.assertIn("eksistensiell", user_message)
    
    @patch('openai.OpenAI')
    def test_fallback_on_api_error(self, mock_openai_class):
        """Test fallback when API raises error"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = OpenAIGenerator()
            
            fallback_called = False
            def mock_fallback():
                nonlocal fallback_called
                fallback_called = True
                return "Fallback prediction"
            
            result = generator.generate_prediction(
                mode="standard",
                user_name="Test",
                user_question="Test",
                fallback=mock_fallback
            )
            
            self.assertTrue(fallback_called)
            self.assertEqual(result, "Fallback prediction")
    
    @patch('openai.OpenAI')
    def test_anti_repeat_mechanism(self, mock_openai_class):
        """Test that recent answers are tracked"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Setup multiple responses
        responses = []
        for i in range(3):
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"Prediction {i}"
            mock_response.usage.total_tokens = 100
            responses.append(mock_response)
        
        mock_client.chat.completions.create.side_effect = responses
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = OpenAIGenerator(anti_repeat_size=5)
            
            # Generate multiple predictions
            for i in range(3):
                result = generator.generate_prediction(
                    mode="standard",
                    user_name="Test",
                    user_question="Test",
                    fallback=lambda: "Fallback"
                )
                self.assertEqual(result, f"Prediction {i}")
            
            # Check that recent answers are stored
            self.assertEqual(len(generator.recent_answers["standard"]), 3)
            self.assertIn("Prediction 0", generator.recent_answers["standard"])
            self.assertIn("Prediction 2", generator.recent_answers["standard"])


class TestOpenAIIntegrationInApp(unittest.TestCase):
    """Test OpenAI integration in the Flask app"""
    
    @patch('app.openai_generator')
    @patch('app.ip_cache')
    def test_index_uses_openai(self, mock_cache, mock_generator):
        """Test that index route uses OpenAI generator"""
        from app import app
        
        # Mock cache to return None (no cached value)
        mock_cache.get.return_value = None
        mock_generator.generate_prediction.return_value = "AI prediction"
        
        with app.test_client() as client:
            response = client.post('/', data={
                'navn': 'Test User',
                'sporsmal': 'Test question?'
            })
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'AI prediction', response.data)
            mock_generator.generate_prediction.assert_called_once()
    
    @patch('app.openai_generator')
    def test_glimtmodus_uses_openai(self, mock_generator):
        """Test that glimtmodus route uses OpenAI generator"""
        from app import app
        
        mock_generator.generate_prediction.return_value = "Glimt AI prediction"
        
        with app.test_client() as client:
            response = client.get('/glimtmodus')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Glimt AI prediction', response.data)
            
            # Check that it was called with correct mode
            call_args = mock_generator.generate_prediction.call_args
            self.assertEqual(call_args.kwargs['mode'], 'glimt')
    
    @patch('app.openai_generator')
    def test_darkmodus_uses_openai(self, mock_generator):
        """Test that darkmodus route uses OpenAI generator"""
        from app import app
        
        mock_generator.generate_prediction.return_value = "Dark AI prediction"
        
        with app.test_client() as client:
            response = client.get('/darkmodus')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Dark AI prediction', response.data)
            
            # Check that it was called with correct mode
            call_args = mock_generator.generate_prediction.call_args
            self.assertEqual(call_args.kwargs['mode'], 'dark')


if __name__ == '__main__':
    unittest.main()
