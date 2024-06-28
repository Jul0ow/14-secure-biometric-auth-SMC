import argparse
import pickle
import time
import numpy as np
from face_recognition import face_distance
from pathlib import Path

"""
    The purpose of this script is to test the authentification of face without SMC.
    This script will try all the combinaison of images in `--data` and will try determine if it is the same face using
    euclidean distance.
    ex usage:
        python3.10 without_smc_benchmark.py --data serialized.pkl
"""


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



def print_stat_bar(passed, total, passed_color, total_color):
    reset_color = "\033[0m"
    pourcentage_passed = int(passed * 100 / total)
    bar = "[" + passed_color + "=" * pourcentage_passed + total_color + "-" * (
            100 - pourcentage_passed) + reset_color + "] {}%".format(pourcentage_passed)
    print(bar)


def printing_stat(success, fail, total):
    # print pourcentage of success
    print("Percentage of success: {}/{}".format(success, success + fail))
    print_stat_bar(success, success + fail, Colors.GREEN, Colors.RED)
    # print pourcentage of completion
    print("Percentage of completion: {}/{}".format(success + fail, total))
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

def euclidean_distance(person1, person2):
    distance = np.subtract(person1, person2)
    # print('Multiply')
    euclidian = np.multiply(distance, distance)
    # print('Sum')
    euclidian = np.sum(euclidian)
    # print('Sqrt')
    euclidian = np.sqrt(euclidian)
    # print('Result', euclidian)
    return euclidian

def process_benchmark_reference(face_encodings):
    """
    :param face_encodings: the list of face encodings with the format:
    [[encoding_image_1, path_image1], [encoding_image2, path_image2], ...]
    """

    # This is the parent process

    nb_success = 0
    nb_fail = 0
    total = len(face_encodings) ** 2
    nb_processed = 0

    for reference in face_encodings:
        for tested in face_encodings:
            nb_processed += 1
            # clear_terminal()
            print("Testing image {} with image {}".format(reference[1], tested[1]))
            expected = is_same_person(reference[1], tested[1])
            result = euclidean_distance(tested[0], reference[0])

            if expected != (result <= threshold):
                print("Failed, expected {} but got {}".format(expected, result))
                nb_fail += 1
            else:
                print("Passed, got {}".format(result))
                nb_success += 1
            printing_stat(nb_success, nb_fail, total)

    print("Threshold used is {}".format(threshold))


# python3.10 without_smc_benchmark.py --data serialized.pkl
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the file containing the face encodings")
    parser.add_argument("--threshold_value", type=float, required=False,
                        help="threshold used to determine if face are the same, "
                             "the default value is 0.4")
    args = parser.parse_args()

    """
    Data must have been serializing with the with the format:
    [[encoding_image_1, path_image1], [encoding_image2, path_image2], ...]
    """

    start_time = time.time()

    with open(args.data, 'rb') as file:
        loaded_data_face_recognition = pickle.load(file)
    print(f"Load data face recognition, {len(loaded_data_face_recognition)} images loaded")

    threshold = 0.575
    if args.threshold_value is not None:
        threshold = args.threshold_value

    process_benchmark_reference(loaded_data_face_recognition)

    print(f"Process benchmark reference took {time.time() - start_time} seconds")