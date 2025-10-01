import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()

def send_email_with_attachment():
    sender_email = os.getenv("gmail_mail")
    sender_password = os.getenv("gmail_pw")
    receiver_email = 'gfsy54@naver.com'

    subject = 'SMTP 메일 전송 (본문 + 첨부파일)'
    body = '안녕하세요.\n이 메일은 Python에서 SMTP를 사용해 보낸 테스트 메일입니다.\n첨부파일도 함께 전달됩니다.'

    # MIMEMultipart 객체 생성
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 본문 추가
    message.attach(MIMEText(body, 'plain'))

    # 첨부할 파일 경로
    filename = 'test.txt'

    try:
        # 파일 읽어서 첨부
        with open(filename, 'rb') as attachment:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(attachment.read())

        encoders.encode_base64(mime_base)
        mime_base.add_header(
            'Content-Disposition',
            f'attachment; filename={filename}'
        )
        message.attach(mime_base)

        # SMTP 서버 연결 및 메일 전송
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print('메일이 성공적으로 전송되었습니다.')

    except FileNotFoundError:
        print(f'첨부파일 {filename} 을 찾을 수 없습니다.')
    except smtplib.SMTPAuthenticationError:
        print('인증 실패: 이메일 주소나 비밀번호를 확인하세요.')
    except smtplib.SMTPConnectError:
        print('서버에 연결할 수 없습니다.')
    except Exception as e:
        print('메일 전송 중 오류 발생:', e)


if __name__ == '__main__':
    send_email_with_attachment()