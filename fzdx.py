# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:/selenium_test"
# https://dxpx.uestc.edu.cn/
# https://dxpx.uestc.edu.cn/fzdx/lesson
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
        self.base_url = 'https://dxpx.uestc.edu.cn/fzdx/lesson'  # 基准url
        self.option = Options()
        self.option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.wd = webdriver.Chrome(service=Service('chromedriver.exe'), options=self.option)
        self.wd.implicitly_wait(15)  # 隐式等待

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
            except Exception as e:
                print(e)
            print("检测到视频暂停,继续播放")

    def printInfo(self, one_index):
        """输出视频信息"""
        print()  # 换行
        time.sleep(1)
        while True:
            try:
                time_ele = self.wd.find_element(By.CSS_SELECTOR, 'div[aria-label="Current time"]')
                print("\r剩余时间:" + time_ele.get_attribute("innerText").replace('-', ''), end='')
                # 检测并处理暂停
                self.address_pause()
                time_ele = self.wd.find_element(By.CSS_SELECTOR, 'div[aria-label="Current time"]')
                if time_ele.get_attribute("innerText").replace('-', '') == "00:00":
                    print('播放完成,点击按钮"我知道了"')
                    break
            except Exception as e:
                self.wd.save_screenshot(f"视频{one_index}.png")
                with open(f"视频{one_index}.txt", "w") as f:
                    f.write(str(e))

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
                # 处理继续观看
                try:
                    continue_ele = self.wd.find_element(By.CSS_SELECTOR, 'a.public_cancel')  # 点击继续观看
                    continue_ele.send_keys(Keys.ENTER)
                except Exception as e:
                    print(e)
                self.printInfo(sidebar_i)  # 输出视频信息

    def run(self):
        # 按钮'我要学习'的列表
        study_list = self.wd.find_elements(By.CSS_SELECTOR, 'div.expand_btn a')
        # 一共几门课
        length_study_list = len(study_list)
        for index_study_list in range(length_study_list):
            # 按钮'开始学习'的列表
            study_list = self.wd.find_elements(By.CSS_SELECTOR, 'div.expand_btn a')
            # 点击按钮'开始学习' 然后进入二级界面
            study_list[index_study_list].send_keys(Keys.ENTER)
            # 接下来只考虑二级界面
            # 获得按钮'必修'
            necessary_btn = self.wd.find_element(By.CSS_SELECTOR, 'body > div > div.w1150 > div.wrap_right > div.lesson1_cont.q_lesson1_con > div.lesson1_title > div > a:nth-child(2)')
            # 点击‘按钮’必修
            necessary_btn.send_keys(Keys.ENTER)
            # 必修页面的课程列表
            necessary_list = self.wd.find_elements(By.CSS_SELECTOR, 'div.l_list_right > h2 > a')
            # 二级页面(必修)的地址
            necessary_page = self.wd.current_url
            # 必修课的个数
            length_necessary_list = len(necessary_list)

            for index_necessary_list in range(length_necessary_list):
                # 处理每个必修专题视频
                self.manage(index_necessary_list)
                # 处理完视频回退
                self.wd.get(necessary_page)
                print(f"专题{index_study_list + 1}/{length_study_list}:完成必修课程{index_necessary_list + 1}/{length_necessary_list},三秒后进入下一个必修课程...")
            self.wd.get(self.base_url)
        print("完成所有必修课程学习!")


if __name__ == '__main__':
    m = Main()
    m.run()
