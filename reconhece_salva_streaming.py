import face_recognition
import cv2
import os
import re
import time

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


#lar = 640
#alt = 480

video_capture = cv2.VideoCapture(0)
lar = int(video_capture.get(3))
alt = int(video_capture.get(4))

#video_capture.set(3,lar);
#video_capture.set(4,alt);


# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('out1.avi', fourcc, 5, (lar, alt))

# Load a sample picture and learn how to recognize it.

known_names, known_face_encodings = scan_known_people("./conhecidos")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0
process_this_frame = 1

while True:
    # Grab a single frame of video
    frame_number += 1
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if ((process_this_frame%10) == 0):
        process_this_frame = 1
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        
        if (len(face_locations) == 0):
            time.sleep(.30)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
            name = "Desconhecido"
            flag = 0
            
            for i in range(0,len(known_names)):
                if match[i]:
                    name = known_names[i]
                    face_names.append(name)
                    flag = 1
                    i = len(known_names)

            if flag == 0:
                face_names.append(name)


    process_this_frame += 1



    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)


    if ((process_this_frame%3) == 0):
        #time.sleep(1)
        print("Escrevendo frame {}".format(frame_number))
        output_movie.write(frame)


    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


