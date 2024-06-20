import argparse
import os
import subprocess
from main import process


def list_all_files(directory, extension):
    """
    List all files with the given extension in a directory.

    :param directory: directory to list
    :param extension: file extension
    """
    res = []
    for root, dirs, files in os.walk(directory):
        files.sort()
        for file in files:
            # check that it is a file with the correct extension
            if len(file) >= 3 and file[-len(extension)::] == extension:
                res.append(os.path.join(root, file))
    res.sort()
    return res

def main(data_dir):
    res = list_all_files(data_dir, '.jpg')
    # for s in res:
        # print(s)
    print("RIRI")
    result = subprocess.Popen(['python3.10', 'main.py', '-M2', '-I0', '--image', res[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("RORO", result)
    print("Returned", process(res[0]))


# python3.10 benchmark.py --data /home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/ -I0
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the data folder")
    args = parser.parse_args()

    main(args.data)

