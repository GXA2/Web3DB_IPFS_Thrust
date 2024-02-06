import requests
import os
import json

def load_config(config_path='config.json'):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()
IPFS_URL = config["ipfs"]["url"] + config["ipfs"]["api_prefix"]

def download_file_from_ipfs(file_hash, output_path):
    url = f'{IPFS_URL}/cat?arg={file_hash}'
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return {"Success": True, "Message": "File downloaded successfully"}
        else:
            return {"Success": False, "Error": "Failed to download file", "StatusCode": response.status_code}
    except Exception as e:
        return {"Success": False, "Error": "An exception occurred", "Exception": str(e)}

if __name__ == '__main__':
    file_hash = 'QmYourFileHashHere'  # Replace with the actual file hash
    output_filename = 'downloaded_file.txt'  # Update as needed
    output_path = os.path.join(config["paths"]["download_directory"], output_filename)
    result = download_file_from_ipfs(file_hash, output_path)
    print(result)
