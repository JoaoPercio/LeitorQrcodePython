import cv2
from pyzbar.pyzbar import decode
import requests
import time
import numpy as np
 # Funcao para exibir a mensagem "aprovado" em verde
def display_approved_message():
     
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # defino a mensagem e o tamanho do texto
    mensagem = 'Aprovado'
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    escala = 1
    espessura = 4

    
    (largura_texto, altura_texto), baseline = cv2.getTextSize(mensagem, fonte, escala, espessura)
    x = (img.shape[1] - largura_texto) // 2
    y = (img.shape[0] + altura_texto) // 2

    #adiciona a mensagem "aprovado" em verde
    cv2.putText(img, mensagem, (x, y), fonte, escala, (0, 255, 0), espessura)
    
    #exiba a imagem
    cv2.imshow('Aprovado', img)
    cv2.waitKey(3000)  # exiba por 3 segundos
    cv2.destroyWindow('Aprovado')

def display_refused_message():
    
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    
    mensagem = 'Recusado'
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    escala = 1
    espessura = 4

    
    (largura_texto, altura_texto), baseline = cv2.getTextSize(mensagem, fonte, escala, espessura)
    x = (img.shape[1] - largura_texto) // 2
    y = (img.shape[0] + altura_texto) // 2

    cv2.putText(img, mensagem, (x, y), fonte, escala, (0, 0, 255), espessura)
   
    cv2.imshow('recusado', img)
    cv2.waitKey(3000)  
    cv2.destroyWindow('recusado')

# Inicializa a camera
cap = cv2.VideoCapture(0)

# Inicializa o timer
last_read_time = time.time()

while True:
    ret, frame = cap.read()

    #decodifica codigos QR na imagem
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        
        #verifique se ja se passaram 5 segundos desde a última leitura
        if time.time() - last_read_time >= 5:
            print(f"Código QR lido: {data}")
            url = f'http://localhost:5000/api/user/usarPasse/{data}'
            response = requests.post(url)
            print(response.status_code)
            if(response.status_code == 204):
                print("Aprovado")
                display_approved_message()
            if(response.status_code != 204):
                print("Recusado")
                display_refused_message()
            
            
            last_read_time = time.time()

    #quadro da câmera
    cv2.imshow('Câmera', frame)

    # tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere a câmera e feche todas as janelas
cap.release()
cv2.destroyAllWindows()