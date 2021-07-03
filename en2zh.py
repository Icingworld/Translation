import requests
from bs4 import BeautifulSoup
import re
import execjs

url_en2zh = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"

header_en2zh = {
    "Origin": "https://fanyi.baidu.com",
    "Host": "fanyi.baidu.com",
    "Cookie": "BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=85a5ak2524ah2h00lq1gdvm390r; H_PS_PSSID=34132_33763_34223_33848_34112_33607_34107_34134; PSINO=5; delPer=0; ab_sr=1.0.1_ZGMyNmVjZDhjZWFjZDI5NWU2YWVmMmEyYTViODg4MDA0MGE2Y2E5M2Q3YTljNTJhZjFhNzU1ODZmMzk4NjFiOTgxZTBhMTA2ZTk1YTVhNjhmOWZjNWVmODNlMjdiYTM3YjI1ZmVlYTA4MTQyYTYxYTI5MDJhYmRhZTNkNGNlZTNmYTM1NDE4ZmRmYzE0MWYzYmUwNDQxZDM3OWVkM2U2MzU2MDc4YzllNzUwNjNmN2JjMjU3NWEwYjYzMTE4ZjY4; ZD_ENTRY=baidu; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BCLID=10787079436579317709; BDSFRCVID=D5-OJexroG0YyvReYPWjUtYzyuweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKKL2OTHmPF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3aQ5rtKRTffjrnhPF3yTJbXP6-hnjy3bRkX4nv5xTF8tja5hr02JLWbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvX5Dg3-7LQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMQa_LWMT-MTryKKJwM4QCefTM3P6l5hFh2qofKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUXa59LUvLLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLK-oj-DDmj5LW3e; MAWEBCUID=web_qaUZfRBEfaNaIwhdpEVDHJvpHUbktOfqjkdVKqawPEBqsnetnf; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; REALTIME_TRANS_SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1625242260; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1625242260; __yjs_duid=1_2f12552af323060561597d8450410eb01621355169411; BDUSS=l2Tm8tZFdiOW5CdlEwcnFWWXN5M1pPekFBNXVjcDdTdHBTRzN0N3d2TXJjOHRnSVFBQUFBJCQAAAAAAAAAAAEAAAAzK6cYampqenc3NzkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACvmo2Ar5qNgZH; BAIDUID=4CD4D2435AC8CF736143CEB0CC625925:FG=1; BIDUPSID=4CD4D2435AC8CF736E5EFDF5361A68DE; PSTM=1621333163",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Referer": "https://fanyi.baidu.com/?aldtype=16047",
}


def en_to_zh(input_data):
    # 调用JS计算sign参数
    with open("BaiduJS.js") as f:
        js_data = f.read()
    sign = execjs.compile(js_data).call("e", input_data)

    request_key = {
        "from": "en",
        "to": "zh",
        "query": input_data,
        "transtype": "translang",
        "simple_means_flag": "3",
        "sign": sign,
        "token": "68076e07e4bbadc223a61c37453972e2",
        "domain": "common"
    }

    p = requests.post(url=url_en2zh, headers=header_en2zh, data=request_key)
    b = BeautifulSoup(p.content, "lxml")
    try:
        block = re.search('"dst":"[\'\"\\\A-Za-z0-9，。/？！;@#¥%&*（）.,、\\-\n\r\s]{0,}","prefixWrap"',str(b)).group(0)
    except AttributeError:
        print(b)  # 方便观察正则出错的地方
    content = block[7:-14]
    bytes_ = content.encode("utf8")
    result = bytes_.decode("unicode_escape")
    return result
