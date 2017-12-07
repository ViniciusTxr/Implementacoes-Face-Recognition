import face_recognition
import cv2
import os
import re
from PIL import Image



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




# carrega as faces conhecidas em uma base de imagens conhecidas
known_names, known_face_encodings = scan_known_people("./conhecidos")

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

# carrega as faces desconhecidas em uma imagem
image = cv2.imread("./desconhecidos/algar.jpg")

face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

x = True

while x:

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        #quanto menor a tolerancia, maior será a precisao
        match = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.50)
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



    # Mostra os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        

        # desenha um quadrado em volta da face
        cv2.rectangle(image, (left-10, top-10), (right+10, bottom+10), (0, 0, 255), 2)

        # escreve o nome embaixo da face 
        cv2.rectangle(image, (left-10, bottom - 5), (right+10, bottom+10), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left, bottom + 6), font, 0.5, (255, 255, 255), 1)

    # mostra a imagem resultante
    cv2.imshow('Image', image)
    cv2.imwrite('saida_img.png',image)

    x = False

cv2.waitKey(0)
cv2.destroyAllWindows()


