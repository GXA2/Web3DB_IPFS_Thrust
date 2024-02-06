import pyeclib

# Data to encode
data = b"Hello, PyECLib!"

def test_ec_schemes(data):
    # List of available EC schemes in PyECLib
    ec_schemes = [
        "flat_xor_hd_3",
        "flat_xor_hd_4",
        "isa_l_rs_vand",
        "isa_l_rs_cauchy",
        "shss",
        "liberasurecode_rs_vand",
        "liberasurecode_rs_cauchy"
    ]

    for scheme in ec_schemes:
        try:
            # Initialize the EC object
            ec_obj = pyeclib.ec_iface.ECBackend(
                ec_type=scheme,
                k=10,  # Number of data fragments
                m=5,   # Number of coding fragments
                hd=3   # Hamming distance (only for flat XOR schemes)
            )

            # Encode data
            encoded_fragments = ec_obj.encode(data)

            # Decode data
            decoded_data = ec_obj.decode(encoded_fragments)

            # Verify the decoded data matches the original
            assert data == decoded_data, "Decoded data does not match the original"
            
            print(f"Successfully tested {scheme} scheme. Data integrity verified.")

        except Exception as e:
            print(f"Failed to test {scheme} scheme. Error: {str(e)}")

if __name__ == "__main__":
    test_ec_schemes(data)
