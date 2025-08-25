# pytest.ini 配套文件
import subprocess
import time
from pathlib import Path

import pytest
import allure
from playwright.sync_api import Page

# 在conftest.py中添加以下fixture【测试文件共享】
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """强制覆盖浏览器启动参数"""
    return {
        **browser_type_launch_args,
        "headless": False,
        "channel":"chromium",
        "slow_mo": 1000,
        "args": ["--start-maximized"]
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """强制覆盖上下文参数"""
    return {
        **browser_context_args,
        "no_viewport": True,  # 禁用固定视口，让 --start-maximized 生效
        "ignore_https_errors": True #忽略https错误
    }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """自动附加失败截图到Allure报告"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="失败截图",
                attachment_type=allure.attachment_type.PNG
            )


@pytest.fixture(scope="session")  # session 作用域：整个测试会话只执行一次
def authenticated_context(browser, base_url):
    """创建已登录的浏览器上下文，全局共享"""
    context = browser.new_context()
    page = context.new_page() #创建唯一的page实例

    # 使用AuthPage执行登录（只执行一次）
    from src.core.auth_page import AuthPage
    auth = AuthPage(page)
    auth.navigate("/login")
    auth.login()

    # 确保主页被正常加载
    if page.url != f"{base_url}/advertise-2/home":
        page.reload()

    yield context   # 保存登录后的上下文
    context.close()  # 测试结束后关闭上下文


@pytest.fixture(scope="class")
def home_page(authenticated_context):
    """使用已登录的上下文和现有page实例"""
    page = authenticated_context.pages[0]  # 获取已存在的page

    # 无需再次导航，直接创建HomePage实例
    from src.pages.home_page import HomePage
    hp = HomePage(page)

    # 验证页面是否正确加载
    assert hp.is_loaded(), "主页未正确加载"

    yield hp


@pytest.fixture(scope="class")
def campaign_page(home_page):
    """从主页导航到广告创建页面"""

    # 点击创建按钮导航到广告创建页面
    campaign_page = home_page.click_create_btn(platform='巨量引擎')

    # 验证广告创建页面是否正确加载
    from src.pages.campaign_page import CampaignPage
    assert isinstance(campaign_page, CampaignPage), "未成功导航到广告创建页面"
    assert campaign_page.is_loaded(), "广告创建页面未正确加载"
    yield campaign_page



