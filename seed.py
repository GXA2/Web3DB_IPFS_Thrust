import os
import random
import requests
from pyeclib.ec_iface import ECDriver

# IPFS API endpoints for nodes
ipfs_nodes = ['http://ipfs-node1:5001', 'http://ipfs-node2:5001', 'http://ipfs-node3:5001', 'http://ipfs-node4:5001']  # Adjust based on your setup

fragment_hashes = [] 

def generate_random_data(size_in_bytes):
    return os.urandom(size_in_bytes)

def add_to_ipfs(node_url, data):
    files = {'file': data}
    response = requests.post(f'{node_url}/api/v0/add', files=files)
    return response.json()['Hash']

def distribute_files(file_sizes):
    for size in file_sizes:
        data = generate_random_data(size)
        node_url = random.choice(ipfs_nodes)  # Randomly select a node
        file_hash = add_to_ipfs(node_url, data)
        print(f'Added file of size {size} bytes to {node_url}, hash: {file_hash}')

def distribute_files_with_erasure_coding(file_size, k, m):
    global fragment_hashes
    ec_driver = ECDriver(k=k, m=m, ec_type='liberasurecode_rs_vand')
    data = generate_random_data(file_size)
    fragments = ec_driver.encode(data)

    for fragment in fragments:
        node_url = random.choice(ipfs_nodes)  # Randomly select a node for each fragment
        fragment_hash = add_to_ipfs(node_url, fragment)
        print(f'Added fragment to {node_url}, hash: {fragment_hash}')
        fragment_hashes += [fragment_hash]

def save_hashes_to_file(hashes, filename):
    """Save a list of IPFS hashes to a file."""
    with open(filename, 'w') as f:
        for hash_ in hashes:
            f.write(hash_ + '\n')




file_sizes = [1024 * 1024 * 10, 1024 * 1024 * 20]  # 10MB, 20MB
distribute_files(file_sizes)

# Distribute a 50MB file with k=5, m=3
distribute_files_with_erasure_coding(1024 * 1024 * 100, 10, 5)

save_hashes_to_file(fragment_hashes, 'fragment_hashes.txt')
