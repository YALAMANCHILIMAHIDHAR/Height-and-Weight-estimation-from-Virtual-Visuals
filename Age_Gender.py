import cv2
import numpy as np

ageProto = "./age.prototxt"
ageModel = "./dex_chalearn_iccv2015.caffemodel"

genderProto = "./gender.prototxt"
genderModel = "./gender.caffemodel"

age_model=cv2.dnn.readNetFromCaffe(ageProto,ageModel)
gender_model=cv2.dnn.readNetFromCaffe(genderProto,genderModel)

def Age_gender(img):
    l=[]
    image=cv2.resize(img,(224,224))
    face_blob=cv2.dnn.blobFromImage(image)
    age_model.setInput(face_blob)
    age_result=age_model.forward()

    gender_model.setInput(face_blob)
    gender_result=gender_model.forward()

    if np.argmax(gender_result[0])==0:
        l.append("Female")
    else:
        l.append("Male")
    indexes=np.array([i for i in range(0,101)])
    l.append(round(np.sum(age_result[0]*indexes)))
    return l
