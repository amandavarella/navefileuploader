# Masking Script README

## 📝 Description

This script (`masking_script.py`) loads a JSON file exported from Jira or a similar issue tracking tool and anonymises personally identifiable information (PII) and sensitive content. It maintains compatibility with the original structure.

## 🔧 What It Does

* Replaces all email addresses with fake ones
* Masks all URLs (http/https) with randomised placeholders
* Anonymises names in `"displayName"`
* Replaces content of fields like `"goal"`, `"body"`, `"summary"`, and `"description"` with randomised text
* Randomises `"fromString"` and `"toString"` for specific fields like `"assignee"`, `"Contributors"`, `"summary"`, and `"Attachment"`

## ▶️ How to Run

1. **Install Python 3** if you haven't already:

   ```bash
   python3 --version
   ```

2. **Save your JSON input file** as `sample.json` in the same folder as the script.

3. **Run the script** from the terminal:

   ```bash
   python3 masking_script.py
   ```

4. **Check the output** file named `masked_sample.json` in the same directory.

## 🌐 Jira JSON Export URL Format

To export issues with changelogs from Jira Cloud using their REST API, use the following format:

```
https://<your-domain>.atlassian.net/rest/agile/1.0/board/<BOARD_ID>/issue?expand=changelog&startAt=0&maxResults=1000
```

* Replace `<your-domain>` with your company’s Jira subdomain.
* Replace `<BOARD_ID>` with the numeric ID of the Jira board.

### 🔍 How to Find the Board ID

1. Open your Jira board in a browser.
2. Look at the URL — it should look something like this:

   ```
   https://company.atlassian.net/secure/RapidBoard.jspa?rapidView=18
   ```
3. The number after `rapidView=` is your **Board ID**.

### ✅ Example

```
https://company.atlassian.net/rest/agile/1.0/board/18/issue?expand=changelog&startAt=0&maxResults=1000
```

## 📂 File Structure

```
├── masking_script.py
├── sample.json           # Your input file
└── masked_sample.json    # Output file with masked data
```

## 🛠 Requirements

* Python 3.6+
* No external dependencies (uses standard library only)

## 📬 Questions?

If you need to customise fields or behaviour, just modify the `mask_data()` function inside the script.
