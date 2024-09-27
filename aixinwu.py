import logging
from DrissionPage import ChromiumOptions, WebPage
import requests
from config import *

logging.basicConfig(level=logging.INFO)

AIXINWU_URL = "https://aixinwu.sjtu.edu.cn/user/order"
ULOGIN_URL = "https://jaccount.sjtu.edu.cn/jaccount/ulogin"
LAST_RESPONSE_HTML = "last_res"
CAPTCHA_URL = "https://jaccount.sjtu.edu.cn/jaccount/captcha"

def captcha_rec(img):
    try:
        files = {
            'file': ('captcha.jpg', img, 'image/jpeg')
        }
        req = requests.post('https://t.yctin.com/en/security/captcha-recognition/', files=files)
        text = req.text.strip()
        logging.info(f"验证码识别结果：{text}")
        return text
    except Exception as e:
        logging.error(f"验证码识别失败: {e}")
        return None

def login(page):
    username = page.ele('@id=input-login-user')
    username.input(USERNAME)
    password = page.ele('@id=input-login-pass')
    password.input(PASSWORD)
    attempts = 0
    while '统一身份认证' in page.title and attempts < 5:
        attempts += 1
        if attempts >= 5:
            logging.error("尝试失败次数过多，请检查密码或稍后再试")
            page.save(name=LAST_RESPONSE_HTML)
            page.close()
            exit(1)
        try:
            captcha_input = page.ele('@id=input-login-captcha')
            captcha_img = page.ele('@id=captcha-img')
            img = captcha_img.get_screenshot(as_bytes=True, scroll_to_center=True)
            with open('captcha.jpg', 'wb') as f:
                f.write(img)
            captcha_text = captcha_rec(img)
            if captcha_text is None:
                page.refresh()
                logging.info("识别失败,正在重试")
                continue
            captcha_input.input(captcha_text,clear=True)
            submit_btn = page.ele('@id=submit-password-button')
            submit_btn.click()
            page.wait(0.4)
        except Exception as e:
            logging.error(f"登录失败，第 {attempts} 次尝试: {e}")
            page.refresh()
            continue

if __name__ == "__main__":
    do = ChromiumOptions().set_paths(local_port=10000, user_data_path=r'.\data0', browser_path=BROWSER_PATH)
    if HEADLESS:
        do.headless()
    page = WebPage(chromium_options=do)
    page.get(AIXINWU_URL)
    page.wait(0.4)
    if "403" in page.title:
        login_btn = page.ele('.:ant-btn-primary')
        login_btn.click()
        page.wait(0.45)
        login(page)
    try:
        page.ele('.:anticon anticon-user').click()
        page.wait(0.5)
        label = page.ele('@text():已连续登录')
        logging.info(label.text)
    except Exception as e:
        logging.error(f"登录天数未找到: {e}")

    page.save(name=LAST_RESPONSE_HTML)
    logging.info(f"可查看 {LAST_RESPONSE_HTML}.mhtml 文件检查登录结果")
    page.close()