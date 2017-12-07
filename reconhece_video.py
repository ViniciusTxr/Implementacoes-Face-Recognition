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


# Abre o video de entrada
input_movie = cv2.VideoCapture("obama_curry.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

larg = int(input_movie.get(3))  
alt = int(input_movie.get(4))

print(larg, alt)

# Cria um video de saida (mesma resolução e frames do video de entrada)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('saida.avi', fourcc, 29.97, (854, 480))

# carrega as faces conhecidas em uma base de imagens conhecidas
known_names, known_face_encodings = scan_known_people("./conhecidos")

face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # pega um frame do video
    ret, frame = input_movie.read()
    frame_number += 1

    # Sai quando o video de entrada acaba
    if not ret:
        break

    # Encontra todas as faces e as codificaçoes das faces no frame atual do video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # ve se alguma face do frame é conhecida
        #quanto menor a tolerancia, maior será a precisao
        match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)

        #associa o(s) rosto(s) conhecido(s) ao(s) seu(s) respectivo(s) nome(s).
        for i in range(0,len(known_names)):
            if match[i]:
                name = known_names[i]
                face_names.append(name)
                i = len(known_names)

    # Marca os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # desenha um quadrado em volta da face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # escreve o nome embaixo da face reconhecida
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # escreve a imagem resultante no video de saida
    print("Escrevendo frame {} / {}".format(frame_number, length))
    output_movie.write(frame)

input_movie.release()
cv2.destroyAllWindows()
