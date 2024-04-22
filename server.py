import cv2, imutils, socket, numpy as np, time, base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip =''
port = 9995
server_socket.bind((host_ip, port))
# server_socket.listen(5)
print("Server listening")

vid = cv2.VideoCapture('1.mkv')
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print(f'Connected to client {client_addr}')
    width = 400
    while(vid.isOpened()):
        _, frame = vid.read()
        frame = imutils.resize(frame, width= width)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        server_socket.sendto(message, client_addr)
        frame = cv2.putText(frame, 'Server side : FPS : ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.imshow('Transmitting video', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1