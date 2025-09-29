from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time
import pyperclip
from dotenv import load_dotenv
import os

load_dotenv()

def naver_login(user_id, user_pw):
    """네이버 로그인 후 드라이버 객체 반환"""
    driver = webdriver.Chrome()  # 크롬드라이버 실행
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(2)

    # 아이디, 비밀번호 입력
    id_input = driver.find_element(By.ID, "id")
    id_input.click()
    pyperclip.copy(user_id)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)

    pw_input = driver.find_element(By.ID, "pw")
    pw_input.click()
    pyperclip.copy(user_pw)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(2)

    pw_input.send_keys(Keys.RETURN)
    time.sleep(3)

    return driver

def get_mail_titles(driver):
    """네이버 메일 제목들을 리스트로 수집"""
    driver.get('https://mail.naver.com/')
    time.sleep(3)

    titles = []
    try:
        mail_elements = driver.find_elements(By.CSS_SELECTOR, '.mail_title')
        for elem in mail_elements[:10]:  # 앞 10개만 수집
            titles.append(elem.text.strip())
    except Exception:
        titles.append('메일을 가져오지 못했습니다.')

    return titles

def main():
    # TODO: 본인 네이버 계정 정보 입력
    user_id = os.getenv("NAVER_ID")
    user_pw = os.getenv("NAVER_PW")

    driver = naver_login(user_id, user_pw)

    # 로그인 후 메일 제목 가져오기
    mail_titles = get_mail_titles(driver)

    print('📧 로그인 후 수집한 메일 제목:')
    for t in mail_titles:
        print('-', t)

    driver.quit()

if __name__ == '__main__':
    main()
