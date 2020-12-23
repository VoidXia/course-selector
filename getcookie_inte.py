# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pytesseract
import time
import datetime
import os
import re
import uuid
import getpass

from PIL import Image, ImageEnhance
import json

with open('pwd.txt', 'r') as tmp:
    pwd = str(tmp.read())

#chrome_driver.get("https://i.sjtu.edu.cn/jaccountlogin")

#chrome_driver.delete_all_cookies()


def getCaptcha(captcha_url, cookies, params):  # 获取验证码

    response = requests.get(captcha_url, cookies=cookies, params=params)
    with open('img.jpeg', 'wb+') as f:
        f.writelines(response)
    image = Image.open('img.jpeg')
    image = image.convert('L')
    image = ImageEnhance.Contrast(image)
    image = image.enhance(3)
    image2 = Image.new('RGB', (150, 60), (255, 255, 255))
    image2.paste(image.copy(), (25, 10))
    image2.save("img2.jpeg")
    code = pytesseract.image_to_string(image2)
    code.replace(" ", "")
    return code


def getcookie():

    with open('cookieupdtime.txt', 'r') as timef:
        if (float(time.time()) - float(timef.read()) < 30):
            return 7

    with open('cookieupdtime.txt', 'w') as timefw:
        timefw.write(str(time.time()))

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    chrome_driver = webdriver.Chrome("./DRIVERS/chromedriver", options=option)

    chrome_driver.get("http://i.sjtu.edu.cn")
    with open('cookie.txt', 'r') as cookieread:
        cookie = json.load(cookieread)
        for c in cookie:
            chrome_driver.add_cookie(c)

    chrome_driver.get("http://i.sjtu.edu.cn/jaccountlogin")
    #chrome_driver.get("http://my.sjtu.edu.cn/")

    while (("jaccount" in chrome_driver.current_url)):  # 防止验证码识别错误，重复尝试。
        cookies = chrome_driver.get_cookies()
        cookies = {i["name"]: i["value"] for i in cookies}
        uuid = chrome_driver.find_element_by_xpath(
            '//form/input[@name="uuid"]')
        params = {'uuid': uuid.get_attribute('value')}

        code = ""
        while (code == ""):
            code = getCaptcha("https://jaccount.sjtu.edu.cn/jaccount/captcha",
                              cookies, params)
            print("\ncode =", code, end="")
            time.sleep(0.03)

        input_user = chrome_driver.find_element_by_id('user')
        input_user.send_keys("xia.xh")
        input_pass = chrome_driver.find_element_by_id('pass')
        input_pass.send_keys(pwd)
        input_code = chrome_driver.find_element_by_id('captcha')
        input_code.send_keys(code)
        #input_code.send_keys(Keys.ENTER)
        # print(chrome_driver.current_url)
        time.sleep(0.03)

    if (json.dumps(chrome_driver.get_cookies()) != []):
        with open('cookie.txt', 'w') as cookiefw:
            cookiefw.write(json.dumps(chrome_driver.get_cookies()))
            print(json.dumps(chrome_driver.get_cookies()))

    chrome_driver.close()

    print("Succeed.")


if __name__ == '__main__':  # 主程序
    getcookie()

# print ("".join(cookies))
