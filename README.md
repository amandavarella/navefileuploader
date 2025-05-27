# NaveClean - JIRA Data Masking Tool

## 📝 Description

This project provides two helper functions to mask sensitive data from JIRA before sending it to Nave:

1. A local file masking function that processes Jira JSON files for manual upload through Nave's interface
2. An automated processor that fetches data from JIRA, masks it, and uploads it directly through Nave's API

## 🔧 What It Does

* Replaces all email addresses with fake ones
* Masks all URLs (http/https) with randomised placeholders
* Anonymises names in `"displayName"`
* Replaces content of fields like `"goal"`, `"body"`, `"summary"`, and `"description"` with randomised text
* Randomises `"fromString"` and `"toString"` for specific fields like `"assignee"`, `"Contributors"`, `"summary"`, and `"Attachment"`

## ⚙️ Environment Configuration

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
   NAVE_API_URL=your_nave_url
   NAVE_API_KEY=your_api_key
   NAVE_DASHBOARD_ID=your_dashboard_id
   ```

**Note:**
- Never commit your `.env` file to version control.
- Only share `.env.example` with placeholder values.

## ▶️ Usage Modes

### Mode 1: Local File Masking

Use this mode when you have a Jira JSON file that you want to mask and upload manually through Nave's interface.

#### Getting Your Jira JSON File

To export issues with changelogs from Jira Cloud using their REST API, use the following format:

```
https://<your-domain>.atlassian.net/rest/agile/1.0/board/<BOARD_ID>/issue?expand=changelog&startAt=0&maxResults=1000
```

* Replace `<your-domain>` with your company's Jira subdomain.
* Replace `<BOARD_ID>` with the numeric ID of the Jira board.

For detailed information about the Jira JSON file format and how to properly extract data from JIRA, please refer to the [Nave documentation](https://getnave.com/blog/loading-data-to-nave/).

##### How to Find the Board ID

1. Open your Jira board in a browser.
2. Look at the URL — it should look something like this:
   ```
   https://company.atlassian.net/secure/RapidBoard.jspa?rapidView=18
   ```
3. The number after `rapidView=` is your **Board ID**.

##### Save the file

Save your Jira JSON input file as `issue.json` in the same folder as the script.

#### Executing the file

1. **Install Python 3** if you haven't already:
   ```bash
   python3 --version
   ```

2. **Run the script** from the terminal:
   ```bash
   python3 naveclean.py
   ```

3. **Upload the output** file named `masked_issue.json` through Nave's interface.

### Mode 2: Automated JIRA to Nave Processing

This mode automatically fetches data from JIRA, masks it, and sends it directly to Nave through their API.

1. **Install required dependencies**:
   ```bash
   pip install requests
   ```

2. **Configure the script**:
   - Open `jira_processor.py`
   - Update the configuration variables at the top:
     - `JIRA_URL`: Your JIRA board URL
     - `JIRA_USERNAME`: Your JIRA email
     - `JIRA_API_TOKEN`: Your JIRA API token
     - `TARGET_API_URL`: Nave's API endpoint (https://file.getnave.com/api/dashboards/update)
     - `TARGET_API_KEY`: Your Nave API key
     - `DASHBOARD_ID`: Your Nave dashboard ID

3. **Run the processor**:
   ```bash
   python3 jira_processor.py
   ```

4. **Set up automation** (optional):
   To run the script daily, add it to your crontab:
   ```bash
   crontab -e
   ```
   Add this line to run it daily at 1 AM:
   ```
   0 1 * * * /path/to/python3 /path/to/jira_processor.py
   ```

## 📂 File Structure

```
├── naveclean.py          # Core masking functionality
├── jira_processor.py     # Full JIRA to Nave integration script
├── issue.json           # Example Jira JSON input file (for Mode 1)
└── masked_issue.json    # Example output file (for Mode 1)
```

## 🛠 Requirements

* Python 3.6+
* `requests` library (for Mode 2)

## 📬 Questions?

If you need to customise fields or behaviour:
* For Mode 1: Modify the `mask_data()` function in `naveclean.py`
* For Mode 2: Adjust the configuration variables in `jira_processor.py`
