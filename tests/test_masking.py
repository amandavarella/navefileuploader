import json
import os
import tempfile
from navefileuploader.masking import mask_json_file, mask_data

def test_mask_data():
    # Test data
    test_data = {
        "fields": {
            "summary": "Test issue",
            "description": "Test with email@example.com and https://example.com",
            "assignee": {
                "displayName": "John Doe",
                "emailAddress": "john@example.com"
            }
        },
        "changelog": {
            "histories": [
                {
                    "author": {
                        "displayName": "Jane Smith",
                        "emailAddress": "jane@example.com"
                    },
                    "items": [
                        {
                            "field": "description",
                            "fromString": "Old text",
                            "toString": "New text"
                        }
                    ]
                }
            ]
        }
    }

    # Mask the data
    masked = mask_data(test_data)

    # Verify the masking
    assert masked["fields"]["summary"] != "Test issue"
    assert masked["fields"]["description"] != "Test with email@example.com and https://example.com"
    assert masked["fields"]["assignee"]["displayName"] != "John Doe"
    assert masked["fields"]["assignee"]["emailAddress"] != "john@example.com"
    assert masked["changelog"]["histories"][0]["author"]["displayName"] != "Jane Smith"
    assert masked["changelog"]["histories"][0]["author"]["emailAddress"] != "jane@example.com"
    assert masked["changelog"]["histories"][0]["items"][0]["fromString"] != "Old text"
    assert masked["changelog"]["histories"][0]["items"][0]["toString"] != "New text"

def test_mask_json_file():
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file, \
         tempfile.NamedTemporaryFile(mode='w', delete=False) as output_file:
        
        # Write test data
        test_data = {
            "fields": {
                "summary": "Test issue",
                "description": "Test with email@example.com"
            }
        }
        json.dump(test_data, input_file)
        input_file.flush()
        
        # Mask the file
        mask_json_file(input_file.name, output_file.name)
        
        # Read and verify the masked data
        with open(output_file.name, 'r') as f:
            masked = json.load(f)
        
        assert masked["fields"]["summary"] != "Test issue"
        assert masked["fields"]["description"] != "Test with email@example.com"
        
        # Clean up
        os.unlink(input_file.name)
        os.unlink(output_file.name) 