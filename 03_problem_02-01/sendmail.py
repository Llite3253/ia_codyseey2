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

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587  # STARTTLS
CSV_FILENAME = './03_problem_02-01/mail_target_list.csv'


def load_recipients_from_csv(path: str) -> List[Tuple[str, str]]:
    """CSV 파일에서 (이름, 이메일) 목록을 읽어 반환한다."""
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
                       subject: str, plain_body: str, html_body: str) -> MIMEMultipart:
    """
    HTML/텍스트 대체 파트를 포함한 메시지 생성.
    첨부 없이 본문만 전송하므로 multipart/alternative 사용.
    """
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # 텍스트 버전(대체) + HTML 버전 추가
    msg.attach(MIMEText(plain_body, 'plain', _charset='utf-8'))
    msg.attach(MIMEText(html_body, 'html', _charset='utf-8'))
    return msg


def send_bulk_individual(sender_email: str, app_password: str,
                         recipients: List[Tuple[str, str]],
                         subject: str, plain_template: str, html_template: str) -> None:
    """
    한 명씩 개별 발송(권장).
    장점: 개인화 가능, 수신자 노출 방지, 스팸 점수 완화.
    """
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, app_password)

            for name, email in recipients:
                plain_body = plain_template.format(name=name)
                html_body = html_template.format(name=name)

                msg = build_message_html(
                    sender=sender_email,
                    recipient_name=name,
                    recipient_email=email,
                    subject=subject,
                    plain_body=plain_body,
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


def send_bulk_single(sender_email: str, app_password: str,
                     recipients: List[Tuple[str, str]],
                     subject: str, plain_template: str, html_template: str) -> None:
    """
    여러 명을 한 번에 발송.
    단점: 수신자 노출 가능, 스팸 점수 상승 위험. 실무에선 BCC 사용 권장.
    여기서는 데모 목적상 To에 나열한다.
    """
    # 공통 본문(개인화 최소화)
    plain_body = plain_template.format(name='여러분')
    html_body = html_template.format(name='everyone')

    # 수신자 주소 문자열
    all_emails = [email for _, email in recipients]

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ', '.join(all_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(plain_body, 'plain', _charset='utf-8'))
    msg.attach(MIMEText(html_body, 'html', _charset='utf-8'))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, all_emails, msg.as_string())
            print(f'[일괄] 전송 완료: {len(all_emails)}명')
    except smtplib.SMTPAuthenticationError:
        print('인증 실패: 이메일 주소 또는 앱 비밀번호를 확인하세요.')
        sys.exit(1)
    except smtplib.SMTPConnectError:
        print('SMTP 서버에 연결할 수 없습니다.')
        sys.exit(1)
    except Exception as e:
        print('일괄 발송 중 오류 발생:', e)
        sys.exit(1)


def main() -> None:
    """프로그램 진입점."""
    sender_email = os.getenv("gmail_id")
    app_password = os.getenv("gmail_pw")
    if not sender_email or not app_password:
        print('환경변수 GMAIL_USER, GMAIL_APP_PASSWORD 를 설정하세요.')
        sys.exit(1)

    recipients = load_recipients_from_csv(CSV_FILENAME)

    # 메일 제목/본문(HTML + 텍스트) — 스토리 반영, {name} 자리표시자 사용
    subject = 'We received your message, Dr. Han — HTML Broadcast'

    plain_template = (
        'Dear {name},\n'
        '“Dr. Han!!, we received your message, but we could not understand the situation...”\n'
        'We are so grateful that you are alive. We will do our best, too.\n'
        'This message is sent in English just in case.\n\n'
        '— Automated relay from Mars mission'
    )

    html_template = (
        '<html>'
        '<body style="font-family: Arial, sans-serif; line-height:1.6;">'
        '<p>Dear <strong>{name}</strong>,</p>'
        '<p>“Dr. Han!!, we received your message, but we could not understand the situation, '
        'so we all froze, and we do not even know how much we cried after hugging each other. '
        'We are so grateful that you are alive, and we will do our best too. '
        'Just in case your condition is not good, we are sending this message in English.”</p>'
        '<p style="margin-top:16px;">This is an automated relay prepared to ensure the message travels '
        'across space reliably. Thank you for your support.</p>'
        '<p>— Mars Mission Relay</p>'
        '</body>'
        '</html>'
    )

    # 두 방식 모두 시도 가능: 우선 개별 발송(권장)
    send_bulk_individual(
        sender_email=sender_email,
        app_password=app_password,
        recipients=recipients,
        subject=subject,
        plain_template=plain_template,
        html_template=html_template
    )

    # 필요 시 일괄 발송도 테스트하려면 주석 해제
    # send_bulk_single(
    #     sender_email=sender_email,
    #     app_password=app_password,
    #     recipients=recipients,
    #     subject=subject,
    #     plain_template=plain_template,
    #     html_template=html_template
    # )


if __name__ == '__main__':
    main()
