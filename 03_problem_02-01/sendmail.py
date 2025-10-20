import csv
import os
import sys
import ssl
import smtplib
from typing import List, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_HOST = 'smtp.naver.com'
SMTP_PORT = 587  # STARTTLS
CSV_FILENAME = './03_problem_02-01/mail_target_list.csv'

def load_recipients_from_csv(path: str) -> List[Tuple[str, str]]:
    recipients: List[Tuple[str, str]] = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if '이름' not in reader.fieldnames or '이메일' not in reader.fieldnames:
                raise ValueError('CSV 헤더에 "이름,이메일" 이 포함되어야 합니다.')
            for row in reader:
                name = (row.get('이름') or '').strip()
                email = (row.get('이메일') or '').strip()
                if name and email and '@' in email:
                    recipients.append((name, email))
    except FileNotFoundError:
        print(f'CSV 파일을 찾을 수 없습니다: {path}')
        sys.exit(1)
    except Exception as e:
        print('CSV 읽기 중 오류 발생:', e)
        sys.exit(1)

    if not recipients:
        print('CSV에서 유효한 수신자 정보를 찾지 못했습니다.')
        sys.exit(1)
    return recipients

def build_message_html(sender: str, recipient_name: str, recipient_email: str,
                       subject: str, html_body: str) -> MIMEMultipart:
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_body, 'html', _charset='utf-8'))
    return msg

def send_bulk_individual(sender_email: str, app_password: str, recipients: List[Tuple[str, str]],
                         subject: str, html_template: str) -> None:
    context = ssl.create_default_context() # TLS(보안 연결)를 위한 기본 SSL 컨텍스트 생성
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, app_password)

            for name, email in recipients:
                html_body = html_template.format(name=name)

                msg = build_message_html(
                    sender=sender_email,
                    recipient_name=name,
                    recipient_email=email,
                    subject=subject,
                    html_body=html_body
                )
                server.sendmail(sender_email, [email], msg.as_string())
                print(f'[개별] 전송 완료: {name} <{email}>')

    except smtplib.SMTPAuthenticationError:
        print('인증 실패: 이메일 주소 또는 앱 비밀번호를 확인하세요.')
        sys.exit(1)
    except smtplib.SMTPConnectError:
        print('SMTP 서버에 연결할 수 없습니다.')
        sys.exit(1)
    except Exception as e:
        print('개별 발송 중 오류 발생:', e)
        sys.exit(1)

def main() -> None:
    sender_email = os.getenv("naver_id")
    app_password = os.getenv("naver_pw")
    if not sender_email or not app_password:
        print('환경변수 NAVER_USER, NAVER_APP_PASSWORD 를 설정하세요.')
        sys.exit(1)

    recipients = load_recipients_from_csv(CSV_FILENAME)

    # 메일 제목/본문(HTML + 텍스트) — 스토리 반영, {name} 자리표시자 사용
    subject = '당신의 메시지를 받았습니다.'

    html_template = (
        '<html>'
        '<body style="font-family: Arial, sans-serif; line-height:1.6;">'
        '<p>{name}님께,</p>'
        '<p>한 박사님! 메시지를 받았지만 상황을 완전히 이해하지는 못했습니다.<br>'
        '그래도 살아 계셔서 너무 감사드리며, 저희도 최선을 다하겠습니다.<br>'
        '혹시 몰라 이 메시지를 한국어로 보내드립니다.</p>'
        '<p style="margin-top:16px;">이 메일은 안정적인 전달을 위해 준비된 자동 중계입니다. '
        '응원해 주셔서 감사합니다.</p>'
        '</body>'
        '</html>'
    )

    # 두 방식 모두 시도 가능: 우선 개별 발송(권장)
    send_bulk_individual(
        sender_email=sender_email,
        app_password=app_password,
        recipients=recipients,
        subject=subject,
        html_template=html_template
    )

if __name__ == '__main__':
    main()
