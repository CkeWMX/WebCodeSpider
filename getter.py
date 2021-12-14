"""
Powered by : 九极实验室
Name：网站前端源码获取
"""
import os
import requesttool


# 替换内容
def replaceScriptContent(url,path):
    rebuildIndex = requesttool.rebuildDocument(url.split("//")[1])
    lines = rebuildIndex.getLines(path)
    soup = rebuildIndex.getBS(lines)

    for js in soup.select("script"):
        try:
            jsattrs = js.attrs['src'].split("/")[-1]
            js.attrs['src'] = "js/" + jsattrs
        except:
            KeyError
    print(os.getcwd())
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    url = "https://www.biubiu001.com"
    getter = requesttool.WebCodeGetter(url)
    # 创建目录 抓取前端源码
    getter.allOperateGetCode()
    index = requesttool.rebuildDocument(url.split("//")[1])
    line = index.getIndexContent()
    soup = index.getBS(line)
    # 修改JS为本地路径
    for js in soup.select("script"):
        try:
            jsattrs = js.attrs['src'].split("/")[-1]
            js.attrs['src'] = "js/" + jsattrs
        except:
            KeyError
            # 修改CSS为本地路径
    for cssLink in soup.find_all(attrs={"rel": "stylesheet"}):
        try:
            cssattrs = cssLink.attrs["href"].split("/")[-1]
            cssLink.attrs["href"] = "css/" + cssattrs
            print(cssLink.attrs["href"])
        except:
            KeyError
    # 修改图片资源为本地路径
    for img in soup.select("img"):
        try:
            imgAttr = img.attrs['src'].split("/")[-1]
            if "jpg" in imgAttr or "png" in imgAttr:
                img.attrs['src'] = "assets/" + imgAttr
                print(img.attrs['src'])
        except:KeyError

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))


