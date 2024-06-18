from deepface import DeepFace

aaron_peirsol = [
    "data/Aaron_Peirsol/Aaron_Peirsol_0001.jpg",
    "data/Aaron_Peirsol/Aaron_Peirsol_0002.jpg",
    "data/Aaron_Peirsol/Aaron_Peirsol_0003.jpg",
    "data/Aaron_Peirsol/Aaron_Peirsol_0004.jpg",
    ]

aaron_sorkin = [
    "data/Aaron_Sorkin/Aaron_Sorkin_0001.jpg",
    "data/Aaron_Sorkin/Aaron_Sorkin_0002.jpg",
    "data/Aaron_Sorkin/Aaron_Sorkin_0003.jpg",
    "data/Aaron_Sorkin/Aaron_Sorkin_0004.jpg",
    ]

print('Is Sorking Sorking ?', DeepFace.verify(img1_path=aaron_peirsol[0], img2_path=aaron_peirsol[1])['verified'])
print('Is Sorking Peirsol ?', DeepFace.verify(img1_path=aaron_sorkin[0], img2_path=aaron_peirsol[1])['verified'])