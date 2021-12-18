import cv2
import numpy as np
import os
import face_recognition
from datetime import datetime

# separate the image name and its type
# getting info from the file where we have our images

path = 'student'
images = []
student_name = []
listed_student = os.listdir(path)
print(listed_student)

for cur_img in listed_student:
    current_image = cv2.imread(f'{path}/{cur_img}')
    images.append(current_image)
    student_name.append(os.path.splitext(cur_img)[0])




# encoding of faces
def faceEncoding(image):
    encodedList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedList.append(encode)
    return encodedList


face_codes = faceEncoding(images)




# to collect the information and put it in the excel sheat

def Entry_Book(name):
    with open('attendence.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        # print(myDataList)
        for line in myDataList:
            entered = line.split(',')
            nameList.append(entered[0])

        if name not in nameList:
            time_now = datetime.now()
            tstr = time_now.strftime('%H:%M:%S')
            dstr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n {name}, {tstr}, {dstr}')
        



'''' reading image from the webcam
# for webcam of laptop id=0
# face_recognition'''

print("Is the Current student is New!")
print("Enter Yes or No")
state = input()
state = state.upper()

if state == 'NO':
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        face = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        face_in_current_frame = face_recognition.face_locations(face)
        code_for_cur_frame = face_recognition.face_encodings(face, face_in_current_frame)

        for encode_face, face_loc in zip(code_for_cur_frame, face_in_current_frame):
            match = face_recognition.compare_faces(face_codes, encode_face)
            fac_dis = face_recognition.face_distance(face_codes, encode_face)

            matchIndex = np.argmin(fac_dis)

            if match[matchIndex]:
                name = student_name[matchIndex]

                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 36), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
                Entry_Book(name)

        cv2.imshow("camera", frame)
        if cv2.waitKey(10) == 13:
            break

else:
    # capturing the image and inserting it into the student folder which is working as database
    cam = cv2.VideoCapture(0)
    path2= 'student'

    print("enter the name : ")
    name = input()
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("NewStudent", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            break
        elif k % 256 == 32:
            img_name = name + ".png".format()
            cv2.imwrite(f'{path2}/{img_name}', frame)
            print("the ragistration is done and attendence has recorded!")
    Entry_Book(name)



