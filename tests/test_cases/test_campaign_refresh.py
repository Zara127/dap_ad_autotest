import pytest
import allure
from datetime import datetime
from src.common.utils import load_yaml, generate_test_combinations
from src.core.locators import AdListLocators, CampaignLocators
from src.pages.campaign_page import CampaignPage

# 加载数据
base_data_single = load_yaml("tests/test_data/base_data_single.yaml")
scenarios_single = load_yaml("tests/test_data/scenarios_single.yaml")

@allure.epic("广告创编测试")
@allure.feature("批量创建页面刷新功能")

class TestCampaignRefresh:
    @allure.story("测试表单页刷新情况内容")
    @pytest.mark.parametrize(
        "scenario_single",
        scenarios_single["short_video_scenarios"],
        ids=[s["name"] for s in scenarios_single["short_video_scenarios"]]
    )
    def test_form_refresh(self, campaign_page, scenario_single):
        """测试表单页刷新清空内容"""
        test_data = next(generate_test_combinations(scenario_single, base_data_single))
        if test_data["budget_type"] == "不限":  # 没有日预算
            campaign_page.set_budget(
                time=test_data["time"],
                time_period=test_data["time_period"],
                bidding_strategy=test_data["bidding_strategy"],
                budget_type=test_data["budget_type"],
                ad_budget=test_data["ad_budget"],
                ad_bid=test_data["ad_bid"]
            )
        else:  # 日预算
            campaign_page.set_budget(
                time=test_data["time"],
                time_period=test_data["time_period"],
                bidding_strategy=test_data["bidding_strategy"],
                budget_type=test_data["budget_type"],
                daily_budget=test_data["daily_budget"],
                ad_budget=test_data["ad_budget"],
                ad_bid=test_data["ad_bid"]
            )
        with allure.step("刷新页面，验证清空草稿内容"):
            campaign_page2 = campaign_page.refresh_page()
            campaign_page2.page.locator(CampaignLocators.LIST_SCHEDULE_BUDGET).click()  # 定位到上次有输入的地方方便查看是否清空
            assert campaign_page2.is_form_empty(), "刷新后表单内容未清空"
