import pytest
import allure

from src.common.utils import load_yaml, generate_test_combinations
from src.core.locators import  CampaignLocators
from src.pages.old_campaign_page import OldCampaignPage  # 导入旧版页面类

# 加载数据
base_data = load_yaml("tests/test_data/base_data.yaml")
scenarios = load_yaml("tests/test_data/scenarios.yaml")

@allure.epic("广告创编测试")
@allure.feature("旧版巨量引擎-批量创建功能测试")
class TestOldVersionBatchCreate:
    """旧版页面测试用例，使用 OldCampaignPage 驱动"""

    @pytest.fixture(scope="function")
    def old_campaign_page(self, campaign_page):
        """ fixture 初始化旧版页面（打开旧版链接）"""
        # 1. 确保当前在新版页面
        assert campaign_page.is_loaded(), "新版页面加载失败"
        # 2. 点击返回旧版按钮
        with allure.step("点击「返回旧版」按钮"):
            page = campaign_page.click_return_old_version()
        return OldCampaignPage(page)  # 初始化旧版操作类

    @allure.story("旧版页面加载验证")
    def test_old_version_load(self, old_campaign_page):
        """验证旧版页面是否正确加载"""
        assert old_campaign_page.is_old_version_loaded(), "旧版页面未加载或定位器失效"
        current_url = campaign_page.get_current_url_after_click()
        assert "advertise-2/toutiao2/batch-create" in current_url, f"跳转URL不符合预期，实际URL: {current_url}"  # todo 旧版链接

    @allure.story("旧版批量创建主流程")
    @pytest.mark.parametrize(
        "scenario",
        scenarios["short_video_scenarios"] + scenarios["live_scenarios"],
        ids=[s["name"] for s in scenarios["short_video_scenarios"] + scenarios["live_scenarios"]]
    )
    def test_old_version_batch_create(self, old_campaign_page, scenario):
        """旧版页面执行批量创建测试"""
        test_data = next(generate_test_combinations(scenario, base_data))
        case_id = f"{test_data['scenario_name']}"

        with allure.step(f"执行旧版组合测试: {case_id}"):
            allure.dynamic.title(case_id)
            allure.dynamic.description(f"测试组合: {test_data}")

            # 旧版页面执行创建
            create_result = old_campaign_page.create_campaign(test_data)

            # 结果断言（旧版以列表页存在广告为成功标志）
            assert create_result, f"旧版广告{case_id}创建失败，无法进入预览页面"

        # # 2. 点击预览按钮并验证跳转预览页
        # with allure.step("点击预览广告按钮，验证跳转"):
        #     preview_page = campaign_page.click_preview_button()
        #     assert preview_page.is_loaded(), "预览页面加载失败"
        #     assert "preview" in preview_page.get_current_page_url(), "未跳转到预览页面"
        #
        # # 3. 预览页点击“创建广告”，验证跳转广告列表页
        # with allure.step("预览页点击创建广告，验证跳转列表页"):
        #     ad_list_page = preview_page.click_create_ad_button()
        #     assert ad_list_page.is_loaded(), "广告列表页面加载失败"
        #     assert "list" in ad_list_page.get_current_page_url(), "未跳转到广告列表页"