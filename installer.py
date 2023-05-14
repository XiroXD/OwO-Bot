import json
import sys
import os


print("Installing requirements")
os.system("pip install -r requirements.txt")

token = input("Enter your discord token: ")

if token is None or token == "":
    print("Invalid token")
    sys.exit(1)

print("Creating config files")
files = {
    "config/config.json": {
        "prefix": ".",
        "token": f"{token}",
        "deletetimer": 12,
        "owofied": False,
    },
    "config/notifications/toasts.json": {"dmlogger": True},
    "config/notifications/webhooks.json": {"title": "OwO Bot", "color": "#ff00d0", "dmlogger": ""},
}


for file_path, contents in files.items():
    try:
        file_directory, file_name = os.path.split(file_path)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        file_path = os.path.join(file_directory, file_name)

        with open(file_path, "w") as f:
            json.dump(contents, f, indent=4)
        print(f"Created file '{file_path}'")
    except Exception as e:
        print(f"Failed to create file '{file_path}': {e}")
