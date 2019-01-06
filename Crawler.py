import time

from bs4 import BeautifulSoup
from collections import defaultdict
import requests

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

links = []
docs = []
inv_indx = defaultdict(set)


def save_link_as_doc(link, count):
    if count > 20: return
    print("Page number " + str(count) + " was saved")
    code = requests.get(link)
    plain = code.text
    time.sleep(360)
    s = BeautifulSoup(plain, "html.parser")
    if(s is not None):
        doc = str(' '.join((str(s.find('div', {'id': 'feature-bullets'}).text)).replace('\n', ' ').replace('\t', ' ').replace('-',' ').replace( ':', ' ').replace('|', ' ').replace(',', ' ').split()))
        doc = doc.lower()
        docs.append(doc)

def  calc_inv_indx(count):
    if count > 20: return
    for word in docs[count].split():
        inv_indx[word].add(count)
    count = count + 1

def create_inv_indx():
    indexCsv = open('index_inspiron.csv', 'w')
    for key in inv_indx.keys():
        toCsv = str(inv_indx[key])
        toCsv = toCsv.replace(',', '->')
        toCsv = toCsv.replace('{', '')
        toCsv = toCsv.replace('}', '')
        indexCsv.write(key + ',' + toCsv + ',' + str(len(inv_indx[key]))+ '\n')
    print(" ")
    indexCsv.close()


def parserToCSV(fileName,output):
    file = open(fileName,'r')
    filesCSV = open(output,'w')
    filesCSV.write('Company, CPU company, CPU model, touchscreen, Link\n')
    count = 0
    for info in file:
        ###to function ###
        companies = ["HP", "Dell", "Lenovo","ACER","Acer Consumer","Alienware","Alphacool","Aorus","Apple","Aspire","Asus","Azom","CIRCLE","Compaq","Computer Upgrade King","CyberpowerPC","Dell","ELECTROPRIME","Ematic","Fujitsu","Generic","Getac","Gigabyte","Google","HardDriveGeeks","HITSAN INCORPORATION","HP","Huawei","Hyundai","iBall","IBM","iBUYPOWER","Intel","Jumper","Koolance","Lava","Lenovo","LEPAKSHI)","LG","Micromax","Mi" ,"crosoft","MITXPC","MSI","Qotom","Razer","RCA","RDP","Reach","Samsung","SAMSUNG","Shop The World","Stillersafe","Torque Traders"]
        cpuModels = ["i3", "i5", "i7","i9","Pentium","Celeron", "Atom","A4","A8","Athlon", "A10", "A6"]
        isTouchscreen = "No"
        company = "None"
        cpuModel = "None"
        cpuCopmany = "None"
        for c in companies:
            if c.lower() in info.lower():
                company = c
        for m in cpuModels:
            if m.lower() in info.lower():
                cpuModel = m
        if 'touchscreen' in info.lower():
            isTouchscreen = "yes"
        if 'intel' in info.lower():
            cpuCopmany = "intel"
        else:
            if 'amd' in info.lower():
                cpuCopmany = "amd"
        filesCSV.write(company + ',')
        filesCSV.write(cpuCopmany + ',')
        filesCSV.write(cpuModel + ',')
        filesCSV.write(isTouchscreen + ',')
        link = file.readline()
        filesCSV.write(link)
        save_link_as_doc(link, count)
        calc_inv_indx(count)
        count += 1
    create_inv_indx()
    file.close()
    filesCSV.close()


def filter(webUrl):
    files = [open("results_black.txt", "a"), open("results_office.txt", "a"), open("results_inspiron.txt", "a")]
    words = ["black","office","inspiron"]
    url = webUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    for link in s.findAll('a', {'class':'s-access-detail-page'}):
        info = link.get('title')
        link = link.get('href')
        links.append(link)
        info = info.lower()
        if words[0] in info:
            files[0].write(info + '\n')
            files[0].write(link + '\n')
        if words[1] in info:
            files[1].write(info + '\n')
            files[1].write(link + '\n')
        if words[2] in info:
            files[2].write(info + '\n')
            files[2].write(link + '\n')
    files[0].close()
    files[1].close()
    files[2].close()



for i in range(0,1):
    #filter("https://www.amazon.in/s/ref=lp_1375424031_pg_2?rh=n%3A976392031%2Cn%3A%21976393031%2Cn%3A1375424031&page=" + str(i) + "&ie=UTF8&qid=1546012663")
    #parserToCSV("results_black.txt","results_black.csv")
    #parserToCSV("results_office.txt","results_office.csv")
    parserToCSV("results_inspiron.txt","results_inspiron.csv")

