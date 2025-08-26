import re

from src.core.base_page import BasePage
from src.core.locators import PreviewLocators
from src.pages.adlist_page import AdListPage


class PreviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def get_current_page_url(self):
        """获取当前页面 URL，用于判断跳转"""
        return self.page.url

    def is_loading(self):
        """验证是否显示数据加载中状态"""
        return self.page.is_visible(PreviewLocators.LOADING_INDICATOR_OLD)

    def wait_for_loading_complete(self):
        """等待数据加载状态消失"""
        self.page.wait_for_selector(PreviewLocators.LOADING_INDICATOR_OLD,state="hidden",timeout=15000)

    def is_loaded(self):
        """验证预览页面是否加载完成"""
        return self.page.is_visible(PreviewLocators.PREVIEW_TITLE)


    def click_create_ad_button(self):  #注：如果会新建页面的话，需要修改返回page2
        """点击预览页「创建广告」按钮，跳转广告列表页"""
        self.click_element(PreviewLocators.CREATE_BUTTON) #点击创建广告按钮
        self.page.wait_for_load_state("networkidle")
        return AdListPage(self.page)  # 返回AdListPage 页面对象类

    def click_back_button(self):
        """点击「返回上一页」按钮，保留草稿内容"""
        self.click_element(PreviewLocators.BACK_BUTTON)
        self.page.wait_for_load_state("networkidle")
        from src.pages.campaign_page import CampaignPage  # 避免循环导入
        return CampaignPage(self.page)

    def click_browser_back(self):
        """点击浏览器返回按钮,清空草稿内容"""
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")
        from src.pages.campaign_page import CampaignPage
        return CampaignPage(self.page)

    def verify_ad_preview_title(self):
        """用于验证创意预览/创意设置是否已更名为广告预览/广告设置"""
        data_grid = self.page.locator(PreviewLocators.AD_PREVIEW_GRID).text_content()
        return data_grid


    def play_ad_material(self):
        """点击播放按钮预览素材"""
        self.click_element(PreviewLocators.PLAY_BUTTON)
        # 验证播放状态（根据实际情况调整）
        self.page.wait_for_selector(PreviewLocators.PAUSE_BUTTON, state="visible")
        return self.page.is_visible(PreviewLocators.PAUSE_BUTTON)


    def get_account_name(self):
        """获取账户名称"""
        full_name = self.page.locator(PreviewLocators.ACCOUNT_NAME).text_content()
        # 提取关键文字（正则或字符串分割）
        # 1. 提取前缀（第一个 '-' 之前的内容）
        prefix = full_name.split('-')[0]  # 结果如 '赛铂'

        # 2. 提取中间标识（匹配所有中文或字母的标识，如 '预约'）
        # 正则表达式：匹配 '---' 后的中文/字母标识
        match = re.search(r'---[a-zA-Z\u4e00-\u9fa5]+', full_name)
        if match:
            # 提取标识并去除 '---'
            middle_part = match.group().replace('---', '')
            # 保留 '预约' 等标识
            middle_part = middle_part.split('-')[0]
        else:
            middle_part = ""

        # 3. 提取数字（最后一个 '-' 之后的内容）
        last_dash_index = full_name.rfind('-')
        if last_dash_index != -1:
            number_part = full_name[last_dash_index + 1:]
        else:
            number_part = ""

        # 组合结果
        return f"{prefix}{middle_part}{number_part}"

    def get_project_name(self):
        """获取项目名称"""
        return self.page.locator(PreviewLocators.PROJECT_NAME).text_content()

    def get_ad_name(self):
        """获取广告名称"""
        return self.page.locator(PreviewLocators.AD_NAME).text_content()

