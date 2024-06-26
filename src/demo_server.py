import argparse
import os
import pickle
import subprocess
from pathlib import Path
import platform

from mpyc.runtime import mpc
from main import compute, compute_from_face_encoding

"""
"""

# python3.10 demo_server_backend.py --data serialized.pkl
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