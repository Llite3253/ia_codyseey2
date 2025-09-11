from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime
from urllib.request import urlopen
import json

PORT = 8080

def get_ip_location(ip):
    try:
        with urlopen(f'http://ip-api.com/json/{ip}') as response:
            data = json.loads(response.read().decode())
            if data['status'] == 'success':
                return f"{data['country']} {data['regionName']} {data['city']}"
            else:
                return '위치 정보를 찾을 수 없음'
    except Exception as e:
        return f'위치 조회 실패: {e}'

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 위치 정보 조회
        location_info = get_ip_location(client_ip)

        print(f'[{now}] 접속한 클라이언트 IP: {client_ip}')
        print(f'[{now}] 접속한 위치 정보: {location_info}')

        # index.html 파일 응답
        if self.path == '/' or self.path == '/index.html':
            self.path = 'index.html'

        return super().do_GET()

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, MyRequestHandler)

    print(f'웹 서버가 {PORT}번 포트에서 시작되었습니다.')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버를 종료합니다.')
    finally:
        httpd.server_close()

if __name__ == '__main__':
    run_server()