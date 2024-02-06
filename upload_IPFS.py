import requests
import os
import json

def load_config(config_path='config.json'):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()
IPFS_URL = config["ipfs"]["url"] + config["ipfs"]["api_prefix"]

def upload_file_to_ipfs(filepath):
    url = f'{IPFS_URL}/add'
    try:
        if not os.path.exists(filepath):
            return {"Error": "File does not exist"}

        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f)}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                return {"Error": "Failed to upload file", "StatusCode": response.status_code}
    except Exception as e:
        return {"Error": "An exception occurred", "Exception": str(e)}

if __name__ == '__main__':
    filepath = os.path.join(config["paths"]["upload_directory"], 'your_file.txt')  # Update 'your_file.txt' as needed
    result = upload_file_to_ipfs(filepath)
    print(result)
