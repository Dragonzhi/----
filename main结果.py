from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# 创建主窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

print("初始化完成...")

# 使用 simpledialog 获取用户输入
username = simpledialog.askstring("输入", "请输入学号：")
print("username:",username)
password = simpledialog.askstring("输入", "请输入密码：", show='*')
print("password:",password)
# 登录所需的信息
# username = '2024013462'
# password = 'zhilong520.'

# username = input("请输入学号：")
# password = input("请输入密码：")

# 登录页面的 URL
login_url = 'https://newehall.nwafu.edu.cn/login'
target_url = simpledialog.askstring("输入", "请输入过程评教的地址：")
# target_url = "https://newehall.nwafu.edu.cn/jwapp/sys/jwwspj/*default/index.do?t_s=1749014041014&amp_sec_version_=1&gid_=VnhSRTRsRlgzN2ZvSmZ6WU95S29BRW1paHk4djhXZmhCTkJEVzM3dXA5elJIYTljajJuZU9KQzdYUWpJekNMbFByY1BvSCtUcHJsSXdEV2ZTVWVXbVE9PQ&EMAP_LANG=zh&THEME=millennium#/pj"

comments = [
    "教师教学很棒！",
    "Good",
    "非常好",
    "好的很",
    "GG"
]

# 设置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0')

# 指定 ChromeDriver 的路径，需替换为你本地的路径
# chromedriver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
# # 使用ChromeDriverManager自动获取匹配的驱动
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

# pyinstaller --onefile main结果.py

if getattr(sys, 'frozen', False):
    base_path = simpledialog.askstring("输入", "请输入Driver路径：")
    print("pathbase:",base_path)
    print("打包环境中尝试使用本地 ChromeDriver ...")
    # 获取打包后可执行文件所在目录
    chromedriver_path = os.path.join(base_path, 'chromedriver.exe')
    try:
        print("尝试使用本地 ChromeDriver...")
        service = Service(chromedriver_path)
        # 尝试初始化 Chrome 驱动，验证驱动是否可用
        test_driver = webdriver.Chrome(service=service, options=chrome_options)
        test_driver.quit()
        print("找到本地 ChromeDriver，使用本地驱动...")
    except Exception as e:
        print(f"使用本地 ChromeDriver 失败，错误信息: {str(e)}，动态下载驱动...")
        # 设置国内镜像源
        os.environ['WDM_SOURCE_URL'] = "https://registry.npmmirror.com/-/binary/chromedriver"
        # 打包环境，使用 webdriver_manager 动态获取 ChromeDriver
        service = Service(ChromeDriverManager().install())
        print("使用动态获取的 ChromeDriver 完成")
else:
    # 开发环境
    chromedriver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    service = Service(chromedriver_path)
    print("开发环境中使用指定的 ChromeDriver...")
driver = webdriver.Chrome(service=service, options=chrome_options)


try:
    # 打开登录页面并登录
    driver.get(login_url)
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'login_submit'))
    )
    login_button.click()
    time.sleep(2)
    
    # 进入目标页面
    driver.get(target_url)
    time.sleep(3)
    flag = True
    if "统一身份认证" in driver.title:  # 检查是否需要进行统一身份认证
        flag = False
        print("登入失败，请检查账号密码是否正确")
    # 循环处理所有未提交的卡片（关键逻辑修改）
    while flag:
        try:
            try:
                # 重新获取当前所有未提交的卡片（确保在主页面）
                cards = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 
                            ".bh-card.bh-card-lv1[data-action='查询问卷详情'] .sc-panel-diagonalStrips.sc-panel-warning")
                    )
                )
            except Exception as e:
                print("全部卡片处理完毕")
                break
            # 处理第一个卡片（避免索引错位）
            target_card = cards[0]
            target_card.click()
            time.sleep(2)
            
            # 处理问卷
            try:
                radio_groups = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".sc-panel-thingNoImg-1-container.wjzb-card")
                    )
                )
                if radio_groups:
                    radio_groups.pop(-1)  # 排除最后一个主观题
                
                for index, group in enumerate(radio_groups):
                    try:
                        time.sleep(0.4)
                        # print(f"正在处理第 {index + 1} 个单选题 : group = {group.text}")
                        input_elements = WebDriverWait(group, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-x-dasm="完全赞同"]'))
                        )
                        for element in input_elements:
                            try:
                                # print("element:",element)
                                try:
                                    element.click()
                                except Exception:
                                    # 若常规点击失败，使用 JavaScript 点击
                                    driver.execute_script("arguments[0].click();", element)
                                print("成功点击一个“完全赞同”选项")
                            except Exception as e:
                                print(f"点击“完全赞同”选项出错: {str(e)}")
                        print(f"成功点击第 {index + 1} 个单选题的所有“完全赞同”选项")
                    except Exception as e:
                        print(f"第 {index + 1} 个单选题出错: {str(e)}")
                # 处理主观题
                try:
                    subjective_textareas = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'textarea[name="YLCS"]'))
                    )
                    for index, textarea in enumerate(subjective_textareas):
                        try:
                            # 滚动到元素可见位置
                            driver.execute_script("arguments[0].scrollIntoView();", textarea)
                            # 确保元素可点击
                            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(textarea))
                            # 输入随机评论
                            textarea.send_keys(comments[random.randint(0, len(comments) - 1)])
                            print(f"第 {index + 1} 个主观题输入成功")
                        except Exception as e:
                            print(f"第 {index + 1} 个主观题输入失败: {str(e)}")
                except Exception as e:
                    print(f"查找主观题元素失败: {str(e)}")
                time.sleep(0.5)
                # 提交问卷
                try:
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.bh-btn.bh-btn-success.bh-btn-large'))
                    )
                    submit_button.click()
                    print("提交按钮点击成功")
                    
                    # 等待确认弹窗并点击确认
                    confirm_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.bh-dialog-btn.bh-bg-primary.bh-color-primary-5'))
                    )
                    confirm_button.click()
                    print("确认提交按钮点击成功")
                except Exception as e:
                    print(f"提交按钮出错: {str(e)}")
                time.sleep(3)
            except Exception as e:
                print(f"问卷处理出错: {str(e)}")
                driver.back()  # 出错时返回主页面继续尝试
                driver.get(target_url)
                time.sleep(3)
        except Exception as e:
            print(f"循环错误: {str(e)}")
            break
        time.sleep(5)
except Exception as e:
    print(f"操作出错: {e}")
finally:
    driver.quit()