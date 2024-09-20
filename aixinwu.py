import json
import os
import pickle
import re
from DrissionPage import ChromiumOptions, WebPage
import requests
from config import *

AIXINWU_URL = "https://aixinwu.sjtu.edu.cn/user/order"
ULOGIN_URL = "https://jaccount.sjtu.edu.cn/jaccount/ulogin"
LAST_RESPONSE_HTML = "last_res"
CAPTCHA_URL = "https://jaccount.sjtu.edu.cn/jaccount/captcha"

def captcha_rec(captcha):
    try:
        files = {
            'file': ('captcha.jpg', open(captcha, 'rb'), 'image/jpeg')
        }
        req = requests.post('https://t.yctin.com/en/security/captcha-recognition/', files=files)
        text = req.text.strip()
        print("验证码识别结果：", text)
        return text
    except Exception as e:
        print(e)
        return None

do = ChromiumOptions().set_paths(local_port=10000, user_data_path=r'.\data0', browser_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
# do.headless()
page = WebPage(chromium_options=do)
page.get(AIXINWU_URL)

attempts = 0
while '403' in page.title and attempts < 5:
    attempts += 1
    login_btn = page.ele('.:ant-btn-primary')
    login_btn.click()

    username = page.ele('@id=input-login-user')
    username.input(USERNAME)
    password = page.ele('@id=input-login-pass')
    password.input(PASSWORD)
    captcha_input = page.ele('@id=input-login-captcha')

    page.wait(1)
    captcha_img = page.ele('@id=captcha-img')
    img = captcha_img.get_screenshot(as_bytes=True, scroll_to_center=True)
    # # img从str变为bytes
    # img = img.encode()
    with open('captcha.jpg', 'wb') as f:
        f.write(img)

    captcha_text = captcha_rec('captcha.jpg')
    if captcha_text is None:
        print("识别失败")
        continue
    captcha_input.input(captcha_text)
    submit_btn = page.ele('@id=submit-password-button')
    submit_btn.click()

if attempts >= 5:
    print("尝试失败次数过多，请稍后再试")
    page.save(name=LAST_RESPONSE_HTML)
    exit(1)

page.save(name=LAST_RESPONSE_HTML)
try:
    page.ele('.:anticon anticon-user').click()
    label = page.ele('@text():已连续登录')
    print(label.text)
except Exception as e:
    print(e)
    print("登录天数未找到，请查看last_res.mhtml文件检查登录结果")