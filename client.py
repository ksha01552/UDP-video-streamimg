import cv2, imutils, socket, numpy as np, time, base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = ''
port = 9995
message = b'hiiiiii'
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
client_socket.sendto(message, (host_ip,port))

while True:
    packet,_ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet,' /')
    npdata = np.fromstring(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)
    frame = cv2.putText(frame, 'Client side : FPS : ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.imshow('Receiving video', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count/(time.time() - st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1