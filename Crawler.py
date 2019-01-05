from bs4 import BeautifulSoup
import requests
links = []

def parserToCSV(fileName,output):
    file = open(fileName,'r')
    filesCSV = open(output,'w')
    filesCSV.write('Company, CPU company, CPU model, touchscreen, Link\n')

    for info in file:
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
        links
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

for i in range(0,250):
    #filter("https://www.amazon.in/s/ref=lp_1375424031_pg_2?rh=n%3A976392031%2Cn%3A%21976393031%2Cn%3A1375424031&page=" + str(i) + "&ie=UTF8&qid=1546012663")
    parserToCSV("results_black.txt","results_black.csv")
    parserToCSV("results_office.txt","results_office.csv")
    parserToCSV("results_inspiron.txt","results_inspiron.csv")


def save_all_links_as_html(from_page, to_page, results_per_page):

    print("Saving all links as html files...")

    count = 0

    for i in range(from_page, to_page + 1):
        source = requests.get("http://www.dx.com/s/security+camera?cateId=0&cateName=All%20Categories&PageIndex=" + str(i) + "#sortBar", headers=agent).text
        soup = BeautifulSoup(source)

        links = []

        for k in range(0, results_per_page):
            results = soup.findAll("a", {"id": "content_ProductList1_rpProducts_lnkShortHeadLine1_"+str(k)})
            links.append(results[0]["href"])

            source2 = requests.get(links[k], headers=agent).text
            soup2 = BeautifulSoup(source2)

            with open("dxHTML/" + str(count) + ".html", "w") as file:
                file.write(str(soup2))

            print(count)


            count = count + 1
