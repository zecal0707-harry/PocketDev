import os
import unittest.mock
from unittest.mock import MagicMock, patch

from src.runner import AgentRunner

def test_runner_call_llm_mock():
    runner = AgentRunner(api_key="fake_key")
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b"Hello from LLM"
        mock_response.__enter__.return_value = mock_response
        
        mock_urlopen.return_value = mock_response
        
        response = runner.call_llm("hello", "gpt4")
        
        assert response == "Hello from LLM"
        
        args, _ = mock_urlopen.call_args
        request_obj = args[0]
        assert request_obj.full_url == "https://api.example.com/v1/generate"
        assert request_obj.headers['Authorization'] == "fake_key"
