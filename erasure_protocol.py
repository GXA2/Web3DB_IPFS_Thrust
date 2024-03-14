import requests
import json
import random
from pyeclib.ec_iface import ECDriver

# Erasure coding setup
k = 10
m = 5
ec_type = "liberasurecode_rs_vand"
ec_driver = ECDriver(k=k, m=m, ec_type=ec_type)

# Encode your data
data = b"Your data here"
fragments = ec_driver.encode(data)

# IPFS node API endpoints
node_endpoints = [
    'http://ipfs-node1:5001/api/v0/add', 
    'http://ipfs-node2:5001/api/v0/add',
    'http://ipfs-node3:5001/api/v0/add',
]

# Shuffle fragments to distribute them randomly
random.shuffle(fragments)

# Distribute fragments across nodes
for endpoint in node_endpoints:
    fragment = fragments.pop()  # Get a fragment to upload
    files = {'file': ('fragment', fragment, 'application/octet-stream')}
    response = requests.post(endpoint, files=files)
    
    if response.status_code == 200:
        print(f"Fragment added successfully to {endpoint}")
        print("Response:", response.json())
    else:
        print(f"Failed to add fragment to {endpoint}")
        print("Response code:", response.status_code)
