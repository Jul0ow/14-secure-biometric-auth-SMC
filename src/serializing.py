import face_recognition
import argparse
import os
import pickle

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


def convert_to_face_encodings(imgs):
    face_encodings = []
    print("Encoding faces...")
    total = len(imgs)
    nb_proceed = 0
    for img in imgs:
        nb_proceed += 1
        image = face_recognition.load_image_file(img)
        try:
            print(f"Encoding face {nb_proceed}/{total}")
            face_encodings.append([face_recognition.face_encodings(image)[0], img])
        except:
            print("Couldn't find face encodings for {}".format(img))
        if nb_proceed == 100:
            break

    return face_encodings

def serialisation(data, dest):
    with open(dest, 'wb') as file:
        print("Serialising data in " + dest)
        pickle.dump(data, file)

# python3 serializing.py  --data /home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/ --dest serialized.pkl
# it will take 25 minutes with the provided dataset of 13 233 images
if __name__ == "__main__":
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the data folder")
    parser.add_argument("--dest", type=str, required=True, help="path to the output file")
    args = parser.parse_args()

    imgs = list_all_files(args.data, ".jpg")
    print("Found " + str(len(imgs)) + " images to serialise")

    data = convert_to_face_encodings(imgs)

    serialisation(data, args.dest)
