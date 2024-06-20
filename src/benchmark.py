import argparse
import asyncio
import os
import subprocess
import time
from pathlib import Path

from mpyc.runtime import mpc
from main import compute


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

async def test_images(image1, image2, threshold):
    """

    Test whether two images represent the same person using MPyC.

    :param image1: the path of the first image
    :param image2: the path of the second image
    :return: True if images represent the same person. False otherwise.
    """

    subprocess.Popen(['python3.10', 'main.py', '-M2', '-I0', '--image', image1], stderr=subprocess.PIPE)
    result = await compute(image2)

    return result <= threshold


async def process_benchmark(res):


    # This is the parent process

    for image1 in res:
        for image2 in res:
            print("Testing image {} with image {}".format(image1, image2))
            expected = is_same_person(image1, image2)
            # result = await test_images(image1, image2, threshold)
            await mpc.start()
            result = await compute(image2)
            await mpc.shutdown()
            if expected and result <= threshold:
                print("Failed, expected {} but got {}".format(expected, result))
            else:
                print("Passed")


    """
    if pid != 0:
        await mpc.shutdown()
    """

# python3.10 benchmark.py --data /home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/ -M2 -I1
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the data folder")
    args = parser.parse_args()

    res = list_all_files(args.data, '.jpg')
    threshold = 0.4

    pid = os.fork()

    if pid == 0:
        # This is the child process
        for image_child1 in res:
            for image_child2 in res:
                subprocess.run(['python3.10', 'main.py', '-M2', '-I0', '--image', image_child2], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    else:
        mpc.run(process_benchmark(res))
