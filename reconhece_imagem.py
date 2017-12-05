import face_recognition
import cv2
import os
import re
from PIL import Image

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 1:
            click.echo("ATENÇÃO: Mais de uma face encontrada em {}. Será considerada somente a primeira face.".format(file))

        if len(encodings) == 0:
            click.echo("ATENÇÃO: Nenhma face encontrada em {}. Arquivo ignorado.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings



def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]



# Load a sample picture and learn how to recognize it.

known_names, known_face_encodings = scan_known_people("./conhecidos")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []




image = cv2.imread("./desconhecidos/algar.jpg")


face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

x = True

while x:
    # Grab a single frame of video

    # Resize frame of video to 1/4 size for faster face recognition processing
    # Only process every other frame of video to save time

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.50)
        name = "N/C"
        flag = 0
        
        for i in range(0,len(known_names)):
            if match[i]:
                name = known_names[i]
                face_names.append(name)
                flag = 1
                i = len(known_names)

        if flag == 0:
            face_names.append(name)



    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        

        # Draw a box around the face
        cv2.rectangle(image, (left-10, top-10), (right+10, bottom+10), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(image, (left-10, bottom - 5), (right+10, bottom+10), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left, bottom + 6), font, 0.5, (255, 255, 255), 1)


       # face_image = image[top:bottom, left:right]
        #pil_image = Image.fromarray(face_image)
        #pil_image.show()

    cv2.imshow('image2', image)
    cv2.imwrite('saida_img.png',image)


    # Display the resulting image

    # Hit 'q' on the keyboard to quit!
    x = False

cv2.waitKey(0)
cv2.destroyAllWindows()


