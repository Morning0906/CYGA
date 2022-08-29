import requests
from bs4 import BeautifulSoup


def download_content(url):
    response = requests.get(url).text
    return response


def save(filename, content):
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(content)

def create_doc_from_filename(filename):
    with open(filename, "r", encoding='utf-8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, "lxml")
    return soup

def parse(soup):
    post_list = soup.find_all("table", class_="ch-table")
    for post in post_list:
        name = post.find_all("a")[0]
        print(name.text.strip())



def main():
    url = "https://yz.chsi.com.cn/sch/search.do?ssdm=&yxls=&ylgx=1"
    filename = "universities.html"
    result = download_content(url)
    save(filename, result)
    soup = create_doc_from_filename(filename)
    parse(soup)

if __name__ == '__main__':
    main()
