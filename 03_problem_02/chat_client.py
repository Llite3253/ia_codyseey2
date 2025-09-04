import socket
import threading

host = '127.0.0.1'
port = 1234

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            print(msg.decode())
        except:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        recv_thread = threading.Thread(target=receive_messages, args=(sock,))
        recv_thread.daemon = True
        recv_thread.start()

        while True:
            msg = input()
            if msg == '/종료':
                sock.sendall(msg.encode())
                break
            sock.sendall(msg.encode())

if __name__ == '__main__':
    main()