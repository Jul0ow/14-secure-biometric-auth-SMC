#!/usr/bin/python3

from deepface import DeepFace
import face_recognition

def main():

    # Récupération de l'image du runner local
    img_path = '/home/matthieu/srs/crypto/14-secure-biometric-auth-SMC/data/Aaron_Eckhart/Aaron_Eckhart_0001.jpg' # input("Path of the image: ")
    # Extraction des vecteurs propres de l'image
    embedding_deepFace = DeepFace.represent(img_path=img_path)[0]['embedding']
    image = face_recognition.load_image_file(img_path)
    toto = face_recognition.face_encodings(image)[0]
    print(len(embedding_deepFace))
    print(len(toto))
    print(toto)


if __name__ == '__main__':
    main()
