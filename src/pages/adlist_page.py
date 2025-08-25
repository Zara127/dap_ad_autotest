from src.core.base_page import BasePage
from src.core.locators import AdListLocators


class AdListPage(BasePage):
    def is_loaded(self):
        return self.page.is_visible(AdListLocators.CREATE_BUTTON)

    def get_current_page_url(self):
        """获取当前页面 URL，用于判断跳转"""
        return self.page.url

    def filter_by_current_user(self,game,account):
        """筛选当前用户创建的广告""" #todo 当前用户是指dap登录用户还是关联账户？？？
        #选择关联游戏
        self.page.locator(AdListLocators.GAME_SELECTOR).first.click()
        self.page.get_by_role("listitem").filter(has_text=game).click()
        #跳转到广告层级
        self.page.get_by_role("tab", name="广告", exact=True).click()
        #输入当前创建广告的账户
        self.page.locator(AdListLocators.FILTER_BAR).get_by_role("textbox", name="请选择").click()
        self.page.locator(AdListLocators.FILTER_BAR).get_by_text("广告账户").click()
        self.page.locator(AdListLocators.FILTER_SEARCH_INPUT).fill(account)
        self.page.locator(AdListLocators.FILTER_SEARCH_INPUT).press("Enter")
        self.page.wait_for_load_state("networkidle")

    def filter_by_account(self, account):
        """筛选指定账户"""
        self.page.locator(AdListLocators.ACCOUNT_FILTER).click()
        self.page.locator(AdListLocators.ACCOUNT_OPTION(account)).click()
        self.page.locator(AdListLocators.FILTER_CONFIRM).click()
        self.page.wait_for_load_state("networkidle")

    def filter_by_project(self, project):
        """筛选指定项目"""
        self.page.locator(AdListLocators.PROJECT_FILTER).click()
        self.page.locator(AdListLocators.PROJECT_OPTION(project)).click()
        self.page.locator(AdListLocators.FILTER_CONFIRM).click()
        self.page.wait_for_load_state("networkidle")

    def get_visible_ads(self):
        """获取当前可见的广告列表"""
        return self.page.locator(AdListLocators.AD_ROWS).all()

    def refresh_page(self):
        """刷新页面并验证筛选条件是否保留"""
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        return self.is_loaded()

    def clear_all_filters(self):
        """清除所有筛选条件"""
        self.page.locator(AdListLocators.CLEAR_FILTERS).click()


    def is_current_user_filtered(self):
        """验证是否已筛选当前用户"""
        return self.page.is_visible(AdListLocators.CURRENT_USER_FILTER)

    def is_account_filtered(self, account):
        """验证是否已筛选指定账户"""
        return self.page.is_visible(AdListLocators.ACCOUNT_FILTERED(account))

    def is_project_filtered(self, project):
        """验证是否已筛选指定项目"""
        return self.page.is_visible(AdListLocators.PROJECT_FILTERED(project))

    def get_first_ad_name(self):
        """获取列表中第一个广告的名称"""
        return self.page.locator(AdListLocators.AD_NAME_FIRST).text_content()

    def get_ad_count(self):
        """获取当前显示的广告数量"""
        return self.page.locator(AdListLocators.AD_ROWS).count()