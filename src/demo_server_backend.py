import argparse
import os
import pickle

from mpyc.runtime import mpc
from main import compute_from_face_encoding

"""
    This script is the backend of the demonstrator server.
    it makes no sense to be launch manually.
    It will iterate over the given database to test if the image that will be given by demo_client_backend
    contains a face present in the database.
    
    If you want to start the demonstrator server run the following command:
        python3 demo_server.py --data /path/to/dataset.pkl
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


def get_dataset_length(dataset_path):
    with open(dataset_path, 'rb') as file:
        loaded_dataset = pickle.load(file)
    return len(loaded_dataset)
def print_stat_bar(passed, total, passed_color, total_color):
    reset_color = "\033[0m"
    pourcentage_passed = int(passed * 100 / total)
    bar = "[" + passed_color + "=" * pourcentage_passed + total_color + "-" * (
            100 - pourcentage_passed) + reset_color + "] {}%".format(pourcentage_passed)
    print(bar)


def printing_stat(nb_completed, total):
    # print pourcentage of completion
    print("Percentage of completion: {}/{}".format(nb_completed, total))
    print_stat_bar(nb_completed, total, Colors.RESET, Colors.RED)



async def process_server(face_encodings, threshold):
    """
    While true loop that wait for a client connection and do an MPC with the client to determine if the image send of
    the client is in the `face_encodings`.

    :param face_encodings: the list of face encodings with the format:
    [[encoding_image_1, path_image1], [encoding_image2, path_image2], ...]
    :param threshold: the threshold for the face encoding
    """

    total = len(face_encodings)
    nb_processed = 0

    await mpc.start()
    for tested in face_encodings:
        nb_processed += 1
        # clear_terminal()
        print("Testing image client image with image {}".format(tested[1]))
        result = await compute_from_face_encoding(tested[0])

        if result <= threshold:
            print("Face recognized successfully")
            break

        printing_stat(nb_processed, total)
    await mpc.shutdown()


# python3.10 demo_server_backend.py --data serialized.pkl -M2 -I1
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the file containing the face encodings")
    args = parser.parse_args()

    """
    Data must have been serializing with the with the format:
    [[encoding_image_1, path_image1], [encoding_image2, path_image2], ...]
    """

    with open(args.data, 'rb') as file:
        loaded_data_face_recognition = pickle.load(file)
    print(f"Load data face recognition, {len(loaded_data_face_recognition)} images loaded")

    default_threshold = 0.4

    mpc.run(process_server(loaded_data_face_recognition, default_threshold))
