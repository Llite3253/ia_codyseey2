from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
import json


def get_ip_location(ip=None):
    # ip-api.com 무료 API 활용   
    try:
        if ip:
            url = f'http://ip-api.com/json/{ip}'
        else:
            url = 'http://ip-api.com/json/'  # 공인 IP 기준
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data.get('status') == 'success':
                return f"{data.get('country')} {data.get('regionName')} {data.get('city')}"
            else:
                return '위치 정보를 찾을 수 없음'
    except Exception as e:
        return f'위치 조회 실패: {e}'

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # favicon 요청은 로그하지 않고 무시
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return None
        
        print('GET 요청이 들어왔습니다.')

        # index.html 파일 읽기
        try:
            with open('3-4/index.html', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1>')
            return None
        
        # 200 응답 전송
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        # index.html 내용 전송
        self.wfile.write(content.encode('utf-8'))
        
        # 위치 정보 조회 (로컬호스트는 조회 불가)
        location_info = get_ip_location()
        print(f'위치 정보: {location_info}')

    def do_POST(self):
        print('POST 요청이 들어왔습니다.')


def run():
    # httpd = HTTPServer(('0.0.0.0', 8080), MyHandler) # 단일 접속 처리
    httpd = ThreadingHTTPServer(('0.0.0.0', 8080), MyHandler) # 다중 접속 처리
    print('Server Start')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server Interrupted')
    finally:
        httpd.server_close()
        print('Server End')


if __name__ == '__main__':
    run()
