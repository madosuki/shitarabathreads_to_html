# coding:utf-8

import sys
import os.path
import urllib.request
import codecs
import re

argvs = sys.argv
argc = len(argvs)

filename = "tinput.html"

count = 1

data = ""

result = '<body bgcolor="#EFEFEF">\n'

idfirst = " ID:"
namecolor = "<font color=\"#008800\"\>"
namecolorclose = "</font>"
jumpname = "<a id="
jumpnameclose = ">"
jumpnameclose2 = "</a>"

numline = ""

#pattern = re.compile(r'ttps?://[\w/:%#\$&\?\(\)~\.=\+\-]+')
replaceanker = re.compile(r'\<a\shref\=\"\/bbs\/read\.cgi\/[a-zA-Z]*\/\d*\/\d*\/(\d*)\"\starget\=\"\_blank\"\>') #返信アンカのリンクをHTML内のレス番号に飛ぶようにする処理に使う正規表現
replaceReadCGItoRAWMode = re.compile(r'read\.cgi') #"rawmode.cgiではなくread.cgiだった場合にrawmodeへ置き換える際に使う"
#replaceanker = re.compile(r'\<a\shref\=\"/bbs/read\.cgi/[a-zA-Z]*/\d*/\d*/(\d*)\"\starget\=\"\_blank\"\>')

def download(s):
    url = argvs[1]
    ReadorRaw = replaceReadCGItoRAWMode.search(url)
    if ReadorRaw:
        url = url.replace("read.cgi", "rawmode.cgi")
    te = os.path.exists(s)
    if not te:
        local_file, headers = urllib.request.urlretrieve(url, s)

def openf(Fname):
    return codecs.open(Fname, 'r', 'euc-jp')

def numlink(num):
    hikaku = int(num)
    if hikaku == 1:
        tmp = '<div id="' + num + '">' + '<a href="#' + num + '">' + num + jumpnameclose2 + ' '
    elif hikaku >= 2:
        tmp = "\n" + "<br><br><br>" + "<div id=\"" + num + "\">" + "<a href=\"#" + num + "\"" +  ">" + num + jumpnameclose2 +  " "
    return tmp

def fline():
    tmpf = openf(filename)
    tmplines = tmpf.readlines()
    getlines = len(tmplines)
    return getlines

if argc >= 2:
    download(filename)
else:
    print("引数がありません")
    exit()

#f = codecs.open('tinput.html', 'r', 'euc-jp')

f = openf(filename)

#/bbs/read.cgi/otaku/15956/1472906650/2

for line in f:
    #data += line.split("<>")
    data = u"".join(line).split("<>")
    if count == 1:
        threadtitle = data[5] + "\n" + "<br><br>"
        result += threadtitle
        for i in range(6):
            if i == 0:
                #result += "<div id=\"" + data[i] + "\">" "<a href=\"#" + data[i] + "\"" +  ">" + data[i] + jumpnameclose2 + "</a>" + " "
                result += "<html lang=ja><head></head><body>"
                result += numlink(data[i])
            elif i == 1:
                tmp = data[i].replace("<b>", "</b>")
                tmp = tmp.replace("</b>", "<b>", 1)
                result += "名前：" +  namecolor + tmp + namecolorclose + " "
            elif i == 2:
                result += data[i] + " "
            elif i == 3:
                resultid = idfirst + data[6]
                result += data[i] + resultid + "<br>"
            elif i == 4:
                m = replaceanker.search(data[i])
                if m:
                    moto = m.group()
                    okikae = m.group(1)
                    replacestr = '<a href=\"#' + okikae + '">'
                    lastokikae = '#' + okikae
                    latest = data[i].replace(moto, replacestr)
                    result += latest + "\n</div>"
                else:
                    result += data[i] + "\n</div>"
                count = 2
            #elif i == 5:
            #    threadtitle = "<br><br><br><br>" + data[i] + "<br>"
            #    result += threadtitle
            #    count = 2
    if count == 2:
        for n in range(5):
            if n == 0:
                #result += "\r\n" + "<br><br><br>" + "<div id=\"" + data[n] + "\">" + "<a href=\"#" + data[n] + "\"" +  ">" + data[n] + jumpnameclose2 + "</a>" + " "
                result += numlink(data[n])
            elif n == 1:
                tmp = data[n].replace("<b>", "</b>")
                tmp = tmp.replace("</b>", "<b>", 1)
                result += "名前：" +  namecolor + tmp + namecolorclose + " "
            elif n == 2:
                result += data[n] + " "
            elif n == 3:
                resultid = idfirst + data[6]
                result += data[n] + resultid + "<br>"
            elif n == 4:
                m = replaceanker.search(data[n])
                if m:
                    moto = m.group()
                    okikae = m.group(1)
                    replacestr = '<a href=\"#' + okikae + '">'
                    lastokikae = '#' + okikae
                    latest = data[n].replace(moto, replacestr)
                    result += latest + "\n</div>"
                else:
                    result += data[n] + "\n</div>"

#data = "".join(str(e) for e in f.readlines())
result += "</body>"

count = 3
f.close()


lastresult = result.replace("<br>", "<br>\n")
lastresult += "</body></html>"
o = codecs.open("o.html", "w", "utf-8")
o.write(lastresult)
o.close()

numline = fline()
