from bs4 import BeautifulSoup
import requests 
import os
import sys

curse = "https://minecraft.curseforge.com"
gameversion = "1.12.2"
folder = "mods"

def download_file(url):
    r = requests.get(url)
    name = r.url.split("/")[-1].encode("ascii")
    with open(folder + "/" + name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return True

def check_update(name, time):
    cflink = curse + "/projects/" + name + "/files"
    req = requests.get(cflink)
    if(req.status_code == 200):
        timechecked = False
        soup = BeautifulSoup(req.text, "html.parser")
        for row in soup.findAll('table')[0].tbody.findAll("tr"):
            dlink = row.findAll('td')[1].contents
            uploaded = row.findAll('td')[3].contents
            gamever = row.findAll('td')[4].contents
            cur = BeautifulSoup(str(gamever), "html.parser").findAll("span")
            ver = cur[0].text
            if ver == gameversion:
                cur = BeautifulSoup(str(uploaded), "html.parser").findAll("abbr")
                modtime = cur[0]['data-epoch']  
                if modtime > time:
                    cur = BeautifulSoup(str(dlink), "html.parser").findAll("a")
                    link = cur[1]['href']
                    if download_file(curse + link + "/download"):
                        print "updated " + name
                        return modtime
                else:
                    print name + " is up to date"
                    return 0
        print "failed to find proper version for " + name
    else:
        print "failed updating " + name
        return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if not os.path.exists(folder):
            os.makedirs(folder)
        text = []
        for line in open(sys.argv[1], "r"):
            l = line.split(" ")
            name = l[0].strip()
            time = 0
            if len(l) == 2:
                time = l[1].strip()
            elif len(l) > 2:
                print "the line"
                print line
                print "is in an incorrect format"
                sys.exit(0)
            date = check_update(name, time)
            if date == 0:
                text.append(line)
            else:
                text.append(str(name) + " " + str(date) + "\n")
        f = open(sys.argv[1], "w")
        f.writelines(text)
    else:
        print "not enough args"
        print "usage python2 " + sys.argv[0] + " <mods.txt>"
