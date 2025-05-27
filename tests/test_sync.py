import os
import pytest
from unittest.mock import patch, MagicMock
from navefileuploader.sync import JiraProcessor

@pytest.fixture
def processor():
    return JiraProcessor(
        jira_username="test_user",
        jira_api_token="test_token",
        target_api_url="https://test.api",
        target_api_key="test_key"
    )

def test_download_jira_data(processor):
    with patch('requests.get') as mock_get:
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"issues": []}
        mock_get.return_value = mock_response

        # Call the method
        result = processor.download_jira_data()

        # Verify the result
        assert result == {"issues": []}
        mock_get.assert_called_once()

def test_save_to_file(processor):
    # Test data
    test_data = {"test": "data"}
    
    # Create a temporary file
    with patch('builtins.open', create=True) as mock_open:
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Call the method
        result = processor.save_to_file(test_data, "test.json")
        
        # Verify the result
        assert result == "test.json"
        mock_file.write.assert_called_once()

def test_send_to_target_api(processor):
    with patch('requests.post') as mock_post, \
         patch('builtins.open', create=True) as mock_open:
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response
        
        # Mock the file
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Call the method
        result = processor.send_to_target_api("test.json")
        
        # Verify the result
        assert result == {"status": "success"}
        mock_post.assert_called_once() 