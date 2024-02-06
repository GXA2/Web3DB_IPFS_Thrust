num_nodes = 20
services = ""

for i in range(1, num_nodes + 1):
    node_name = f"ipfs-node{i}"
    services += f"""
  {node_name}:
    image: ipfs/kubo
    volumes:
      - ./swarm.key:/data/ipfs/swarm.key
      - {node_name}-data:/data/ipfs
    environment:
      - LIBP2P_FORCE_PNET=1
    networks:
      - ipfs_network

volumes:"""

for i in range(1, num_nodes + 1):
    node_name = f"ipfs-node{i}"
    services += f"""
  {node_name}-data:"""

compose_template = f"""
version: '3.7'

services:{services}

networks:
  ipfs_network:
    driver: bridge
"""

with open("docker-compose.yml", "w") as f:
    f.write(compose_template)
