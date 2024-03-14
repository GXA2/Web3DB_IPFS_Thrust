import requests

# IPFS node URL
IPFS_URL = 'http://ipfs-node1:5001'

def upload_file(filepath):
    """Upload a file to IPFS using the HTTP API and return the hash of the file."""
    files = {'file': open(filepath, 'rb')}
    response = requests.post(f'{IPFS_URL}/api/v0/add', files=files)
    response_json = response.json()
    return response_json['Hash']

def retrieve_file(file_hash, output_file):
    """Retrieve a file from IPFS using its hash and the HTTP API."""
    response = requests.get(f'{IPFS_URL}/api/v0/cat?arg={file_hash}', stream=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

if __name__ == "__main__":
    file_to_upload = 'example.txt'
    output_file = 'retrieved_example.txt'

    # Ensure 'example.txt' exists with content to upload
    with open(file_to_upload, 'w') as f:
        f.write("Hello, IPFS via HTTP API!")

    file_hash = upload_file(file_to_upload)
    print(f"Uploaded {file_to_upload} to IPFS with hash: {file_hash}")

    retrieve_file(file_hash, output_file)
    print(f"Retrieved file from IPFS and saved as: {output_file}")
