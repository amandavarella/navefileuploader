#!/usr/bin/env python3

import requests
import json
from .masking import mask_json_file
import os
from datetime import datetime
import glob
from dotenv import load_dotenv
import gzip
import io
import sys

# Load environment variables
load_dotenv()

# JIRA Configuration
JIRA_URL = os.getenv('JIRA_URL')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

# Target API Configuration
TARGET_API_URL = os.getenv('NAVE_API_URL')
TARGET_API_KEY = os.getenv('NAVE_API_KEY')
DASHBOARD_ID = os.getenv('NAVE_DASHBOARD_ID')

def cleanup_json_files():
    """Remove any existing JSON files in the current directory"""
    json_files = glob.glob("*.json")
    for file in json_files:
        try:
            os.remove(file)
            print(f"Removed existing file: {file}")
        except Exception as e:
            print(f"Error removing file {file}: {str(e)}")

class JiraProcessor:
    def __init__(self, jira_username, jira_api_token, target_api_url, target_api_key):
        self.jira_username = jira_username
        self.jira_api_token = jira_api_token
        self.target_api_url = target_api_url
        self.target_api_key = target_api_key
        
    def download_jira_data(self):
        """Download data from JIRA agile board"""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        auth = (self.jira_username, self.jira_api_token)
        
        params = {
            'expand': 'changelog',
            'startAt': 0,
            'maxResults': 1000,
            'jql': 'ORDER BY updated DESC'
        }
        
        response = requests.get(JIRA_URL, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def save_to_file(self, data, file_path):
        """Save data to a JSON file."""
        with open(file_path, 'w') as f:
            json_str = json.dumps(data, indent=2)
            f.write(json_str)
        return file_path
    
    def send_to_target_api(self, file_path):
        """Send the masked file to the target API"""
        try:
            headers = {
                'Authorization': self.target_api_key,
                'Accept': 'application/json'
            }

            # Prepare multipart form data
            with open(file_path, 'rb') as f:
                files = {
                    'data': (os.path.basename(file_path), f, 'application/json')
                }
                data = {
                    'dashboardId': DASHBOARD_ID,
                    'cumulative': 'false'
                }

                print(f"Sending request to Nave API with dashboard ID: {DASHBOARD_ID}")
                print(f"Request URL: {self.target_api_url}")

                response = requests.post(
                    self.target_api_url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=60
                )

                if response.status_code != 200:
                    print(f"Error response from Nave API: {response.text}")
                    print(f"Request headers: {headers}")
                    print(f"Request data: {data}")
                    print(f"File size: {os.path.getsize(file_path)} bytes")

                response.raise_for_status()
                return response.json()

        except Exception as e:
            print(f"Error sending data to Nave API: {str(e)}")
            raise
    
    def process_jira_data(self):
        """Main method to process JIRA data"""
        try:
            # Download data from JIRA
            print("Downloading data from JIRA...")
            jira_data = self.download_jira_data()
            
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_file = f"raw_jira_data_{timestamp}.json"
            self.save_to_file(jira_data, raw_file)
            
            # Mask the data
            print("Masking sensitive data...")
            masked_file = f"masked_jira_data_{timestamp}.json"
            mask_json_file(raw_file, masked_file)
            
            # Send to target API
            print("Sending masked data to target API...")
            result = self.send_to_target_api(masked_file)
            
            # Clean up temporary files
            os.remove(raw_file)
            os.remove(masked_file)
            
            print("Processing completed successfully!")
            return result
            
        except Exception as e:
            print(f"Error processing JIRA data: {str(e)}")
            raise

def main():
    # Validate environment variables
    required_vars = ['JIRA_URL', 'JIRA_USERNAME', 'JIRA_API_TOKEN', 
                    'NAVE_API_URL', 'NAVE_API_KEY', 'NAVE_DASHBOARD_ID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease create a .env file with these variables. See .env.example for a template.")
        sys.exit(1)

    # Clean up any existing JSON files
    cleanup_json_files()
    
    # Initialize processor
    processor = JiraProcessor(
        jira_username=JIRA_USERNAME,
        jira_api_token=JIRA_API_TOKEN,
        target_api_url=TARGET_API_URL,
        target_api_key=TARGET_API_KEY
    )
    
    # Process the data
    try:
        processor.process_jira_data()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 