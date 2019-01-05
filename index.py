from bs4 import BeautifulSoup
import requests


def createResultsTextsFiles(i, webUrl):
    file = open("doc" + str(i) + ".txt", "a")
    url = webUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    for link in s.findAll('a', {'class': 's-access-detail-page'}):
        info = link.get('title')
        link = link.get('href')
        info = info.lower()
        link = link.lower
        file.write(info + ' ' + link + '\n')
    file.close()


for i in range(0, 20):
    createResultsTextsFiles(i,
                            "https://www.amazon.in/s/ref=lp_1375424031_pg_2?rh=n%3A976392031%2Cn%3A%21976393031%2Cn%3A1375424031&page=" + str(
                                i) + "&ie=UTF8&qid=1546012663")
