#!/usr/bin/python3

from mpyc.runtime import mpc
from mpyc.numpy import np
import face_recognition
import argparse

secflt = mpc.SecFlt()
secfpx = mpc.SecFxp(32)

async def compute(img_path):
    # Récupération de l'image du runner local
    # img_path = '/home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/Aaron_Peirsol/Aaron_Peirsol_0003.jpg' # input("Path of the image: ")
    # Extraction des vecteurs propres de l'image
    image = face_recognition.load_image_file(img_path)
    embedding = face_recognition.face_encodings(image)[0]
    # embedding = DeepFace.represent(img_path=img_path)[0]['embedding']
    embedding =  secfpx.array(embedding)

    # Récupération de l'image de la seconde partie
    user, server = mpc.input(embedding)

    print('Computing the distance')
    distance = np.subtract(user, server)
    print('Computing the euclidian distance')
    print('Multiply')
    euclidian = np.multiply(distance, distance)
    print('Sum')
    euclidian = np.sum(euclidian)

    print('Printing the result')
    euclidian = await mpc.output(euclidian)
    # print('Sqrt')
    euclidian = np.sqrt(euclidian)
    print('Result', euclidian)
    return euclidian

async def main(img_path):
    # Initialiser le runtime MPyC
    await mpc.start()

    euclidian = await compute(img_path)

    await mpc.shutdown()
    return euclidian


def process(image):
    return mpc.run(main(image))


# python3.10 main.py --image "/home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/Aaron_Peirsol/Aaron_Peirsol_0001.jpg" -M2 -I1
if __name__ == "__main__":
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True, help="path to the image to be load")
    args = parser.parse_args()

    process(args.image)