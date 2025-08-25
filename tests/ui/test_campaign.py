import pytest
import allure
from datetime import datetime
from src.common.utils import load_yaml, generate_test_combinations
from src.core.locators import AdListLocators, CampaignLocators
from src.pages.campaign_page import CampaignPage

# 加载数据
base_data = load_yaml("tests/test_data/base_data.yaml")
scenarios = load_yaml("tests/test_data/scenarios.yaml")

@allure.epic("广告创编测试")
@allure.feature("批量创建功能-新版")

class TestCampaignCreate:
    @allure.story("主页到广告批量创建页面跳转测试")
    def test_campaign_loaded(self, campaign_page):
        assert campaign_page.is_loaded(), "广告批量创建页面加载失败"

    # [返回旧版]测试在test_campaign_old.py中

    @allure.story("批量创建测试")
    @pytest.mark.parametrize(
        "scenario",
        # scenarios["short_video_scenarios"]+   #todo
        scenarios["live_scenarios"],
        ids=[s["name"] for s in
             # scenarios["short_video_scenarios"] +    #todo
             scenarios["live_scenarios"]]
    )
    def test_create_campaign(self, campaign_page, scenario):
        """创建广告,生成所有组合"""
        test_data = next(generate_test_combinations(scenario, base_data))
        case_id = f"{test_data['scenario_name']}"
        # 1.执行广告创建
        with allure.step(f"执行组合测试: {case_id}"):
            allure.dynamic.title(case_id)
            allure.dynamic.description(f"测试组合: {test_data}")
            create_result = campaign_page.create_campaign(test_data)
            campaign_page.refresh_page()
            # 验证结果
            assert create_result, f"广告{case_id}创建流程失败，无法进入预览页面"

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

