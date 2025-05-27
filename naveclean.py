# Version: 1.1.2

import json
import re
import random
import string

# Regex patterns
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
HTTP_URL_REGEX = re.compile(r"https?://[\w./\-]+")

REPLACEMENT_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Sam", "Jamie", "Riley", "Quinn", "Avery"]

RANDOM_SUMMARY_WORDS = ["Improve", "Refactor", "Fix", "Update", "Add", "Remove", "Test", "Clean", "Document", "Review"]

def random_email():
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    domain = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"{name}@{domain}.com"

def random_url():
    path = '/'.join(random.choices(string.ascii_lowercase, k=5))
    return f"https://{random_string(10)}.com/{path}"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def random_display_name():
    return random.choice(REPLACEMENT_NAMES)

def random_text():
    return ' '.join(random.choices(RANDOM_SUMMARY_WORDS, k=3))

def mask_value(value, key_hint=None):
    if isinstance(value, str):
        if key_hint == "displayName":
            return random_display_name()
        if key_hint in ["goal", "body", "summary", "description"]:
            return random_text()
        value = EMAIL_REGEX.sub(lambda m: random_email(), value)
        value = HTTP_URL_REGEX.sub(lambda m: random_url(), value)
    return value

def mask_data(obj, key_hint=None):
    if isinstance(obj, dict):
        if obj.get("field") == "description":
            siblings = {k: obj.get(k) for k in ["fromString", "to", "toString"]}
            if all(v is None for v in siblings.values()):
                obj = {**obj, "fromString": None, "to": None, "toString": None}
            else:
                obj = {**obj, "fromString": "text" if siblings.get("fromString") else None,
                              "to": "text" if siblings.get("to") else None,
                              "toString": "text" if siblings.get("toString") else None}
        elif obj.get("field") in ["assignee", "Contributors"]:
            obj["fromString"] = random_display_name() if obj.get("fromString") else None
            obj["toString"] = random_display_name() if obj.get("toString") else None
        elif obj.get("field") == "summary":
            obj["fromString"] = random_text() if obj.get("fromString") else None
            obj["toString"] = random_text() if obj.get("toString") else None
        elif obj.get("field") == "Attachment":
            obj["fromString"] = random_text() if obj.get("fromString") else None
            obj["toString"] = random_text() if obj.get("toString") else None
        return {k: mask_data(v, k) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [mask_data(item) for item in obj]
    elif isinstance(obj, str):
        return mask_value(obj, key_hint)
    else:
        return obj

def mask_json_file(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)
    masked = mask_data(data)
    with open(output_path, "w") as f:
        json.dump(masked, f, indent=2)
    print(f"Masked file saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    mask_json_file("issue.json", "masked_issue.json")
