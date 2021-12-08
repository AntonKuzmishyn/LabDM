from bs4 import BeautifulSoup as bs
import requests
import xlsxwriter

URL = "https://www.playground.ru/cyberpunk_2077/opinion"
HOST = "https://www.playground.ru"
HEADERS = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}


def gethtml(url, params):
    print(url+str(params))
    return requests.get(url+str(params), headers=HEADERS)


def getcontent(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='post-content')
    posts = []
    for item in items:
        posts.append({
            'title': item.find('div', class_='post-title').find_next('a').get_text(strip=True),
            'link': item.find('div', class_='post-title').find_next('a').get('href'),
            'comments': item.
                find('div', class_='post-footer post-metadata').
                find_next('div', class_="post-footer-aside").
                find_next('span', class_="module-item-counters").
                find_next('a', class_="comments-link").get_text(strip=True),
            'rating': item.
                find('div', class_='post-footer post-metadata').
                find_next('div', class_="post-footer-aside").
                find_next('span', class_="module-item-counters").
                find_next('span', class_="post-rating-counter").get_text(strip=True),

        })
    return posts


def get_pages_count(html):
    soup = bs(html, 'html.parser')
    pagination = soup.find_all('li', class_='page-item')
    if pagination:
        return int(pagination[-2].find_next('a').get_text())
    else:
        return 1


def parse():
    html = gethtml(URL, "?p=1")

    if html.status_code == 200:
        posts = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} from {pages_count}...')
            html = gethtml(URL, params=f'?p={page}')
            posts.extend(getcontent(html.text))
        print(posts)
        return posts
    else:
        print('Error')


if __name__ == '__main__':
    posts = parse()

    workbook = xlsxwriter.Workbook('LabDM.xlsx')
    worksheet = workbook.add_worksheet('Parsed')

    row = 0
    col = 0

    for elem in posts:
        worksheet.write(row, col, elem['title'])
        worksheet.write(row, col + 1, elem['link'])
        worksheet.write(row, col + 2, elem['comments'])
        worksheet.write(row, col + 3, elem['rating'])
        row += 1

    workbook.close()



