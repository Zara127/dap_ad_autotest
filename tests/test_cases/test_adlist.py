import pytest
import allure
from src.common.utils import load_yaml, generate_test_combinations
from src.core.locators import AdListLocators
from src.pages.campaign_page import CampaignPage
from src.pages.adlist_page import AdListPage
from src.pages.preview_page import PreviewPage

# 加载测试数据
base_data = load_yaml("tests/test_data/base_data_single.yaml")
scenarios = load_yaml("tests/test_data/scenarios_single.yaml")

@allure.epic("广告创编测试")
@allure.feature("广告列表页功能")
class TestAdListPage:
    @pytest.fixture(scope="class", params=scenarios["short_video_scenarios"],
                    ids=lambda scenario: scenario["name"])
    def ad_list_context(self, campaign_page, request):
        """创建广告并跳转到广告列表页，返回测试上下文"""
        scenario = request.param
        test_data = next(generate_test_combinations(scenario, base_data))
        # 执行完整创建流程
        campaign_page.create_campaign(test_data) #批量创建
        preview_page = campaign_page.click_preview_button() #进入预览页

        #todo 元素定位有问题
        # account_name = preview_page.get_account_name().text_content() #在预览页获得账户名称，保存在上下文中,用于后续进行筛选功能测试
        # project_name = preview_page.get_project_name().text_content()  # 在预览页获得项目名称
        # ad_name = preview_page.get_ad_name().text_content()  # 在预览页获得广告名称

        ad_list_page = preview_page.click_create_ad_button() #创建广告，进入广告列表页
        ad_list_page.page.wait_for_load_state("networkidle")

        # 如果当前广告列表页存在小弹窗，则关闭掉
        # if ad_list_page.page.locator(".popup").is_visible():
        #     ad_list_page.page.locator(".popup .el-icon-close").click()
        # if ad_list_page.page.locator(".task-progress-detail > div > .el-icon-close").is_visible():
        #     ad_list_page.page.locator(".task-progress-detail > div > .el-icon-close").click()
        # if ad_list_page.page.get_by_role("tooltip", name=" 在这里可以看近三天的批量广告推送进度哦~").locator("i").is_visible():
        #     ad_list_page.page.get_by_role("tooltip", name=" 在这里可以看近三天的批量广告推送进度哦~").locator("i").click()

        account = test_data["account"] #创建广告的账户，用于后续对筛选功能进行测试
        game = test_data["game"] #关联游戏，用于后续对筛选功能进行测试


        test_context = {

            "ad_list_page": ad_list_page,
            "account": account,
            "game": game,
            "test_data": test_data,
            #todo 定位有问题
            # "account_name": account_name,
            # "project_name": project_name,
            # "ad_name": ad_name
        }
        yield test_context

    # -------------------- 批量创建后跳转验证 --------------------

    @allure.story("广告列表页加载测试")
    def test_ad_list_loaded(self, ad_list_context):
        """验证广告列表页加载成功"""
        ad_list_page = ad_list_context["ad_list_page"]
        assert ad_list_page.is_loaded(), "广告列表页面加载失败"
        assert "list" in ad_list_page.get_current_page_url(), "未跳转到广告列表页"

    # -------------------- 最新创建广告验证 --------------------
    @allure.story("最新创建广告验证")
    def test_latest_created_ad(self, ad_list_context):
        """验证最新创建的广告显示在列表顶部"""
        ad_list_page = ad_list_context["ad_list_page"]
        account = ad_list_context["account"]
        game = ad_list_context["game"]

        with allure.step("筛选当前用户和账户"):
            ad_list_page.filter_by_current_user(game, account)

        with allure.step("验证最新创建广告显示在顶部"):
            first_ad_name = ad_list_page.get_first_ad_name() #todo 元素定位有问题
            # 假设广告名称包含特定标识
            assert "DAPNBZDHCS" in first_ad_name, "最新创建的广告未显示在顶部"
    # @allure.story("最新创建广告验证")
    # def test_latest_created_ad(self, ad_list_context):
    #     """验证按照当前用户筛选默认展示最新创建的广告"""
    #     ad_list_page = ad_list_context["ad_list_page"]
    #     account = ad_list_context["account"]
    #     game = ad_list_context["game"]

    #     # ad_name = ad_list_context["ad_name"]    #在预览页可以获得广告名称，保存在上下文中
    #     # project_name = ad_list_context["project_name"] #在预览页可以获得项目名称，保存在上下文中
    #     # account_name = ad_list_context["account_name"] #在预览页可以获得账户名称，保存在上下文中
    #
    #     with allure.step("验证按照当前账户进行筛选，最新广告在列表中"):
    #         ad_list_page.filter_by_current_user(game, account)
    #
    #         first_ad_text = ad_list_page.page.locator(AdListLocators.AD_NAME).text_content()
    #         # 检查第一个广告（最新创建）是否包含广告名称
    #         assert "test_zst" in first_ad_text, "最新创建的广告未显示在顶部"

    # # -------------------- 默认筛选条件验证 --------------------
    # @allure.story("广告层级跳转与筛选验证")
    # def test_ad_level_filter(self, ad_list_context):
    #     """验证跳转至广告层级并筛选当前用户"""
    #     ad_list_page = ad_list_context["ad_list_page"]
    #     account = ad_list_context["account"]
    #     game = ad_list_context["game"]
    #
    #     with allure.step("验证跳转至广告层级"):
    #         ad_list_page.page.locator(AdListLocators.AD_TAB).click()
    #         assert "ad" in ad_list_page.get_current_page_url(), "未跳转至广告层级"
    #
    #     with allure.step("验证默认筛选当前用户"):
    #         assert ad_list_page.is_current_user_filtered(), "未筛选当前用户"
    #
    #     with allure.step("验证筛选本批次账户"):
    #         ad_list_page.filter_by_account(account)
    #         assert ad_list_page.is_account_filtered(account), f"未筛选账户: {account}"
    #
    #     with allure.step("验证广告列表显示"):
    #         ad_count = ad_list_page.get_ad_count()
    #         assert ad_count > 0, "未找到符合条件的广告"