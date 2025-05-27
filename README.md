# NaveFileUploader

A Python package for masking and syncing JIRA data to Nave.

## 📝 Description

This project provides two main functionalities to mask sensitive data from JIRA before sending it to Nave:

1. A local file masking function that processes Jira JSON files for manual upload through Nave's interface
2. An automated processor that fetches data from JIRA, masks it, and uploads it directly through Nave's API

## 🔧 What It Does

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

After installation, you can use the command-line tools:

```bash
# Mask a JIRA JSON file
nave-mask input.json output.json

# Sync JIRA data to Nave
nave-sync
```

Or use the Python API:

```python
from navefileuploader import mask_json_file, JiraProcessor

# To mask a file
mask_json_file("input.json", "output.json")

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