import argparse
import face_recognition

from mpyc.runtime import mpc

from demo_server_backend import get_dataset_length
from main import compute_from_face_encoding

"""
    This script is the backend of the demonstrator client.
    it makes no sense to be launch manually.
    
    If you want to start the demonstrator client run the following command:
        python3 demo_client.py --data /path/to/img.jpg
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


def printing_stat(completed, total):
    # print pourcentage of completion
    print("Percentage of completion: {}/{}".format(completed, total))
    print_stat_bar(completed, total, Colors.RESET, Colors.RED)



async def test_img(img_path, threshold):
    """
    Lunch an MPC calculus to test if the `img_path` represents a person presents in the server's database.
    Uses the threshold to determine it.

    :param img_path: the path of the image
    :param threshold: the threshold use to determine if the face is in the database
    """

    # This is the parent process
    await mpc.start()

    nb_test = get_dataset_length("../data/serialized_150.pkl")
    image = face_recognition.load_image_file(img_path)

    try:
        embedding = face_recognition.face_encodings(image)[0]
    except:
        print(Colors.RED + "Cannot found face in image, recognition FAILED!" + Colors.RESET)
        return -1

    # Need to do an MPC for at worst each image in the database
    for i in range(nb_test):
        result = await compute_from_face_encoding(embedding)

        if result <= threshold:
            print(Colors.GREEN + "Face recognized, Verification successful!" + Colors.RESET)
            await mpc.shutdown()
            return
        printing_stat(i, nb_test)

    await mpc.shutdown()
    print(Colors.RED + "Face not recognized." + Colors.RESET)


# python3.10 demo_client.py --data /home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/Najib_al-Salhi/Najib_al-Salhi_0001.jpg -M2 -I0
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the image to be tested")
    args = parser.parse_args()

    default_threshold = 0.4
    mpc.run(test_img(args.data, default_threshold))
