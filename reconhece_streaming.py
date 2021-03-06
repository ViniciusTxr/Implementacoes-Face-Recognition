import face_recognition
import cv2
import os
import re


#-----------------------------------------------------------------------

#função para encontrar todas as faces em uma pasta
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



#-----------------------------------------------------------------------



def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]



#-----------------------------------------------------------------------



# pega por referencia #0 que é o padrao para webcam
video_capture = cv2.VideoCapture(0)

# carrega as faces conhecidas em uma base de imagens conhecidas
known_names, known_face_encodings = scan_known_people("./conhecidos")

face_locations = []
face_encodings = []
face_names = []
process_this_frame = 10

while True:
    # pega um frame do video
    ret, frame = video_capture.read()

    #processa um frame a cada 10 (com a finalidade de otimizar)
    if ((process_this_frame%10) == 0):
    # Encontra todas as faces e as codificaçoes das faces no frame atual da webcam
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # ve se alguma face do frame é conhecida
            #quanto menor a tolerancia, maior será a precisao
            match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
            name = "N/C"
            flag = 0
            
             #associa o(s) rosto(s) encontrados ao(s) seu(s) respectivo(s) nome(s).
            for i in range(0,len(known_names)):
                if match[i]:
                    name = known_names[i]
                    face_names.append(name)
                    flag = 1
                    i = len(known_names)

            #se nao encontrou nenhuma face conhecida, entao marca ela com 'N/C' = nao conhecido
            if flag == 0:
                face_names.append(name)


    process_this_frame += 1


    # Mostra os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        # desenha um quadrado em volta da face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # escreve o nome embaixo da face 
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

    # mostra a imagem resultante na janela da webcam
    cv2.imshow('Video', frame)

    # apertar 'q' para encerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Encerra a webcam e fecha as janelas 
video_capture.release()
cv2.destroyAllWindows()


