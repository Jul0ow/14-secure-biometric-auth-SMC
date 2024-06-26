import argparse
import subprocess

"""
"""

# python3.10 demo_server.py --data serialized.pkl
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the image to be tested")
    args = parser.parse_args()

    subprocess.run(['python3.10', 'demo_client_backend.py', '--data', args.data, '-M2', '-I1'])
