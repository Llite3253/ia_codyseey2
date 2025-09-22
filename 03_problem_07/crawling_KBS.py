import requests
from bs4 import BeautifulSoup

def fetch_kbs_headlines():
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'
    response = requests.get(url)

    if response.status_code != 200:
        print('KBS 페이지 요청 실패:', response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headline_list = []

    main_wrapper = soup.find('div', class_='main-news-wrapper')
    if main_wrapper is not None:
        main_title = main_wrapper.find('p', class_='title')
        if main_title:
            title = main_title.get_text(separator=' ', strip=True)
            headline_list.append(title)

    sub_wrapper = soup.find('div', class_='small-sub-news-wrapper')
    if sub_wrapper is not None:
        sub_titles = sub_wrapper.find_all('p', class_='title')
        for tag in sub_titles:
            title = tag.get_text(separator=' ', strip=True)
            headline_list.append(title)

    return headline_list

def fetch_naver_weather():
    url = 'https://search.naver.com/search.naver?query=날씨'
    response = requests.get(url)

    if response.status_code != 200:
        print('날씨 페이지 요청 실패:', response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    weather_list = []

    temp_tag = soup.find('div', class_='temperature_text')
    if temp_tag:
        temperature = temp_tag.get_text(strip=True)
        weather_list.append(f'현재 온도: {temperature}')

    condition_tag = soup.find('span', class_='weather before_slash')
    if condition_tag:
        condition = condition_tag.get_text(strip=True)
        weather_list.append(f'날씨 상태: {condition}')

    summary_tags = soup.select('dl.summary_list > div.sort > dd.desc')
    labels = ['체감 온도', '습도', '풍속']
    for i, tag in enumerate(summary_tags[:3]):
        weather_list.append(f'{labels[i]}: {tag.get_text(strip=True)}')

    return weather_list

def fetch_naver_popular_stocks():
    url = 'https://finance.naver.com/sise/lastsearch2.naver'
    response = requests.get(url)

    if response.status_code != 200:
        print('주식 페이지 요청 실패:', response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    stock_list = []

    rows = soup.select('table.type_5 tr')[2:]  # Skip header rows

    for row in rows[:5]:  # 상위 5개만 가져오기
        cols = row.select('td')
        if len(cols) >= 2:
            name = cols[1].get_text(strip=True)
            price = cols[3].get_text(strip=True)
            stock_list.append(f'{name}: {price}원')

    return stock_list

def main():
    while True:
        print('\n--- 정보 선택 ---')
        print('1. KBS 헤드라인 뉴스')
        print('2. 네이버 날씨')
        print('3. 네이버 인기 주식')
        print('0. 종료')

        choice = input('번호를 선택하세요 (0~3): ').strip()

        if choice == '1':
            headlines = fetch_kbs_headlines()
            print('\nKBS 헤드라인 뉴스:')
            for i, title in enumerate(headlines, start=1):
                print(f'{i}. {title}')

        elif choice == '2':
            weather = fetch_naver_weather()
            print('\n현재 날씨 정보:')
            for item in weather:
                print('-', item)

        elif choice == '3':
            stocks = fetch_naver_popular_stocks()
            print('\n인기 검색 주식 TOP 5:')
            for i, item in enumerate(stocks, start=1):
                print(f'{i}. {item}')

        elif choice == '0':
            print('프로그램을 종료합니다.')
            break

        else:
            print('잘못된 입력입니다. 0~3 중에서 선택하세요.')

if __name__ == '__main__':
    main()