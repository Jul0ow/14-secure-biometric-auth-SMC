import argparse
import subprocess

"""
    This script is a wrapper around demo_client_backend.py. It will run the demo_client_backend.py
    with MPyC parameters and the path to the image to be tested.
    
    If you want to start the demonstrator client run the following command:
        python3 demo_client.py --data /path/to/img.jpg
"""

# python3.10 demo_server.py --data serialized.pkl
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the image to be tested")
    args = parser.parse_args()

    subprocess.run(['python3.10', 'demo_client_backend.py', '--data', args.data, '-M2', '-I1'])
