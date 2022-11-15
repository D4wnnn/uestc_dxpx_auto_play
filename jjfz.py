# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:/selenium_test"
# https://dxpx.uestc.edu.cn/
# https://dxpx.uestc.edu.cn/jjfz/lesson
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class Main:
    def __init__(self):
        """
        selenium预处理
        """
        self.base_url = 'https://dxpx.uestc.edu.cn/jjfz/lesson'  # 基准url
        self.option = Options()
        self.option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.wd = webdriver.Chrome(service=Service('chromedriver.exe'), options=self.option)
        self.wd.implicitly_wait(3)  # 隐式等待
        self.index_study_list = 0

    def remove_blank(self):
        """更改属性target为'_self'"""
        js = 'var items = document.getElementsByTagName("a");for (var i = 0; i < items.length; i++) {var tmp = items[' \
             'i];tmp.target="_self";} '
        self.wd.execute_script(js)

    def address_pause(self):
        """处理视频暂停问题"""
        pause_ele = self.wd.find_element(By.CSS_SELECTOR, '#wrapper > div > div.plyr__controls > button:nth-child(1)')
        if pause_ele.get_attribute("aria-label") == "Play":
            pause_btn = self.wd.find_element(By.CSS_SELECTOR, '#wrapper > div > div.plyr__controls > button:nth-child(1)')
            pause_btn.send_keys(Keys.ENTER)
            try:
                # 尝试点击'继续'(处理弹窗)
                self.wd.find_element(By.CSS_SELECTOR, '.public_btn a').click()
            except Exception:
                pass
            print("检测到视频暂停,继续播放")

    def printInfo(self):
        """输出视频信息"""
        print()  # 换行
        self.wd.implicitly_wait(0)
        while True:
            try:
                # 获取时间元素
                time_ele = self.wd.find_element(By.CSS_SELECTOR, 'div[aria-label="Current time"]')
                # 若视频播放完成则休眠三秒
                if time_ele.get_attribute("innerText").replace('-', '') == "00:00":
                    time.sleep(3)
                    self.wd.implicitly_wait(3)
                    return
                elif len(self.wd.find_elements(By.CSS_SELECTOR, '#wrapper > div > div.plyr__controls > div.plyr__controls__item.plyr__menu > button > span')) == 1:
                    time.sleep(3)
                    print("2315413451#%!@#%!@#%!2351235")
                    self.wd.implicitly_wait(3)
                    return
                else:
                    # 打印时间信息
                    time_ele = self.wd.find_element(By.CSS_SELECTOR, 'div[aria-label="Current time"]')
                    print("\r剩余时间:" + time_ele.get_attribute("innerText").replace('-', ''), end='')
                    # 检测并处理暂停
                    self.address_pause()
            except Exception:
                pass

    def address_box(self):
        try:
            # 获取按钮我知道了
            i_know = self.wd.find_element(By.CSS_SELECTOR, 'a.public_submit')
            # 点击按钮我知道了
            i_know.click()
            # 获取按钮继续观看
            continue_ele = self.wd.find_element(By.CSS_SELECTOR, 'a.public_cancel')
            # 点击按钮继续观看
            continue_ele.send_keys(Keys.ENTER)
        except Exception:
            pass

    def manage(self, j):
        """处理每一个必修视频"""
        # 必修页面的课程列表
        necessary = self.wd.find_elements(By.CSS_SELECTOR, 'div.l_list_right > h2 > a')
        # 点击必修课程
        necessary[j].send_keys(Keys.ENTER)
        # 接下来只考虑三级界面
        # 获得侧边栏的课程列表
        sidebars = self.wd.find_elements(By.CSS_SELECTOR, 'a[style]')
        length_sidebar = len(sidebars)
        print(f"成功加载侧边栏的课程列表,一共{length_sidebar}个视频")
        for sidebar_i in range(length_sidebar):
            # 获得侧边栏的课程列表
            sidebars = self.wd.find_elements(By.CSS_SELECTOR, 'a[style]')
            print(f"正在播放第{sidebar_i + 1}个视频，一共{length_sidebar}个")
            # 判断是否播放完
            if "red" in sidebars[sidebar_i].get_attribute("style"):
                print(f"视频{sidebar_i + 1}播放完成,即将播放下一个视频")
                continue
            else:
                # 若未播放完
                sidebars[sidebar_i].send_keys(Keys.ENTER)
                # 处理一些弹窗
                self.address_box()
                # 输出视频信息
                self.printInfo()

    def run(self):
        # 按钮'开始学习'的列表
        study_list = self.wd.find_elements(By.CSS_SELECTOR, 'div.lesson_center_a a.study')
        # 一共几门课
        length_study_list = len(study_list)
        for index_study_list in range(length_study_list):
            self.index_study_list = index_study_list
            # 按钮'开始学习'的列表
            study_list = self.wd.find_elements(By.CSS_SELECTOR, 'div.lesson_center_a a.study')
            # 点击按钮'开始学习' 然后进入二级界面
            study_list[index_study_list].send_keys(Keys.ENTER)
            # 接下来只考虑二级界面
            if self.index_study_list != 8:
                # 获得按钮精品课程
                good_btn = self.wd.find_element(By.CSS_SELECTOR, 'body > div > div.w1150 > div.wrap_left > div.wrap_left_list.lesson_left > ul > li:nth-child(2) > div > a > span')
                # 点击按钮精品课程
                good_btn.click()
            # 获得按钮'必修'
            necessary_btn = self.wd.find_element(By.CSS_SELECTOR, 'body > div > div.w1150 > div.wrap_right > div.lesson1_cont.q_lesson1_cont > div.lesson1_title > div > a:nth-child(2)')
            # 点击‘按钮’必修
            necessary_btn.send_keys(Keys.ENTER)
            # 必修页面的课程列表
            necessary_list = self.wd.find_elements(By.CSS_SELECTOR, 'div.l_list_right > h2 > a')
            # 二级页面(必修)的地址
            necessary_page = self.wd.current_url
            # 必修课的个数
            length_necessary_list = len(necessary_list)

            for index_necessary_list in range(length_necessary_list):
                # 移除_blank
                self.remove_blank()
                # 处理每个必修专题视频
                self.manage(index_necessary_list)
                # 处理完视频回退
                self.wd.get(necessary_page)
                if self.index_study_list != 8:
                    # 获得按钮精品课程
                    good_btn = self.wd.find_element(By.CSS_SELECTOR, 'body > div > div.w1150 > div.wrap_left > div.wrap_left_list.lesson_left > ul > li:nth-child(2) > div > a > span')
                    # 点击按钮精品课程
                    good_btn.click()
                # 获得按钮'必修'
                necessary_btn = self.wd.find_element(By.CSS_SELECTOR, 'body > div > div.w1150 > div.wrap_right > div.lesson1_cont.q_lesson1_cont > div.lesson1_title > div > a:nth-child(2)')
                # 点击‘按钮’必修
                necessary_btn.send_keys(Keys.ENTER)
                print(f"专题{index_study_list + 1}/{length_study_list}:完成必修课程{index_necessary_list + 1}/{length_necessary_list},三秒后进入下一个必修课程...")
            self.wd.get(self.base_url)
        print("完成所有必修课程学习!")


if __name__ == '__main__':
    m = Main()
    m.run()
