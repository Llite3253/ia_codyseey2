from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_mail_titles(driver):
    """네이버 메일 제목들을 리스트로 수집"""
    driver.get("https://mail.naver.com/")
    time.sleep(3)

    titles = []
    try:
        mail_elements = driver.find_elements(By.CSS_SELECTOR, ".mail_title, .subject strong, a.subject")
        for elem in mail_elements[:10]:
            text = elem.text.strip()
            if text:
                titles.append(text)
    except Exception:
        titles.append("메일을 가져오지 못했습니다.")

    return titles

def main():
    driver = webdriver.Chrome()

    # 네이버 로그인 페이지 열기
    driver.get("https://nid.naver.com/nidlogin.login")

    # 📌 여기서 직접 아이디/비밀번호/자동입력방지 입력
    input("👉 네이버 로그인 완료 후 Enter 키를 누르세요...")

    # 로그인 후 메일 제목 가져오기
    mail_titles = get_mail_titles(driver)

    print("📧 로그인 후 수집한 메일 제목:")
    if mail_titles:
        for t in mail_titles:
            print("\n-", t)
    else:
        print("메일이 없습니다.")

    driver.quit()


if __name__ == "__main__":
    main()
