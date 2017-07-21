# coding:utf-8

import sys
import os.path
import urllib.request
import codecs
import re

class Threads:
    def __init__(self):
        self.replaceanker = re.compile(r'\<a\shref\=\"\/bbs\/read\.cgi\/[a-zA-Z]*\/\d*\/\d*\/(\d*)\"\starget\=\"\_blank\"\>')
        self.replaceReadCGItoRAWMode = re.compile(r'read\.cgi')

        self.result = '<body bgcolor="#EFEFEF">\n'

        self.idfirst = " ID:"
        self.namecolor = "<font color=\"#008800\"\>"
        self.namecolorclose = "</font>"
        self.jumpname = "<a id="
        self.jumpnameclose = ">"
        self.jumpnameclose2 = "</a>"
    
    def download(self, path, url):
        ReadorRaw = self.replaceReadCGItoRAWMode.search(url)
        if ReadorRaw:
            url = url.replace("read.cgi", "rawmode.cgi")
            te = os.path.exists(path)
        if not te:
            local_file, headers = urllib.request.urlretrieve(url, path)

    def openf(self, Fname):
        return codecs.open(Fname, 'r', 'euc-jp')

    def numlink(self, num):
        hikaku = int(num)
        if hikaku == 1:
            tmp = '<div id="' + num + '">' + '<a href="#' + num + '">' + num + self.jumpnameclose2 + ' '
        elif hikaku >= 2:
            tmp = "\n" + "<br><br><br>" + "<div id=\"" + num + "\">" + "<a href=\"#" + num + "\"" +  ">" + num + self.jumpnameclose2 +  " "
        return tmp

    def GetTextLineFromFile(self, filename):
        tmpf = self.openf(filename)
        tmplines = tmpf.readlines()
        getlines = len(tmplines)
        return getlines

    def ReturnThreadTitle(self):
        return self.result

    def SetThreadTitle(self, s):
        self.result = s

    def DatToHTML(self, filename, outname):
        count = 1
        f = self.openf(filename)
        for line in f:
            data = u"".join(line).split("<>")
            if count == 1:
                threadtitle = data[5] + "\n" + "<br><br>"
                self.result += threadtitle
                for i in range(6):
                    if i == 0:
                        self.result += "<html lang=ja><head></head><body>"
                        self.result += self.numlink(data[i])
                    elif i == 1:
                        tmp = data[i].replace("<b>", "</b>")
                        tmp = tmp.replace("</b>", "<b>", 1)
                        self.result += "名前：" +  self.namecolor + tmp + self.namecolorclose + " "
                    elif i == 2:
                        self.result += data[i] + " "
                    elif i == 3:
                        resultid = self.idfirst + data[6]
                        self.result += data[i] + resultid + "<br>"
                    elif i == 4:
                        m = self.replaceanker.search(data[i])
                        if m:
                            moto = m.group()
                            okikae = m.group(1)
                            replacestr = '<a href=\"#' + okikae + '">'
                            lastokikae = '#' + okikae
                            latest = data[i].replace(moto, replacestr)
                            self.result += latest + "\n</div>"
                        else:
                            self.result += data[i] + "\n</div>"
                        count = 2

            if count == 2:
                for n in range(5):
                    if n == 0:
                        self.result += self.numlink(data[n])
                    elif n == 1:
                        tmp = data[n].replace("<b>", "</b>")
                        tmp = tmp.replace("</b>", "<b>", 1)
                        self.result += "名前：" +  self.namecolor + tmp + self.namecolorclose + " "
                    elif n == 2:
                        self.result += data[n] + " "
                    elif n == 3:
                        resultid = self.idfirst + data[6]
                        self.result += data[n] + resultid + "<br>"
                    elif n == 4:
                        m = self.replaceanker.search(data[n])
                        if m:
                            moto = m.group()
                            okikae = m.group(1)
                            replacestr = '<a href=\"#' + okikae + '">'
                            lastokikae = '#' + okikae
                            latest = data[n].replace(moto, replacestr)
                            self.result += latest + "\n</div>"
                        else:
                            self.result += data[n] + "\n</div>"

        self.result += "</body>"

        count = 3
        f.close()

        lastresult = self.result.replace("<br>", "<br>\n")
        lastresult += "</body></html>"

        self.WriteFile(lastresult, outname)

    def WriteFile(self, text, outname):
        o = codecs.open(outname, "w", "utf-8")
        o.write(text)
        o.close()