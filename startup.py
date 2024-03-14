import docker
import io
import tarfile
import time

client = docker.from_env()

network_name = 'ipfs_network'
image_name = 'ipfs/kubo'
swarm_key_path = './swarm.key'  # Make sure this path is correct

# Ensure the Docker network exists
try:
    network = client.networks.get(network_name)
    print(f"Network '{network_name}' already exists.")
except docker.errors.NotFound:
    network = client.networks.create(network_name, driver="bridge")
    print(f"Network '{network_name}' created.")

def create_tar_bytes(source_file):
    """
    Create a tar archive in memory from the given source file.
    """
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        # Read the file in binary mode and add it to the tar
        with open(source_file, 'rb') as f:
            file_data = f.read()
        tar_info = tarfile.TarInfo(name='swarm.key')
        tar_info.size = len(file_data)
        tar_info.mtime = 0  # Set modification time to epoch
        tar.addfile(tar_info, io.BytesIO(file_data))
    tar_stream.seek(0)  # Reset the stream position
    return tar_stream.getvalue()  # Return the bytes of the tar archive

def copy_swarm_key_to_container(container, tar_bytes):
    """
    Copy the tar bytes to the specified path inside the container.
    """
    success = container.put_archive('/data/ipfs/', tar_bytes)
    if not success:
        raise Exception(f"Failed to copy swarm key to container {container.name}")
    print(f"Successfully copied swarm key to {container.name}")

def start_ipfs_node(node_name, swarm_key_bytes):
    """
    Start an IPFS node, connect it to the network, and configure it with a swarm key.
    """
    container = client.containers.run(image_name, detach=True, name=node_name, command="daemon --enable-pubsub-experiment", auto_remove=False, tty=True, stdin_open=True)
    print(f"Started IPFS node: {node_name}")
    network.connect(container)
    
    # Wait for a moment to ensure the container is ready
    time.sleep(2)
    
    copy_swarm_key_to_container(container, swarm_key_bytes)
    
# Prepare the tar bytes for the swarm key
swarm_key_bytes = create_tar_bytes(swarm_key_path)

# Start multiple IPFS nodes
node_names = ['ipfs-node1', 'ipfs-node2', 'ipfs-node3', 'ipfs-node4']  # Adjust names and quantity as needed

for name in node_names:
    start_ipfs_node(name, swarm_key_bytes)
    # Add a delay between starting each node to avoid race conditions
    time.sleep(4)

print("All IPFS nodes started and connected to the private network.")
