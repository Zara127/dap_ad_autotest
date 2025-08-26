# Pytest Fixture定义
# pytest.ini 配套文件
import datetime
import subprocess
import time
from pathlib import Path

import pytest
import allure
from playwright.sync_api import Page, BrowserContext, Playwright
from src.pages.home_page import HomePage
from src.pages.campaign_page import CampaignPage
from src.pages.old_campaign_page import OldCampaignPage

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

# 失败截图基础配置
SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)  # parents=True：创建多级目录；exist_ok=True：避免目录已存在报错

@pytest.fixture(scope="function", autouse=True)
def capture_screenshot_on_failure(request, authenticated_context: BrowserContext):
    """
    全局自动截图 Fixture：
    - scope="function"：每个用例执行一次（确保每个用例截图独立）
    - autouse=True：无需手动调用，所有用例自动生效
    - 依赖 authenticated_context：获取当前活跃页面进行截图
    """
    yield

    # 1. 判断用例是否失败（仅在“调用阶段”失败时截图，排除 setup/teardown 失败）
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # 2. 生成唯一截图文件名（用例名 + 时间戳，避免参数化用例截图重名）
        case_name = request.node.name.replace("[", "_").replace("]", "_").replace("/", "_") # 处理参数化用例名中的特殊字符（如 [ ] 替换为 _）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # 时间戳（精确到秒，避免同一用例多次失败截图覆盖）
        screenshot_path = SCREENSHOT_DIR / f"{case_name}_{timestamp}.png" # 最终截图路径

        # 3. 获取当前活跃页面（从 authenticated_context 中获取最后一个打开的页面），避免因多页面切换导致截图错页
        page = authenticated_context.pages[-1] if authenticated_context.pages else None
        if not page:
            allure.attach("截图失败：当前无活跃页面", name="截图异常", attachment_type=allure.attachment_type.TEXT)
            return

        # 4. 执行截图（Playwright 核心 API，full_page=True 截取全页面，包括滚动区域）
        try:
            page.screenshot(
                path=str(screenshot_path),
                full_page=True,  # 关键：截取完整页面，而非仅视口内内容
                timeout=10000    # 截图超时时间（10秒，避免网络波动导致截图失败）
            )
        except Exception as e:
            # 截图本身失败时，记录异常到 Allure 报告
            allure.attach(f"截图执行失败：{str(e)}", name="截图异常", attachment_type=allure.attachment_type.TEXT)
            return

        # 5. 关联截图到 Allure 报告（点击失败用例可查看截图）
        allure.attach.file(
            source=str(screenshot_path),
            name=f"用例失败截图_{timestamp}",
            attachment_type=allure.attachment_type.PNG,  # 明确附件类型为图片
            extension="png"  # 附件扩展名
        )

        # 6. （可选）关联截图到 HTML 报告（如果使用 pytest-html 插件）
        if hasattr(request.config, "_html"):
            # 内嵌截图到 HTML 报告，设置最大宽度便于查看
            request.config._html.append(
                f'<div style="margin:10px 0;">'
                f'<h4>失败截图：</h4>'
                f'<img src="{screenshot_path}" alt="用例失败截图" style="max-width:800px;border:1px solid #eee;">'
                f'</div>'
            )

# Pytest 钩子函数（标记用例执行结果）
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子函数：记录用例执行结果（setup/call/teardown）
    作用：为 capture_screenshot_on_failure Fixture 提供用例失败状态判断依据
    """
    # 获取用例执行报告
    outcome = yield
    rep = outcome.get_result()

    # 将报告结果挂载到 item 对象上（供后续 Fixture 访问）
    setattr(item, f"rep_{rep.when}", rep)



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
    hp = HomePage(page)
    # 验证页面是否正确加载
    assert hp.is_loaded(), "主页未正确加载"
    yield hp


@pytest.fixture(scope="class")
def campaign_page(home_page):
    """从主页导航到广告创建页面"""
    campaign_page = home_page.click_create_btn(platform='巨量引擎')
    # 验证新版广告创建页面是否正确加载
    assert isinstance(campaign_page, CampaignPage), "未成功导航到广告创建页面"
    assert campaign_page.is_loaded(), "广告创建页面未正确加载"
    yield campaign_page

@pytest.fixture(scope="class")
def old_campaign_page(campaign_page):
    """从新版广告创建页面到旧版广告创建页面"""
    old_campaign_page = campaign_page.click_return_old_version()
    # 验证旧版广告创建页面是否正确加载
    assert isinstance(old_campaign_page, OldCampaignPage), "未成功导航到旧版广告创建页面"
    assert old_campaign_page.is_loaded(), "旧版广告创建页面未正确加载"
    yield old_campaign_page


