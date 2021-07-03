from zh2en import *
from en2zh import *
import time

with open("content.txt", "r") as f:
    # 读取待翻译内容
    data = f.readlines()
    f.close()

article = ""
count = 100  # 翻译次数
length = len(data)

for word in data:
    word = word[:-1]
    for i in range(0, count):
        trans = zh_to_en(word)
        word = en_to_zh(trans)
        # 等待1s防止IP被封，百度的服务器或许可以删掉试试？
        time.sleep(1)
    article = article + word + "\r"
    print(length)
    length -= 1

with open("result.txt", "w") as f1:
    f1.write(article)
    f1.close()
