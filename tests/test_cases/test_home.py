import pytest
import allure

@allure.epic("广告平台UI测试")
@allure.feature("主页功能")
class TestHome:
    @allure.story("页面加载测试")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_page_load(self, home_page): # 直接使用fixture，无需重新定义
        """测试主页基础加载"""
        with allure.step("验证主页核心元素"):
            assert home_page.is_loaded()

        allure.attach(
            home_page.page.screenshot(full_page=True),
            name="主页截图",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.story("导航菜单测试")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigation_items(self, home_page):
        """验证主导航菜单"""
        expected_items = ["广告", "广告数据","万花筒","工具库"]
        actual_items = home_page.get_nav_items()
        assert all(item in actual_items for item in expected_items)

    @allure.story("跳转到广告创建页面测试")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_campaign(self,home_page):
        """测试从主页进入创建广告流程"""
        campaign_page = home_page.click_create_btn(platform="巨量引擎")
        assert campaign_page.is_loaded()