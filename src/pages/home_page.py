from src.core.base_page import BasePage
from src.core.locators import HomeLocators, CampaignLocators
from src.pages.campaign_page import CampaignPage


#主页
class HomePage(BasePage):
    def __init__(self, page, env='test'):
        super().__init__(page, env)

    def is_loaded(self):
        """验证主页是否成功加载"""
        return self.page.is_visible(HomeLocators.MAIN_CONTENT)

    def get_nav_items(self):
        """获取主导航菜单项"""
        return [item.inner_text() for item in
                self.page.query_selector_all(HomeLocators.NAV_ITEMS)]

    def navigate_to(self, menu_name):
        """导航到指定菜单"""
        menu_item = self.page.get_by_role("menuitem", name=menu_name)
        menu_item.click()
        return self

    def click_create_btn(self, platform):
        """点击去创建按钮，进入广告创建页面"""
        with self.page.expect_popup() as page2_info:
            self.page.get_by_text("去创建").first.click()
        page2 = page2_info.value
        # 等待页面加载完成
        page2.wait_for_load_state("networkidle")
        #保证页面成功加载
        try:
            page2.locator(CampaignLocators.PAGE_TITLE).wait_for(state="visible", timeout=5000)  # 等待特定元素可见
        except Exception as e:
            print(f"特定元素未加载: {e}. 尝试重新加载页面...")
            page2.reload()
            page2.wait_for_load_state("networkidle")
            page2.locator(CampaignLocators.PAGE_TITLE).wait_for(state="visible", timeout=5000)  # 再次等待特定元素可见

        #返回广告创建页面实例
        return CampaignPage(page2)





