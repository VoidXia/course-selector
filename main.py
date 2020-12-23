# -*- coding: UTF-8 -*-
course_name = ""
course_keyword1 = ""
course_keyword2 = ""
course_original_id = ""

corid = 1
delaytime = 5

from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getcookie_inte import getcookie
import requests
import pytesseract
import time
import datetime
import os
import sys

from PIL import Image, ImageEnhance
import json

syslen = len(sys.argv)

if (syslen >= 2):
    course_name = sys.argv[1]
    print("CTYPE: ", corid, end="\n")
if (syslen >= 3):
    course_name = sys.argv[2]
    print("COURSE: ", course_name, end="\n")
if (syslen >= 4):
    course_keyword1 = sys.argv[3]
    print("KEYWORD1: ", course_keyword1, end="\n")
if (syslen >= 5):
    course_keyword2 = sys.argv[4]
    print("KEYWORD2: ", course_keyword2, end="\n")

print("DELAYTIME:", delaytime)
print()
#tongshiflag = 1
'''if("PU" in course_name):
    tongshiflag = 1
    corid = 6
if("tongshi"in course_keyword1 or "tongshi"in course_keyword2):
    tongshiflag = 1
    corid = 6
if("tongxuan"in course_keyword1 or "tongxuan"in course_keyword2):
    tongshiflag = 1
    corid = 7'''

corid = str(corid)

option = webdriver.ChromeOptions()
option.add_argument('headless')

chrome_driver = webdriver.Chrome(executable_path="./DRIVERS/chromedriver",
                                 options=option)
#chrome_driver = webdriver.Chrome(executable_path="./DRIVERS/chromedriver")
chrome_driver.get("https://i.sjtu.edu.cn/")

chrome_driver.set_window_position(x=0, y=0)
chrome_driver.set_window_size(1200, 1080)
chrome_driver.delete_all_cookies()
time.sleep(0.2)

the_id = ""


def pressButton(the_id_):  # ELECT
    button = chrome_driver.find_elements_by_xpath('//*[@id="btn-xk-' + the_id +
                                                  '"]')  ###  the_id_ TODO
    #button = element.find_elements(By.CLASS_NAME, 'an')
    if (len(button) > 0):
        button[0].click()
        print("\n\n", course_name,
              "  ############  BUTTON PRESSED!!!  ############  \n\n")
    else:
        print("\n", course_name,
              "  ############  BUTTON NOT FOUND.   ############  \n")
    #classes[len(classes)-1].click()


time_start = time.time()
time_real_start = time.time()


def stopwatch():
    global time_start
    time_end = time.time()
    if (0):
        print('time cost:', time_end - time_start, 's\n')
    time_start = time.time()
    #print(datetime.datetime.now())


def check_url():
    while ("xsxk" not in chrome_driver.current_url):
        #while(0):
        print("WRONG URL")
        chrome_driver.delete_all_cookies()
        if (getcookie() == 7):
            print("WAITING FOR COOKIE...")
            time.sleep(9)
        with open("./cookie.txt", 'rb') as cookief:
            cookie = json.load(cookief)
            for c in cookie:
                chrome_driver.add_cookie(c)
        chrome_driver.get(
            "https://i.sjtu.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default"
        )
        time.sleep(0.5)


with open("./cookie.txt", 'rb') as cookief:
    cookie = json.load(cookief)
    for c in cookie:
        chrome_driver.add_cookie(c)
time.sleep(0.2)

chrome_driver.get(
    "https://i.sjtu.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default"
)
time.sleep(0.08)


def refresh(str):
    chrome_driver.refresh()
    print("\nREFRESHED DUE TO:  ", str)


def find_and_click_tab():
    navtab = chrome_driver.find_element_by_xpath('//*[@id="nav_tab"]/li[' +
                                                 corid + ']/a')
    navtab.click()


def find_and_click_query(ss=1):
    queryf = []
    searchInputf = []
    while (len(queryf) == 0 or len(searchInputf) == 0):
        queryf = chrome_driver.find_elements_by_name("query")
        searchInputf = chrome_driver.find_elements_by_name("searchInput")
        #print(queryf)
    while (len(queryf) == 0 or len(searchInputf) == 0):
        refresh("NO QUERY BOX.")
        queryf = chrome_driver.find_elements_by_name("query")
        searchInputf = chrome_driver.find_elements_by_name("searchInput")
        #print(queryf)
    print("FOUND QUERY BOX.")
    query = queryf[0]
    searchInput = searchInputf[0]

    searchInput.send_keys(course_name)

    ############

    stopwatch()
    if (ss == 1):
        query.click()
    print("QUERY BTN CLICKED")


def find_and_click_ok():
    btn_ok = chrome_driver.find_elements_by_id("btn_ok")
    if (len(btn_ok) > 0):
        time.sleep(0.5)
        alertj = chrome_driver.find_elements_by_class_name(
            "modal-body")[0].text
        print(alertj)
        btn_ok[0].click()
        if ("已无余" in alertj):
            return 1
        if ("最多可选" in alertj):
            return 2
        return 9
    return 0


