from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime
import urllib.request
import json
import socketserver

PORT = 8080

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'[{now}] 접속한 클라이언트 IP: {client_ip}')

        self.print_location_info(client_ip)

        # 응답 상태 코드 200과 함께 index.html 전달
        if self.path == '/' or self.path == '/index.html':
            self.path = 'index.html'

        return super().do_GET()
    
    def print_location_info(self, ip):
        try:
            with urllib.request.urlopen(f'http://ip-api.com/json/{ip}') as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                result = json.loads(data.decode(encoding))

                if result['status'] == 'success':
                    print(f'국가: {result["country"]}, 도시: {result["city"]}')
                    print(f'ISP: {result["isp"]}')
                    print(f'지역: {result["regionName"]}, 위도: {result["lat"]}, 경도: {result["lon"]}')
                else:
                    print('위치 정보를 찾을 수 없습니다.')
        except Exception as e:
            print(f'[에러] 위치 정보 조회 실패: {e}')

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