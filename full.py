import cv2
import math
import numpy as np
import mediapipe as mp
from Age_Gender import Age_gender
from Feature_extraction import features
import joblib
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

f_dict={'a':4.0,'b':5.1,'c':5.942,'d':6.065,'e':6.21,'f':6.21,'g':6.21,'h':6.23,'i':6.23,'j':6.4}
m_dict={'a':4.0,'b':5.1,'c':6.02,'d':6.2,'e':6.4,'f':6.4,'g':6.4,'h':6.57,'i':6.57,'j':6.31}

age_dict={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9}

weight_predictor=joblib.load('Weight_predictor.joblib')

def dist(a1,a2):
    return math.sqrt(((a2[0]-a1[0])**2)+((a2[1]-a1[1])**2))

def altitude(a1,a2,a3):
    a=dist(a1,a2)
    b=dist(a2,a3)
    c=dist(a3,a1)
    s=(a+b+c)/2
    area=math.sqrt(s*(s-a)*(s-b)*(s-c))
    return (2*area)/b

cap = cv2.VideoCapture('d:/FY/FullPerson.mp4')
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    show=cv2.resize(image,(1200,750))

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    h,w,c=image.shape

    height_measurements=0
    height_counter=0
    if results.pose_landmarks!=None and results.face_landmarks!=None:
        key2 = []
        for data_point in results.face_landmarks.landmark:
            key2.append({
                         'X': data_point.x,
                         'Y': data_point.y,})

        Leye=[int(key2[145]['X']*w),int(key2[145]['Y']*h)]
        Reye=[int(key2[374]['X']*w),int(key2[374]['Y']*h)]

        Cheek_Bone_R=(int(key2[34]['X']*w),int(key2[34]['Y']*h))
        Cheek_Bone_L=(int(key2[264]['X']*w),int(key2[264]['Y']*h))

        Chin=(int(key2[152]['X']*w),int(key2[152]['Y']*h))

        Fore_head=(int(key2[10]['X']*w),int(key2[10]['Y']*h))
        Top_fore_head=(Fore_head[0],Fore_head[1]-20)

        Face_height=dist(Top_fore_head,Chin)
        Cheek_Bone_Width=dist(Cheek_Bone_L,Cheek_Bone_R)

        pad_x=round(Cheek_Bone_Width/8)
        pad_y=round(Face_height/8)

        Face_roi=image[Top_fore_head[1]-round(pad_y/4):Chin[1],Cheek_Bone_R[0]:Cheek_Bone_L[0]]

        A_G=Age_gender(Face_roi)
        sex=A_G[0]
        age=A_G[1]
        if age>0 and age<7:
            k='a'
        elif age>=7 and age<13:
            k='b'
        elif age>=13 and age<17:
            k='c'
        elif age>=17 and age<24:
            k='d'
        elif age>=24 and age<30:
            k='e'
        elif age>=30 and age<35:
            k='f'
        elif age>=35 and age<43:
            k='g'
        elif age>=43 and age<54:
            k='h'
        elif age>=54 and age<63:
            k='i'
        else:
            k='j'
        if sex=='Male':
            gender=1
            constant_known=m_dict[k]
        else:
            gender=0
            constant_known=f_dict[k]
        age=age_dict[k]
        print(A_G)

        constant_ref=dist(Leye,Reye)
        pixels_per_metric=constant_ref/constant_known

        key1 = []
        for data_point in results.pose_landmarks.landmark:
            key1.append({
                         'X': data_point.x,
                         'Y': data_point.y,})
        Rshoulder=[int(key1[12]['X']*w),int(key1[12]['Y']*h)]
        Lshoulder=[int(key1[11]['X']*w),int(key1[11]['Y']*h)]

        Rhip=[int(key1[24]['X']*w),int(key1[24]['Y']*h)]
        Lhip=[int(key1[23]['X']*w),int(key1[23]['Y']*h)]

        Rknee=[int(key1[26]['X']*w),int(key1[26]['Y']*h)]
        Lknee=[int(key1[25]['X']*w),int(key1[25]['Y']*h)]

        Rheel=[int(key1[30]['X']*w),int(key1[30]['Y']*h)]
        Lheel=[int(key1[29]['X']*w),int(key1[29]['Y']*h)]

        a=dist(Rshoulder,Rhip)+dist(Rhip,Rknee)+dist(Rknee,Rheel)
        b=dist(Lshoulder,Lhip)+dist(Lhip,Lknee)+dist(Lknee,Lheel)
        body_lower=(a+b)/2

        full_lenght=body_lower+altitude(Top_fore_head,Rshoulder,Lshoulder)
        height_measurements+=full_lenght/pixels_per_metric
        height_counter+=1

        #cv2.circle(image,Top_fore_head,10,(255,0,255),cv2.FILLED)

        height=height_measurements/height_counter
        f1,f2,f3,f4,f5,f6,f7=features(key2,h,w,constant_known)
        x=np.array([height,f1,f2,f3,f4,f5,f6,f7,age,gender])

        weight=weight_predictor.predict([x])
        #print("height",height)
        #print("weight",weight[0])
        Fore_head[0],Fore_head[1]-20
        cv2.putText(show,str(height),(500,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2,cv2.LINE_AA)
        cv2.putText(show,str(weight),(500,150),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2,cv2.LINE_AA)

    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())


    cv2.imshow('Result',show)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
cv2.destroyAllWindows()
