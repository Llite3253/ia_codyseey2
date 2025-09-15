from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime
from urllib.request import urlopen
import json

PORT = 8080

def get_ip_location(ip=None):
    try:
        if ip:
            url = f'http://ip-api.com/json/{ip}'
        else:
            url = 'http://ip-api.com/json/'  # 공인 IP 기준
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data['status'] == 'success':
                return f"{data['country']} {data['regionName']} {data['city']}"
            else:
                return '위치 정보를 찾을 수 없음'
    except Exception as e:
        return f'위치 조회 실패: {e}'

class MyRequestHandler(SimpleHTTPRequestHandler):
    # 캐시 방지 헤더 추가
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        client_ip = self.client_address[0]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 위치 정보 조회
        location_info = get_ip_location()

        print(f'[{now}] 접속한 클라이언트 IP: {client_ip}', flush=True)
        print(f'[{now}] 접속한 위치 정보: {location_info}', flush=True)

        # index.html 파일 응답
        if self.path == '/' or self.path == '/index.html':
            self.path = 'index.html'

        return super().do_GET()

def run_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, MyRequestHandler)

    print(f'웹 서버가 {PORT}번 포트에서 시작되었습니다.', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버를 종료합니다.', flush=True)
    finally:
        httpd.server_close()

if __name__ == '__main__':
    run_server()
