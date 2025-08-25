# 页面基类 POM
import json
import os
import time
from playwright.sync_api import Page, Cookie,expect
from src.common.utils import load_config
from dotenv import load_dotenv

from src.core.locators import AuthLocators

#登录页——账户密码登录——navigate
class BasePage:
    def __init__(self, page: Page, env='test'):
        self.page = page
        self.env = env
        # self._inject_auth_token()  #初始化时自动调用,冲突
        # self.handle_popups() # 初始化时设置弹窗监听

    def _inject_auth_token(self):
        """注入Authorization到所有请求头"""
        config = load_config(self.env)
        token = config['test']['auth']['token']   #!!!注意test层级

        #设置请求头
        self.page.context.set_extra_http_headers({
            "Authorization": f"Basic "+ token,
            "auth-token": token,
        })

    def handle_popups(self):
        """处理弹窗逻辑"""
        def on_popup(popup):
            print("检测到弹窗，正在判断是否为账号安全中心-应用授权管理页面...")
            try:
                # 等待弹窗加载特定元素（超时时间3秒）
                popup.wait_for_selector("//div[contains(text(), '应用授权管理')]", timeout=3000)
                print("确认是账号安全中心-应用授权管理页面，正在关闭...")
                popup.close()
                print("账号安全中心-应用授权管理页面已关闭")
            except:
                print("不是账号安全中心-应用授权管理页面，继续保留")

        self.page.on("popup", on_popup)# 设置弹窗监听器


    def navigate(self, path):
        base_url = load_config(self.env)['test']['base_url'] #!!!注意忘记test层级
        target_url = f"{base_url}{path}"
        self.page.goto(target_url, wait_until="networkidle")



    def wait_for_element(self, selector, timeout=5000):
        """等待元素加载"""
        self.page.wait_for_selector(selector, timeout=timeout)

    def select_option(self, selector, value):
        """选择下拉框选项"""
        self.page.select_option(selector, value)

    def click_element(self, selector):
        """点击元素"""
        self.page.click(selector)

    def fill_input(self, selector, text):
        """填写输入框"""
        self.page.fill(selector, text)

    def is_element_visible(self, selector, timeout=2000):
        """检查元素是否可见"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return self.page.is_visible(selector)
        except:
            return False