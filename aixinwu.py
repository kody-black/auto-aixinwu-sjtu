import json
import logging
import os
import pickle
import re
import time
from bs4 import BeautifulSoup
import requests
from config import account

AIXINWU_URL = "https://aixinwu.sjtu.edu.cn/index.php/login"
ULOGIN_URL = "https://jaccount.sjtu.edu.cn/jaccount/ulogin"
LOGGING_FILE = "aixinwu.log"
LAST_RESPONSE_HTML = "last_res.html"
COOKIE_FILE = "user.cookies"

def extract_login_days(response):
    patten = re.compile(r"您已连续登陆&nbsp;(\d+)&nbsp;天")
    login_info = patten.search(response.text)
    if login_info:
        print("连续登录天数：", login_info.group(1))
    else:
        print("登录天数未找到，请查看last_res.html文件检查登录结果")
        # 删除cookies文件
        os.remove(COOKIE_FILE)
        print("已删除cookies文件，请重试")
    return login_info

def save_cookies(session, filename):
    with open(filename, 'wb') as f:
        pickle.dump(session.cookies, f)

def load_cookies(session, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            try:
                session.cookies.update(pickle.load(f))
            except:
                print("加载Cookie文件失败")
                return False
        print("成功加载Cookie文件")
        return True
    else:
        print("Cookie文件不存在")
        return False

def fetch_captcha(session, referer, uuid):
    captcha_url = f"https://jaccount.sjtu.edu.cn/jaccount/captcha?uuid={uuid}"
    response = session.get(captcha_url, headers={"Referer": referer})
    return response.content

def captcha_rec(captcha):
    files = {
        'file': ('captcha.jpg', open(captcha, 'rb'), 'image/jpeg')
    }
    req = requests.post('https://t.yctin.com/en/security/captcha-recognition/', files=files)
    text = req.text.strip()
    print("识别结果：", text)
    return text

def login_jaccount(session):
    response = session.get(AIXINWU_URL)
    login_url = re.search(r"URL=(.*)\"></head>", response.text).group(1)
    print("登录URL: ", login_url)
    response = session.get(login_url)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', string=re.compile('loginContext'))
    if script:
        # 使用正则表达式提取 loginContext 对象
        pattern = re.compile(r'var loginContext = ({.*?});', re.S)
        match = pattern.search(script.string)
        if match:
            login_context_js = match.group(1)
            # 将属性名修正为 JSON 格式（用双引号包围）
            login_context_js = re.sub(r'(?<!")(\b\w+\b)(?!"):', r'"\1":', login_context_js)

            try:
                # 解析 JSON 对象
                login_context = json.loads(login_context_js)
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
        else:
            print("loginContext pattern not found")
    else:
        print("Script containing loginContext not found")

    referer = response.url
    captcha_image = fetch_captcha(session, referer, login_context["uuid"])

    with open("captcha.jpg", "wb") as f:
        f.write(captcha_image)

    captcha_code = captcha_rec("captcha.jpg")

    login_context["user"] = account["username"]
    login_context["pass"] = account["password"]
    login_context["captcha"] = captcha_code
    session.post(ULOGIN_URL, data=login_context)
    
    save_cookies(session, COOKIE_FILE)
    return session


if __name__ == "__main__":
    logging.basicConfig(filename=LOGGING_FILE, level='DEBUG')
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logging.info("=============== Log Started at " + date + "===============")
    
    # 创建会话
    session = requests.Session()
    # 设置头部信息
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.57 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9"
    })

    if load_cookies(session, COOKIE_FILE) == False:
        session = login_jaccount(session)
        print(session.cookies)
        logging.info("=============== Login successfully at %s ===============" % date)
    else:
        print(session.cookies)
        logging.info("=============== Login by cookies successfully at %s ===============" % date)

    response = session.get(AIXINWU_URL)
    print(session.cookies)
    login_days_info = extract_login_days(response)
    
    # 登录结果保存在文件ans.log中
    with open(LAST_RESPONSE_HTML, "w", encoding='utf-8') as f:
        f.write(response.text)