def CANCELCOURSE():
    print("\n\nCANCEL original COURSE!\n\n")
    button = chrome_driver.find_elements_by_xpath('//*[@id="tr_' +
                                                  course_original_id +
                                                  '"]/td[23]/button')
    #button = element.find_elements(By.CLASS_NAME, 'an')
    print(len(button))
    if (len(button) > 0):
        button[0].click()
        time.sleep(0.5)
        btn_confirm = chrome_driver.find_elements_by_id("btn_confirm")
        btn_confirm[0].click()
        print(
            "\n\n", course_name,
            "  ############  BUTTON PRESSED!!!  COURSE CANCELLED!!!!!!!!!!!!!!!!############  \n\n"
        )
    else:
        print("\n", course_name,
              "  ############  BUTTON NOT FOUND.   ############  \n")
    #os._exit()


counter = 0

if (1):

    check_url()
    find_and_click_ok()

    time.sleep(0.1)

    ### GOTO_FLAG
    nodata = chrome_driver.find_elements_by_class_name("nodata")
    if (len(nodata) > 0):
        print(nodata[0].text)
        while ("管理员" in nodata[0].text):
            refresh(course_name + ": NOT OPENED YET.")
            check_url()
            time.sleep(delaytime)  ############  ##########
            counter = counter + 1
            print(datetime.datetime.now(), "   ", counter, end=": ")
            stopwatch()
            nodata = chrome_driver.find_elements_by_class_name("nodata")

    time_real_start = time.time()
    print("\nInitialize ", end="")
    stopwatch()
    print()
    #if(tongshiflag):
    find_and_click_query(0)
    find_and_click_tab()
    #else:
    #    find_and_click_query()

    find_and_click_ok()
    check_url()

    print("PHASE1")
    time.sleep(1)

    stopwatch()
    flag = 0
    length = 0
    course_text = ""
    course_splitted = ""
    time.sleep(0.05)
    lenclasses = 0
    sad_counter = 0
    #print(chrome_driver.find_elements_by_xpath("//p[contains(text(),'李成林')]"))
    #classes = chrome_driver.find_elements_by_class_name("body_tr")
    #lenclasses = len(classes)
    while (flag != 1):
        '''
        flag =  1 : Selected!
                2 : NOT OPEN
                3 : FULL
                0 : NOTHING DONE
        '''

        check_url()
        if (flag == 3):

            time.sleep(delaytime)
            print()
            print(datetime.datetime.now())
            #if(tongshiflag):
            find_and_click_tab()
            print("TAB CLICKED")
            time.sleep(1.2)
            '''else:
                refresh("STUPID")
                time.sleep(2)
                find_and_click_query()
            '''

            #find_and_click_query()

            find_and_click_ok()

            #time.sleep(0.1)

            stopwatch()
            length = 0
            course_text = ""
            course_splitted = ""
            time.sleep(0.05)
            lenclasses = 0

            classes = chrome_driver.find_elements_by_class_name("body_tr")
            lenclasses = len(classes)
            flag = 0

        if (flag == 2):
            nodata = chrome_driver.find_elements_by_class_name("nodata")
            if (len(nodata) > 0):
                print(nodata[0].text)
                while ("管理员" in nodata[0].text):
                    refresh(course_name + ": NOT OPENED YET.")
                    check_url()
                    time.sleep(delaytime)  ############  ##########
                    counter = counter + 1
                    print(datetime.datetime.now(),
                          "   ",
                          counter,
                          end=": [2] :")
                    stopwatch()
            find_and_click_query()
            flag = 0
        classes = chrome_driver.find_elements_by_class_name("body_tr")
        lenclasses = len(classes)
        #print(lenclasses)

        if (lenclasses == 0):
            #time.sleep(5)
            refresh("NO SUCH CLASS AVAILABLE:  " + course_name)
            sad_counter = sad_counter + 1
            if (sad_counter == 10):
                break
            flag = 2
            ###goto###
        print("NOW SEARCHING COURSES")
        stopwatch()
        i = 0
        if (course_original_id == ""):
            for i in range(lenclasses):
                course_text = classes[i].text
                if ("退选" in course_text):
                    course_original_id = classes[i].get_attribute("id")[3:]
                    print("GET ORIGINAL ID:", course_original_id)
        for i in range(lenclasses):
            course_text = classes[i].text
            course_splitted = course_text.split()
            length = len(course_splitted)
            #print(length)
            stopwatch()

            #print("IIIIIIIIIforward    ",i,lenclasses)

            #print(course_text)
            #print("已满" not in course_text)
            if ((course_keyword1 in course_text)
                    and (course_keyword2 in course_text)):
                #OROROROR

                #print("TEXXXXXXXXT:",course_text)

                print("GOT A MATCH!")
                #print(course_splitted,"")

                if ("退选" in course_text):
                    print(
                        "\n", course_name,
                        "  ############  Already selected.  ############  \n")
                    flag = 1
                    break
                #print(classes[i].text)

                the_id = classes[i].get_attribute("id")[3:]
                the_jxb_id = chrome_driver.find_elements_by_id("do_" +
                                                               the_id)[0].text

                if ("已满" in course_text):
                    flag = 3
                    print("GET TARGETED ID:", the_id)
                    print("CLASS IS FULL! RETRYING...")
                    #break
                    continue
                elif ("/" in course_text):
                    CANCELCOURSE()

                #print(classes[i])######## print the webElement of the corresponding course

                print(course_name, "\nTHE VERY ID:  ", the_id, end="\n")
                print("SELECT ID:", the_jxb_id, end="\n")
                #stopwatch()

                #while(1):
                if (1):
                    try:
                    
# The last part will be released once this period of course selection ends.
