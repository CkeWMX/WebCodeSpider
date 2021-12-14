"""
Powered by : 九极实验室
"""
import requests
from bs4 import BeautifulSoup
import os


class WebCodeGetter:
    url = ""
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.111'
    }

    def __init__(self, u):
        self.url = u

    # 获取网站源码
    def getWebCode(self):
        code = requests.get(self.url, headers=self.header).text
        return code

    # BeautifulSoup对象
    @property
    def getBS(self):
        code = self.getWebCode()
        soup = BeautifulSoup(code, "lxml")
        return soup

    # 获取CSS层叠样式表
    def getCssScriptUrl(self):
        soup = self.getBS
        CssScriptList = []
        for cssLink in soup.find_all(attrs={"rel": "stylesheet"}):
            CssScriptList.append(cssLink)
        return CssScriptList

    def JsCode(self):
        soup = self.getBS
        JsList = []
        for jsLink in soup.select("script"):
            try:
                # print(jsLink.attrs["src"])
                code = requests.get(jsLink.attrs["src"], headers=self.header)
                return code
            except:
                KeyError

    # 获取JAVASCript脚本内容
    def getJsCode(self):
        soup = self.getBS
        JsList = []
        for jsLink in soup.select("script"):
            try:
                # print(jsLink.attrs["src"])
                if "http" in jsLink.attrs["src"]:
                    code = requests.get(jsLink.attrs["src"], headers=self.header).text
                    with open(self.url.split("//")[1] + "/js/" + jsLink.attrs["src"].split("/")[-1], "w",
                              encoding="utf-8") as f:
                        f.write(code)
            except:
                KeyError

    # 获取CSS层叠样式表内容
    def getCssScriptCode(self):
        cssList = self.getCssScriptUrl()
        for csslist in cssList:
            if "http" in csslist.attrs["href"]:
                code = requests.get(csslist.attrs["href"], headers=self.header).text
                with open(self.url.split("//")[1] + "/css/" + csslist.attrs["href"].split("/")[-1], "w",
                          encoding="utf-8") as f:
                    f.write(code)

    # 获取所有静态图片资源
    def getImageSource(self):
        soup = self.getBS
        for img in soup.select("img"):
            try:
                with open(self.url.split("//")[1] + "/assets/" + img.attrs["src"].split("/")[-1], "wb") as f:
                    f.write(requests.get(img.attrs['src'], headers=self.header).content)
            except:KeyError

    # 文件操作
    def fileOS(self, dirname):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
            os.chdir(dirname)
            os.mkdir("css")
            os.mkdir("js")
            os.mkdir("assets")
        else:
            code = self.getWebCode()
            with open(self.url.split("//")[1] + "/" + "index.html", "w", encoding="utf-8") as f:
                f.write(code)

    # 资源获取整合
    def allOperateGetCode(self):
        self.fileOS(self.url.split("//")[1])
        self.getImageSource()
        self.getCssScriptCode()
        self.getJsCode()


# 文档修改类
class rebuildDocument():
    # 工作目录
    workPath = ""

    def __init__(self, workPath):
        self.workPath = workPath

    def getBS(self, code):
        soup = BeautifulSoup(code, "lxml")
        return soup

    # 读取Index
    def getIndexContent(self):
        os.chdir(self.workPath)
        if os.path.split(os.getcwd())[-1] == self.workPath:
            with open("index.html", "r+", encoding="utf-8") as f:
                line = f.read()
        else:
            os.chdir(self.workPath)
        return line


