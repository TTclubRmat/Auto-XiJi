# 希冀网课自动脚本 Ver 1.1
# By TIANT
# 2024.10.14

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

username = 'xxxxxxxxxxx'  # 用户名
password = 'xxxxxxxxxxx'  # 密码
className = 'C程序设计'  # 课程名称
videoName = 'C程序设计'  #子课程名称

# Edge WebDriver路径（下载地址：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#installation）
# 如果该WebDriver不符合您的Edge浏览器版本请自行下载替换
edge_driver_path = 'msedgedriver_new.exe'
service = Service(edge_driver_path)

options = webdriver.EdgeOptions()
options.use_chromium = True
driver = webdriver.Edge(service=service, options=options)


def wait_for_video_completion(driver):
    while True:
        # 找到并获取<span class="vjs-remaining-time-display">标签的内容
        remaining_time_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'vjs-remaining-time-display'))
        )
        remaining_time = remaining_time_element.text
        print(f"获取课程时间: {remaining_time}")
        try:
            minutes, seconds = map(int, remaining_time.split(':'))
            total_seconds = minutes * 60 + seconds
            break
        except (ValueError, AttributeError):
            print("无效的时间格式，重新获取")
            time.sleep(1)
    time.sleep(total_seconds + 10)
    print("准备进入下一课\n")


def select_next_option(driver):
    # 找到<select>元素
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'classSelect'))
    )

    # 获取所有<option>元素
    options = select_element.find_elements(By.TAG_NAME, 'option')

    # 找到当前选中的<option>并选择下一个选项
    for index, option in enumerate(options):
        if option.get_attribute('selected'):
            next_index = (index + 1) % len(options)  # 循环选择
            next_option = options[next_index]
            print(f"-----开始播放 {next_option.text}-----")
            next_option.click()
            break


try:
    # 打开浏览器并登录到指定地址
    driver.get('http://10.5.151.196')

    # 等待页面加载
    time.sleep(1)  # 页面加载较慢，增加等待时间

    # 搜索并填写学号
    stid_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    stid_input.clear()
    stid_input.send_keys(username)

    # 搜索并填写密码
    pwd_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    pwd_input.clear()
    pwd_input.send_keys(password)

    # 搜索并点击登录按钮
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(text(), "登 录")]'))
    )
    login_button.click()

    # 等待1秒
    time.sleep(1)

    # 搜索并点击课程链接
    intro_to_computers_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, className))
    )
    intro_to_computers_link.click()

    # 搜索并点击子课程链接
    intro_to_computers_24_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, videoName))
    )
    intro_to_computers_24_link.click()

    # 搜索页面上为“继续学习”文字的a标签，点击该标签
    continue_learning_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, '继续学习'))
    )
    continue_learning_link.click()
    print("-----开始继续学习-----")

    while True:
        # 点击播放视频按钮
        play_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="vjs-big-play-button" and @title="Play Video"]'))
        )
        play_button.click()
        time.sleep(2)
        # 等待视频播放完成
        wait_for_video_completion(driver)
        # 选择下一个选项
        select_next_option(driver)

except Exception as e:
    print(f"Error: {e}")
finally:
    # 关闭浏览器
    driver.quit()
