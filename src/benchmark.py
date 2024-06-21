import argparse
import os
import subprocess
import time
from pathlib import Path
import platform

from mpyc.runtime import mpc
from main import compute


class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    # Couleurs de fond
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


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


def clear_terminal():
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def print_stat_bar(passed, total, passed_color, total_color):
    reset_color = "\033[0m"
    pourcentage_passed = int(passed * 100 / total)
    bar = "[" + passed_color + "=" * pourcentage_passed + total_color + "-" * (
                100 - pourcentage_passed) + reset_color + "] {}%".format(pourcentage_passed)
    print(bar)

def printing_stat(success, fail, total):
    # print pourcentage of success
    print("Pourcentage of success: {}/{}".format(success, success + fail))
    print_stat_bar(success, success + fail, Colors.GREEN, Colors.RED)
    # print pourcentage of completion
    print("Pourcentage of completion: {}/{}".format(success + fail, total))
    print_stat_bar(success + fail, total, Colors.RESET, Colors.RED)


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


async def process_benchmark_iterator(res):
    await mpc.start()

    for _ in range(len(res)):
        for tested in res:
            await compute(tested)

    await mpc.shutdown()


async def process_benchmark_reference(res):
    # This is the parent process
    await mpc.start()

    nb_success = 0
    nb_fail = 0
    total = len(res) ** 2

    for reference in res:
        for tested in res:
            # clear_terminal()
            print("Testing image {} with image {}".format(reference, tested))
            expected = is_same_person(reference, tested)
            # result = await test_images(image1, image2, threshold)
            result = await compute(reference)

            if result == -1:
                # print("Face not found")
                nb_fail += 1
            elif expected and result <= threshold:
                print("Failed, expected {} but got {}".format(expected, result))
                nb_fail += 1
            else:
                # print("Passed")
                nb_success += 1
            printing_stat(nb_success, nb_fail, total)
            # time.sleep(0.5)

    await mpc.shutdown()


# python3.10 benchmark.py --data /home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/ -M2 -I1
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the data folder")
    parser.add_argument("--iterator", action="store_true",
                        help="set if the program is an iterator that will provide all images")
    args = parser.parse_args()

    res = list_all_files(args.data, '.jpg')
    threshold = 0.4

    if args.iterator:
        mpc.run(process_benchmark_iterator(res))
    else:
        subprocess.Popen(['python3.10', 'benchmark.py', '--iterator', '--data', args.data, '-M2', '-I0'],
                         stderr=subprocess.PIPE)
        mpc.run(process_benchmark_reference(res))
