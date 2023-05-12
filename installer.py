import json
import os


print("Installing requirements")
os.system("pip install -r requirements.txt")


files = {
    "config/config.json": {"prefix": ".", "token": "", "deletetimer": 12, "owofied": False},
    "config/notifications/toasts.json": {"dmlogger": True},
    "config/notifications/webhooks.json": {"dmlogger": ""},
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
