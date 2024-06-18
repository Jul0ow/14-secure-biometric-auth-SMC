#!/usr/bin/python3

from deepface import DeepFace
from mpyc.runtime import mpc
from mpyc.numpy import np
import face_recognition

secflt = mpc.SecFlt()

async def main():
    # Initialiser le runtime MPyC
    await mpc.start()

    # Récupération de l'image du runner local
    img_path = '/home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/Aaron_Eckhart/Aaron_Eckhart_0001.jpg' # input("Path of the image: ")
    # Extraction des vecteurs propres de l'image
    image = face_recognition.load_image_file(img_path)
    embedding = face_recognition.face_encodings(image)[0]
    # embedding = DeepFace.represent(img_path=img_path)[0]['embedding']
    # embedding = [secflt(x) for x in embedding]

    # Récupération de l'image de la seconde partie
    user, server = mpc.input(embedding)

    # user = np.array(user)
    # server = np.array(server)

    distance = user - server
    # distance = [user[i] - server[i] for i in range(len(user))]

    await mpc.output(distance)

    await mpc.shutdown()


mpc.run(main())

# /home/juloow/Documents/14-secure-biometric-auth-SMC/data/Aaron_Eckhart/Aaron_Eckhart_0001.jpg