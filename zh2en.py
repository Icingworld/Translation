import requests
from bs4 import BeautifulSoup
import re
import execjs

url_zh2en = "https://fanyi.baidu.com/v2transapi?from=zh&to=en"

header_zh2en = {
    "Origin": "https://fanyi.baidu.com",
    "Host": "fanyi.baidu.com",
    "Cookie": "ab_sr=1.0.1_YjI1Yjk1ZDJkZTU1MjM2MTNkNDQ3MTQyZWYwMzc5M2M3M2Y2ZWMwOGY2NWM3NzlhMmFlNTc4NDgyYWNjNTc5ZGRlMzVlMjdmNzBmZGVkMmJhYTM2MzQ2OGNkMzg5YTYwYzU2ZGI5MzAxY2VkMDk4M2QyNWIxOGMzNGFjZWYwM2MyY2QzOTZlOWQwMTg2NDk1NDU5Zjc4NWU1ZmMzZjU4MQ==; MAWEBCUID=web_qaUZfRBEfaNaIwhdpEVDHJvpHUbktOfqjkdVKqawPEBqsnetnf; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=0g218l010k80010h5n1gdugd60q; H_PS_PSSID=34132_33763_34223_33848_34112_33607_34107_34134; PSINO=5; delPer=0; __yjs_st=2_NDBkZWVjY2M1NjVmM2M5MWMyMjhlODU2ZDhlZWFmNTE1NGM0MjdmZTllYzQ1YjY4YjEwNWY1MmQzODlkMjVkNmE0ZDU1MDU1NzY4ZjMwZDM3MzZkNDlkMjQyZjkxZjViZTE3YWU4NDAzY2U3ODRhNjIyNzUxNmI0MTBkMmQyNmViMGY4Y2ExYmU2MzZlODNmOGJmYzA5OGMxNTdkNDZmOGViYzMwMGYyNTJmNTZlYzFkYmFiYWI3YzYxZDg3MzlhODk4NTA2MTI5MjVkMjBkOWU1NjFmOGVkY2M0OTc2ZjZiMzgzMTA4ZjRmOWJmZjY3MjM3ODkyZDNjYTc3ZDUxZl83Xzg4NDk4MThi; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; REALTIME_TRANS_SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1625242260; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1625242260; BCLID=11038811863435978151; BDSFRCVID=K38OJexroG0YyxOeYNMqUtYzyuweG7bTDYLtOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKKL2OTHmPF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3aQ5rtKRTffjrnhPF3yTJbXP6-hnjy3bRkX4nv5xTF8tja5hr02JLWbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvX5Dg3-7LQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqC-BhILw3D; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; __yjs_duid=1_2f12552af323060561597d8450410eb01621355169411; BDUSS=l2Tm8tZFdiOW5CdlEwcnFWWXN5M1pPekFBNXVjcDdTdHBTRzN0N3d2TXJjOHRnSVFBQUFBJCQAAAAAAAAAAAEAAAAzK6cYampqenc3NzkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACvmo2Ar5qNgZH; BAIDUID=4CD4D2435AC8CF736143CEB0CC625925:FG=1; BIDUPSID=4CD4D2435AC8CF736E5EFDF5361A68DE; PSTM=1621333163",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Referer": "https://fanyi.baidu.com/?aldtype=16047",
}


def zh_to_en(input_data):
    # 调用JS计算sign参数
    with open("BaiduJS.js") as f:
        js_data = f.read()
    sign = execjs.compile(js_data).call("e", input_data)

    request_key = {
        "from": "zh",
        "to": "en",
        "query": input_data,
        "transtype": "translang",
        "simple_means_flag": "3",
        "sign": sign,
        "token": "68076e07e4bbadc223a61c37453972e2",
        "domain": "common"
    }

    p = requests.post(url=url_zh2en, headers=header_zh2en, data=request_key)
    b = BeautifulSoup(p.content, "lxml")
    try:
        block = re.search('"dst":"[\\\A-Za-z0-9!?,.;:；，。：（）！？/\\-@#$%^&*()\'\"\n\r\s]{0,}","prefixWrap"', str(b)).group(0)
    except AttributeError:
        print(b)
    content = block[7:-14]
    return content
