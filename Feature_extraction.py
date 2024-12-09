import math

def dist1(a1,a2):
    return math.sqrt(((a2[0]-a1[0])**2)+((a2[1]-a1[1])**2))


def features(key,h,w,const):
    Left_eye_C=(int(key[145]['X']*w),int(key[145]['Y']*h))
    Right_eye_C=(int(key[374]['X']*w),int(key[374]['Y']*h))

    eye_d=dist1(Left_eye_C,Right_eye_C)
    ppm=eye_d/const

    def dist(a1,a2):
        return (math.sqrt(((a2[0]-a1[0])**2)+((a2[1]-a1[1])**2)))/ppm
        
    def Area(a1,a2,a3):
        a=dist(a1,a2)
        b=dist(a2,a3)
        c=dist(a3,a1)
        s=(a+b+c)/2
        area=math.sqrt(s*(s-a)*(s-b)*(s-c))
        return area

    Cheek_Bone_R=(int(key[34]['X']*w),int(key[34]['Y']*h))
    Cheek_Bone_L=(int(key[264]['X']*w),int(key[264]['Y']*h))

    Jaw_Bone_R=(int(key[138]['X']*w),int(key[138]['Y']*h))
    Jaw_Bone_L=(int(key[367]['X']*w),int(key[367]['Y']*h))
    Cheek_Bone_width=dist(Cheek_Bone_R,Cheek_Bone_L)
    Jaw_Bone_width=dist(Jaw_Bone_R,Jaw_Bone_L)

    CJWR=(Cheek_Bone_width/Jaw_Bone_width)

    Upper_Facial_B=(int(key[15]['X']*w),int(key[15]['Y']*h))
    Upper_Facial_T=(int(key[8]['X']*w),int(key[8]['Y']*h))

    WHR=(Jaw_Bone_width/dist(Upper_Facial_T,Upper_Facial_B))

    Chin=(int(key[152]['X']*w),int(key[152]['Y']*h))
    Between_Eye_C=(int(key[6]['X']*w),int(key[6]['Y']*h))
    Lower_cheek_R=((int(key[150]['X']*w),int(key[150]['Y']*h)))
    Lower_cheek_L=((int(key[379]['X']*w),int(key[379]['Y']*h)))

    Par_P=dist(Cheek_Bone_L,Jaw_Bone_L)+dist(Jaw_Bone_L,Lower_cheek_L)+dist(Lower_cheek_L,Chin)+dist(Chin,Lower_cheek_R)+dist(Lower_cheek_R,Jaw_Bone_R)+dist(Jaw_Bone_R,Cheek_Bone_R)+Cheek_Bone_width
    Par_A=(Area(Cheek_Bone_L,Cheek_Bone_R,Jaw_Bone_L)+Area(Cheek_Bone_R,Jaw_Bone_R,Jaw_Bone_L)+Area(Jaw_Bone_L,Jaw_Bone_R,Chin)+Area(Jaw_Bone_L,Lower_cheek_L,Chin)+Area(Jaw_Bone_R,Lower_cheek_R,Chin))
    PAR=(Par_P/Par_A)

    Right_eye_R=(int(key[130]['X']*w),int(key[130]['Y']*h))
    Right_eye_L=(int(key[133]['X']*w),int(key[133]['Y']*h))
    Left_eye_R=(int(key[463]['X']*w),int(key[463]['Y']*h))
    Left_eye_L=(int(key[263]['X']*w),int(key[263]['Y']*h))

    ES=(dist(Right_eye_L,Right_eye_R)+dist(Left_eye_L,Left_eye_R))/2

    Fore_head=(int(key[10]['X']*w),int(key[10]['Y']*h))
    Top_fore_head=(Fore_head[0],Fore_head[1]-35)

    Face_height=dist(Top_fore_head,Chin)
    Lower_face_height=dist(Between_Eye_C,Chin)

    LFFH=Lower_face_height/Face_height

    FWLF=Cheek_Bone_width/Lower_face_height

    R_EB_R=(int(key[53]['X']*w),int(key[53]['Y']*h))
    R_EB_C=(int(key[65]['X']*w),int(key[65]['Y']*h))
    R_EB_L=(int(key[55]['X']*w),int(key[55]['Y']*h))
    L_EB_R=(int(key[285]['X']*w),int(key[285]['Y']*h))
    L_EB_C=(int(key[295]['X']*w),int(key[295]['Y']*h))
    L_EB_L=(int(key[283]['X']*w),int(key[283]['Y']*h))
    R_eye_top_c=(int(key[159]['X']*w),int(key[159]['Y']*h))
    L_eye_top_C=(int(key[386]['X']*w),int(key[386]['Y']*h))

    AEBE=(dist(R_EB_R,Right_eye_R)+dist(R_EB_C,R_eye_top_c)+dist(R_EB_L,Right_eye_L)+dist(L_EB_R,Left_eye_R)+dist(L_EB_C,L_eye_top_C)+dist(L_EB_L,Left_eye_L))/6

    return CJWR,WHR,PAR,ES,LFFH,FWLF,AEBE
