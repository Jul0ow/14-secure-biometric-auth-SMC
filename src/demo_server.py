import argparse
import subprocess

"""
    This script is a wrapper around the backend of the demonstrator server.
    It will launch the backend with the correct MPyC parameters and the given path of the database file
    
    The dataset must be a pickle file that have generated with the serializing.py script.
    
    If you want to start the demonstrator server run the following command:
        python3 demo_server.py --data /path/to/dataset.pkl
"""

# python3.10 demo_server.py --data serialized.pkl
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the file containing the face encodings")
    args = parser.parse_args()

    """
    Data must have been serializing with the with the format:
    [[encoding_image_1, path_image1], [encoding_image2, path_image2], ...]
    """

    while True:
        subprocess.run(['python3.10', 'demo_server_backend.py', '--data', args.data, '-M2', '-I0'])