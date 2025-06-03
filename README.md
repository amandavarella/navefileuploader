# NaveFileUploader

A Python package for masking and syncing JIRA data to Nave.

## 📝 Description

This project provides two main functionalities to mask sensitive data from JIRA before sending it to Nave:

1. A local file masking function that processes Jira JSON files for manual upload through Nave's interface
2. An automated processor that fetches data from JIRA, masks it, and uploads it directly through Nave's API

## 🔑 Getting Your Jira API Token

Before you begin, you'll need to obtain a Jira API token. Here's how:

1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Log in with your Atlassian account
3. Click "Create API token"
4. Give your token a label (e.g., "NaveFileUploader")
5. Click "Create"
6. Copy the token immediately - you won't be able to see it again!

**Important:** Store this token securely. You'll need it for the environment configuration step.

## 🔐 Getting Your Nave API Token and Dashboard ID

You'll also need a Nave API token to use this package. To obtain one:

1. Contact the Nave team
2. Request an API token for the NaveFileUploader integration

To find your dashboard ID:
1. Go to your Nave dashboard in the browser
2. Look at the URL: `https://file.getnave.com/dashboard/<your-dashboard-id>`
3. The dashboard ID is the slug at the end of the URL

**Important:** Keep these credentials secure and never share them publicly.

## 🔧 What the masking feature does

* Replaces all email addresses with fake ones
* Masks all URLs (http/https) with randomised placeholders
* Anonymises names in `"displayName"`
* Replaces content of fields like `"goal"`, `"body"`, `"summary"`, and `"description"` with randomised text
* Randomises `"fromString"` and `"toString"` for specific fields like `"assignee"`, `"Contributors"`, `"summary"`, and `"Attachment"`

## 🚀 Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amandavarella/navefileuploader.git
   cd navefileuploader
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Add the virtual environment's bin directory to your PATH (optional, but recommended):
   ```bash
   echo 'export PATH="$(pwd)/venv/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

### Environment Configuration

Before running any scripts, create a `.env` file in the project root with your credentials. You can use the provided `.env.example` as a template:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your actual Jira and Nave credentials in the `.env` file:
   ```
   # JIRA Configuration
   JIRA_URL=your_jira_url
   JIRA_USERNAME=your_username
   JIRA_API_TOKEN=your_token

   # Nave Configuration
   NAVE_API_URL=https://file.getnave.com/api/dashboards/update
   NAVE_API_KEY=your_api_key
   NAVE_DASHBOARD_ID=your_dashboard_id
   ```

**Note:**
- Never commit your `.env` file to version control.
- Only share `.env.example` with placeholder values.

### Usage

#### 1. Local File Masking

This functionality processes Jira JSON files for manual upload through Nave's interface.

To get your JIRA data:
1. Go to this address:
   ```bash
   https://<your-company>.atlassian.net/rest/agile/1.0/board/<your-board-id>/issue?expand=changelog&startAt=0&maxResults=1000
   ```
2. In your browser, go to File > Save Page As
3. Save the file as `issue.json` in the root directory of this app

Then run the command-line tool:
```bash
nave-mask
```

The tool will:
1. Look for `issue.json` in the current directory
2. Create a masked version as `masked_issue.json` in the same directory

After the tool completes:
Go to your Nave's dashboard: 
```bash
https://file.getnave.com/update/<your-dashboard-id>
```
and upload the `masked_issue.json`

Or using the Python API:
```python
from navefileuploader import mask_json_file

# To mask a file
mask_json_file("issue.json", "masked_issue.json")
```

#### 2. Automated JIRA Sync

This functionality fetches data from JIRA, masks it, and uploads it directly through Nave's API.

Using the command-line tool:
```bash
nave-sync
```

Or using the Python API:
```python
from navefileuploader import JiraProcessor

# To sync data
processor = JiraProcessor(
    jira_username="your_username",
    jira_api_token="your_token",
    target_api_url="your_api_url",
    target_api_key="your_api_key"
)
processor.process_jira_data()
```

## 📂 Project Structure

```
navefileuploader/
├── src/                    # Source code directory
│   └── navefileuploader/   # Main package directory
│       ├── __init__.py     # Package initialization
│       ├── masking.py      # Data masking functionality
│       └── sync.py         # JIRA sync functionality
├── tests/                  # Test files directory
│   ├── __init__.py
│   ├── test_masking.py
│   └── test_sync.py
├── examples/               # Example files
│   └── issue.json         # Sample JIRA data
├── docs/                   # Documentation
│   └── README.md          # Detailed documentation
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore file
├── requirements.txt       # Project dependencies
└── setup.py              # Package installation file
```

## 🧪 Running Tests

To run the test suite:

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Run tests
pytest

# Run tests with coverage
pytest --cov=navefileuploader
```

## 🛠 Development

1. Make sure you're in the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests before committing:
   ```bash
   pytest
   ```

## 📬 Questions?

If you need to customise fields or behaviour:
* For masking: Modify the `mask_data()` function in `src/navefileuploader/masking.py`
* For syncing: Adjust the configuration variables in `src/navefileuploader/sync.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.