import face_recognition
import argparse
import os
import pickle
import random

"""
    This script serializes face recognition models into a pickle file. The script use **face_recognition** library to 
    extract face encodings from an image.
    The serialized format is [[face_encodings, image_path],...]
    The limit parameter limits the maximum number of face encodings to be serialized.
    ex usage:
    python3 serializing.py  --data /dir/to/data/ --dest serialized_150.pkl --limit 150
"""

def list_all_files(directory, extension, shuffle):
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
    if shuffle:
        random.shuffle(res)
    else:
        res.sort()
    return res


def convert_to_prod_face_encodings(imgs, limit):
    face_encodings = []
    print("Encoding faces...")
    total = limit
    nb_proceed = 0
    for img in imgs:
        nb_proceed += 1
        image = face_recognition.load_image_file(img)
        try:
            print(f"Production encoding face {nb_proceed}/{total}")
            face_encodings.append([face_recognition.face_encodings(image)[0]])
        except:
            print("Couldn't find face encodings for {}".format(img))
        if nb_proceed >= limit:
            break

    return face_encodings


def convert_to_face_encodings(imgs, limit):
    face_encodings = []
    print("Encoding faces...")
    total = limit
    nb_proceed = 0
    for img in imgs:
        nb_proceed += 1
        image = face_recognition.load_image_file(img)
        try:
            print(f"Encoding face {nb_proceed}/{total}")
            face_encodings.append([face_recognition.face_encodings(image)[0], img])
        except:
            print("Couldn't find face encodings for {}".format(img))
        if nb_proceed >= limit:
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
    parser.add_argument("--limit", type=int, required=False, help="set the maximum number of images to serialize")
    parser.add_argument("--prod", action="store_true", help="set the dataset to the prod format, production format does not link face encodings to people's names")
    parser.add_argument("--no-shuffle", action="store_true", help="If present the script will take all the image in --data in alphabetical order (default is random)")
    args = parser.parse_args()

    shuffle = True
    if args.no_shuffle:
        shuffle = False

    imgs = list_all_files(args.data, ".jpg", shuffle)
    print("Found " + str(len(imgs)) + " images to serialise")

    if args.limit is None:
        limit = len(imgs)
    else:
        if args.limit < len(imgs):
            limit = args.limit
        else:
            limit = len(imgs)
    if args.prod:
        data = convert_to_prod_face_encodings(imgs, limit)
    else:
        data = convert_to_face_encodings(imgs, limit)

    print(f"Converted {len(data)} images to face encodings, {(len(data) * 100)/limit:.2f}% converting rate")

    serialisation(data, args.dest)
