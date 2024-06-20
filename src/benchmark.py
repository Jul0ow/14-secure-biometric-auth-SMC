import argparse
import os
import subprocess
from pathlib import Path

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

def is_same_person(file1, file2):
    """

    Test if two files have the same person. Which means in our case that the two files belongs to the same directory

    :param file1: the first file representing the first person
    :param file2: the second file representing the second person
    """

    dossier1 = Path(file1).resolve().parent
    dossier2 = Path(file2).resolve().parent
    return dossier1 == dossier2

def test_images(image1, image2, threshold):
    """

    Test whether two images represent the same person using MPyC.

    :param image1: the path of the first image
    :param image2: the path of the second image
    :return: True if images represent the same person. False otherwise.
    """

    subprocess.Popen(['python3.10', 'main.py', '-M2', '-I0', '--image', image1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = process(image2)

    return result <= threshold



def main(data_dir):
    res = list_all_files(data_dir, '.jpg')
    # for s in res:
        # print(s)

    expected = is_same_person(res[0], res[1])
    result = test_images(res[0], res[1], 0.4)

    if expected != result:
        print("Failed")
    else:
        print("Passed")

# python3.10 benchmark.py --data /home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/ -I0
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the data folder")
    args = parser.parse_args()

    main(args.data)

