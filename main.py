# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:/selenium_test"
# https://dxpx.uestc.edu.cn/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def address_pause():
    """处理视频暂停问题"""
    if wd.find_element(By.CSS_SELECTOR, '#wrapper > div > div.plyr__controls > button:nth-child(1)').get_attribute(
            "aria-label") == "Play":
        wd.find_element(By.CSS_SELECTOR, '#wrapper > div > div.plyr__controls > button:nth-child(1)').send_keys(
            Keys.ENTER)
        print("检测到视频暂停,继续播放")


def remove_blank():
    """更改属性target为'_self'"""
    js = 'var items = document.getElementsByTagName("a");for (var i = 0; i < items.length; i++) {var tmp = items[' \
         'i];tmp.target="_self";} '
    wd.execute_script(js)


def manage(j):
    """处理视频"""
    necessary = wd.find_elements(By.CSS_SELECTOR,
                                 'body > div > div.w1150 > div.wrap_right > div.lesson1_cont.q_lesson1_cont > '
                                 'div.lesson1_lists > ul > li')  # 必修的课程列表
    necessary[j].find_element(By.CSS_SELECTOR, 'h2 a').send_keys(Keys.ENTER)  # 此后进入视频
    time.sleep(3)
    little_one = wd.find_elements(By.CSS_SELECTOR, 'a[style]')  # 侧边栏的课程列表
    length_little_one = len(little_one)
    index = 1  # 第几个视频
    print("成功加载侧边栏的课程列表,一共{}个视频".format(length_little_one))
    for k in range(length_little_one):
        little_one = wd.find_elements(By.CSS_SELECTOR, 'a[style]')  # 侧边栏的课程列表
        print("正在播放第{}个视频，一共{}个".format(index, length_little_one))
        if "red" in little_one[k].get_attribute("style"):
            print("视频{}播放完成,即将播放下一个视频".format(index))
            index += 1
            continue
        little_one[k].send_keys(Keys.ENTER)
        while True:
            print("剩余时间:" + wd.find_element(By.CSS_SELECTOR, 'div[aria-label="Current time"]').get_attribute(
                "innerText").replace('-', ''))
            address_pause()
            time.sleep(3)
            if wd.find_element(By.CSS_SELECTOR, 'div[aria-label="Current time"]').get_attribute(
                    "innerText").replace('-', '') == "00:00":
                print('播放完成,点击按钮"我知道了"')
                break
        index += 1


# selenium预处理
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
wd = webdriver.Chrome(service=Service('chromedriver.exe'), options=option)
wd.implicitly_wait(3)  # 隐式等待

study_list = wd.find_elements(By.CSS_SELECTOR, 'a.study')  # 按钮'开始学习'的列表
length_study_list = len(study_list)  # 一共几门课
index_study_list = 1
for i in range(length_study_list):
    study_list = wd.find_elements(By.CSS_SELECTOR, 'a.study')  # 按钮'开始学习'的列表
    if index_study_list == 0 or index_study_list == 1:
        index_study_list += 1
        continue
    study_list[i].send_keys(Keys.ENTER)  # 点击按钮'开始学习'
    wd.find_element(By.CSS_SELECTOR,
                    'body > div > div.w1150 > div.wrap_right > div.lesson1_cont.q_lesson1_cont > div.lesson1_title > '
                    'div > a:nth-child(2)').send_keys(
        Keys.ENTER)  # 点击‘按钮’必修
    necessary_list = wd.find_elements(By.CSS_SELECTOR,
                                      'body > div > div.w1150 > div.wrap_right > div.lesson1_cont.q_lesson1_cont > '
                                      'div.lesson1_lists > ul > li')  # 必修的课程列表
    tmp_url = wd.current_url
    length_necessary_list = len(necessary_list)  # 必修课的个数
    index_necessary_list = 1  # 第几个必修课
    remove_blank()  # 移除target="_blank"属性
    for j in range(length_necessary_list):
        manage(j)  # 处理视频
        wd.get(tmp_url)  # 处理完视频回退
        remove_blank()  # 移除target="_blank"属性
        print("专题{}/{}:完成必修课程{}/{},三秒后进入下一个课程...".format(index_study_list, length_study_list, index_necessary_list,
                                                         length_necessary_list))
        time.sleep(3)
        index_necessary_list += 1
    index_study_list += 1  # 专题加一
    wd.get("https://dxpx.uestc.edu.cn/jjfz/lesson")
