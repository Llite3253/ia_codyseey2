import socket
import threading

host = '0.0.0.0'
port = 1234

clients = {}
lock = threading.Lock()

def broadcast_message(message, exclude_client = None):
    with lock:
        for client, name in clients.items():
            if client != exclude_client:
                try:
                    client.sendall(message.encode())
                except Exception:
                    continue

def private_message(sender_name, target_name, message) :
    with lock:
        for client, name in clients.items():
            if name == target_name:
                try:
                    client.sendall(f'(귓속말) {sender_name}> {message}'.encode())
                except Exception:
                    continue
                return True
    return False

def handle_client(client_socket, addr):
    try:
        client_socket.sendall('사용자 이름을 입력하세요: '.encode())
        name = client_socket.recv(1024).decode().strip()

        with lock:
            clients[client_socket] = name

        print(f'{name}님 접속 {addr}')
        broadcast_message(f'{name}님이 입장하셨습니다.')

        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            decoded_msg = msg.decode().strip()
            if decoded_msg == '/종료':
                break

            if decoded_msg.startswith('/귓속말'):
                parts = decoded_msg.split(' ', 2)
                if len(parts) < 3:
                    client_socket.sendall('형식: /귓속말 [대상이름] [메시지]'.encode())
                    continue
                _, target_name, private_msg = parts
                success = private_message(name, target_name, private_msg)
                if not success:
                    client_socket.sendall(f'{target_name}님을 찾을 수 없습니다.'.encode())
                continue

            broadcast_message(f'{name}> {decoded_msg}', exclude_client=None)

    except Exception as e:
        print(f'오류 발생: {e}')

    finally:
        with lock:
            if client_socket in clients:
                left_name = clients.pop(client_socket)
        broadcast_message(f'{left_name}님이 퇴장하셨습니다.')
        client_socket.close()
        print(f'연결 종료: {addr}')

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    server_socket.settimeout(1.0)

    print(f'서버 시작: {host}:{port}')
    try:
        while True:
            try:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print('서버 종료 중...')
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()