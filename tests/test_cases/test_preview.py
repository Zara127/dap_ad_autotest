import pytest
import allure
from datetime import datetime
from src.common.utils import load_yaml, generate_test_combinations
from src.core.locators import PreviewLocators, CampaignLocators
from src.pages.campaign_page import CampaignPage
from src.pages.preview_page import PreviewPage

base_data = load_yaml("tests/test_data/base_data_single.yaml")
scenarios = load_yaml("tests/test_data/scenarios_single.yaml")


@allure.epic("广告创编测试")
@allure.feature("预览页功能测试")
class TestPreviewPage:
    # @allure.story("预览页加载状态测试")
    @pytest.fixture(scope="class",params=scenarios["live_scenarios"],
                    ids=lambda scenario: scenario["name"])
    def preview_context(self, campaign_page, request):
        """创建广告并进入预览页，返回上下文"""
        scenario = request.param
        test_data = next(generate_test_combinations(scenario, base_data))
        campaign_page.create_campaign(test_data) # 执行广告创建
        preview_page = campaign_page.click_preview_button() # 进入预览页
        assert preview_page.is_loading(), "未显示数据加载中状态"
        preview_page.wait_for_loading_complete()
        assert not preview_page.is_loading(), "加载状态未消失"

        test_contest = {
            "campaign_page": campaign_page,
            "preview_page": preview_page,
            "test_data": test_data
        }

        yield test_contest

#todo 待验证，现有页面没有
    # @allure.story("预览页加载状态测试")
    # def test_preview_loading_state(self, preview_context):
    #     """验证预览页加载状态显示与消失"""
    #     campaign_page = preview_context["campaign_page"]   #TODO 并不能保存未点击预览按钮前的页面状态
    #
    #     with allure.step("点击预览按钮，验证显示加载状态"):
    #         campaign_page.click_preview_button()
    #         preview_page = PreviewPage(campaign_page.page)
    #         assert preview_page.is_loading(), "未显示数据加载中状态"
    #
    #     with allure.step("等待加载完成，验证加载状态消失"):
    #         preview_page.wait_for_loading_complete()
    #         assert not preview_page.is_loading(), "加载状态未消失"


    @allure.story("预览页面跳转测试")
    def test_preview_page_loaded(self, preview_context):
        """验证预览页面加载成功"""
        preview_page = preview_context["preview_page"]
        assert preview_page.is_loaded(), "预览页面加载失败"
        assert "preview" in preview_page.get_current_page_url(), "未跳转到预览页面"

# #todo，待验证，现有页面未修改
#     @allure.story("预览页标题和功能测试")
#     def test_preview_title_changes(self, preview_context):
#         """测试预览页标题更名"""
#         preview_page = preview_context["preview_page"]
#         data_grid = preview_page.verify_ad_preview_title()
#
#         with allure.step("验证创意预览更名为广告预览"):
#             preview_page.verify_ad_preview_title()
#             assert "广告预览" in data_grid, "标题未更改为广告预览"
#
#         with allure.step("验证创意设置更名为广告设置"):
#             assert "广告设置" in data_grid, "标题未更改为广告设置"
#
#
# #todo 待验证，现有页面没有
#     @allure.story("预览页素材播放功能测试")
#     def test_material_play_function(self, preview_context):
#         """测试素材播放功能"""
#         preview_page = preview_context["preview_page"]
#
#         with allure.step("点击播放按钮，验证素材播放"):
#             is_playing = preview_page.play_ad_material()
#             assert is_playing, "素材播放失败"
#
#
# #TODO 待验证，现有页面没有返回按钮
#     @allure.story("预览页返回功能测试")
#     def test_preview_back_button(self, preview_context):
#         """测试预览页返回按钮功能"""
#         preview_page = preview_context["preview_page"]
#         campaign_page = preview_context["campaign_page"]
#         test_data = preview_context["test_data"]
#
#         with allure.step("验证返回上一页按钮存在"):
#             assert preview_page.page.locator(PreviewLocators.BACK_BUTTON).is_visible(), "返回上一页按钮不存在"
#
#         with allure.step("点击返回上一页，验证保留草稿内容"):
#             campaign_page2 = preview_page.click_back_button()
#
#             # 验证关键字段保留
#             campaign_page2.locator(CampaignLocators.LIST_SCHEDULE_BUDGET).click()  # 定位到上次有输入的地方方便查看是否清空
#             filled_ad_budget = campaign_page2.page.locator(CampaignLocators.AD_BUDGET_INPUT).input_value()
#             assert test_data["ad_budget"] in filled_ad_budget, "广告预算未保留"
#
#             filled_ad_bid = campaign_page2.page.locator(CampaignLocators.AD_BID_INPUT).input_value()
#             assert test_data["ad_bid"] in filled_ad_bid, "广告出价未保留"


    @allure.story("浏览器返回按钮测试")
    def test_browser_back_button(self, preview_context):
        """测试浏览器返回按钮不保留草稿"""
        preview_page = preview_context["preview_page"]

        with allure.step("点击浏览器返回，验证清空草稿内容"):
            campaign_page2 = preview_page.click_browser_back()
            assert campaign_page2.is_form_empty(), "浏览器返回后表单内容未清空"



