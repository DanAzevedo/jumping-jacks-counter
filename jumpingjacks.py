import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture('resources/jumpingjacks.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5) # Variável de detecção
draw = mp.solutions.drawing_utils # Desenhar as linhas e os pontos dentro do vídeo
count = 0
check = True

while True:
    ret, img = cap.read()
    videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)
    points = results.pose_landmarks
    draw.draw_landmarks(img, points, pose.POSE_CONNECTIONS)
    h, w, _ = img.shape # Extraindo as dimensões da imagem

    if points:
        # Extraimos o produto de y * h e x * w para converter a imagem em pixel
        rFootY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h) # Extraindo coordenadas do pé direito "y"
        rFootX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w) # Extraindo coordenadas do pé direito "x"
        lFootY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)  # Extraindo coordenadas do pé esquerdo "y"
        lFootX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)  # Extraindo coordenadas do pé esquerdo "x"
        rHandY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h) # Extraindo coordenadas da mão direita "y"
        rHandX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x*w) # Extraindo coordenadas da mão direita "x"
        lHandY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)  # Extraindo coordenadas da mão esquerda "y"
        lHandX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x*w)  # Extraindo coordenadas da mão esquerda "x"

        # Cálculo de distância entre dois pontos
        handDist = math.hypot(rHandX - lHandX, rHandY - lHandY)
        footDist = math.hypot(rFootX - lFootX, rFootY - lFootY)

        print(f'Mãos {handDist} Pés {footDist}')
        # Melhor resultado hands<=150 - foot >=150

        if check == True and handDist <= 150 and footDist >= 150: # Há polichinelos
            count += 1
            check = False # Para não contabilizar o mesmo valor duas vezes
        if handDist > 150 and footDist < 150: # Não há polichinelos
            check = True

        text = f'DONE {count}'
        cv2.rectangle(img, (20,240), (280,120), (255,0,0), -1)
        cv2.putText(img, text, (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)


    cv2.imshow('Result', img)
    cv2.waitKey(40)