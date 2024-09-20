import os
import pickle
from DrissionPage import ChromiumOptions, WebPage

AIXINWU_URL = "https://aixinwu.sjtu.edu.cn/user/order"
LAST_RESPONSE_HTML = "last_res.html"
COOKIE_FILE = "user.cookies"


def save_cookies():
    # 显示cookie
    print(page.cookies())
    # 显示cookie类型
    print(type(page.cookies())) 
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(page.cookies(), f)


if __name__ == "__main__":
    do = ChromiumOptions().set_paths(local_port=10000, user_data_path=r'.\data0', browser_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
    except FileNotFoundError:
        cookies = None

    
    if cookies:
        do.headless = True
        page = WebPage(chromium_options=do)
        page.set.cookies(cookies)
    else:
        page = WebPage(chromium_options=do)

    page.get(AIXINWU_URL)
    while '我的订单' not in page.title:
        print("未成功登录，请手动在浏览器中登录")
        input("完成登录后按回车键继续")
        page.get(AIXINWU_URL)
        save_cookies()
    else:
        print("已成功登录")

    with open(LAST_RESPONSE_HTML, "w", encoding='utf-8') as f:
            f.write(page.html)

    try:
        label = page.ele('@text():已连续登录')
        print(label.text)
    except Exception as e:
        print(e)
        print("登录天数未找到，请查看last_res.html文件检查登录结果")
        # 删除cookies文件
        os.remove(COOKIE_FILE)
        print("已删除cookies文件，请重试")
