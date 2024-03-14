import requests
from pyeclib.ec_iface import ECDriver


file_hashes = ['QmWgU42LJNmMZCxhHwB3WnyTCm2jLjofTVqBCoCZnjDNsA', 'QmNXRBUiVGctUePnhHFg8fyHfkn2eHJW2TqGDAguoiaWBB']  # Replace with actual hashes

ipfs_nodes = ['http://ipfs-node1:5001', 'http://ipfs-node2:5001', 'http://ipfs-node3:5001', 'http://ipfs-node4:5001']  # Your IPFS node endpoints


def load_hashes_from_file(filename):
    """Load a list of IPFS hashes from a file."""
    with open(filename, 'r') as f:
        hashes = [line.strip() for line in f]
    return hashes

fragment_hashes = load_hashes_from_file('fragment_hashes.txt')


def retrieve_from_ipfs(hash, nodes):
    """Try to retrieve a file/fragment from IPFS using its hash."""
    for node in nodes:
        try:
            response = requests.post(f'{node}/api/v0/cat?arg={hash}')
            if response.status_code == 200:
                print(f'Successfully retrieved {hash} from {node}')
                return response.content
        except requests.ConnectionError:
            print(f'Node {node} is not reachable.')
    return None

def recover_files(file_hashes, nodes):
    """Recover files based on their IPFS hashes."""
    for hash in file_hashes:
        data = retrieve_from_ipfs(hash, nodes)
        if data:
            print(f'Successfully recovered file with hash: {hash}')
        else:
            print(f'Failed to recover file with hash: {hash}')

def recover_erasure_coded_file(fragment_hashes, nodes, k, m):
    """Recover an erasure-coded file from its fragments."""
    ec_driver = ECDriver(k=k, m=m, ec_type='liberasurecode_rs_vand')
    retrieved_fragments = []

    for hash in fragment_hashes:
        fragment = retrieve_from_ipfs(hash, nodes)
        if fragment:
            retrieved_fragments.append(fragment)
            if len(retrieved_fragments) >= k:
                try:
                    # Attempt to reconstruct the original data
                    original_data = ec_driver.decode(retrieved_fragments)
                    print('Successfully reconstructed the original file.')
                    # Save or process your original_data here
                    break
                except Exception as e:
                    print(f'Error reconstructing data: {e}')
    
    if len(retrieved_fragments) < k:
        print('Insufficient fragments retrieved to reconstruct the original file.')

recover_files(file_hashes, ipfs_nodes)
recover_erasure_coded_file(fragment_hashes, ipfs_nodes, k=10, m=5)
