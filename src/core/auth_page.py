from src.common.utils import load_config
from src.core.base_page import BasePage
from src.core.locators import AuthLocators

#登录页
class AuthPage(BasePage):
    def __init__(self, page, env='test'):
        super().__init__(page, env)


    def login(self):
        """使用账号密码登录"""
        # 读取test.yaml文件获取账号信息
        config = load_config(self.env)
        username = config['test']['auth']['username']
        password = config['test']['auth']['password']

        self.page.click(AuthLocators.ACCOUNT_PWD_LOGIN)
        print("已点击‘账户密码登录’按钮")

        self.page.fill(AuthLocators.USERNAME_INPUT, username)
        print(f"已输入用户名")

        self.page.fill(AuthLocators.PASSWORD_INPUT, password)
        print("已输入密码")

        self.page.click(AuthLocators.LOGIN_BUTTON)
        # self.page.get_by_role("button", name="登录").click()
        print("已点击登录按钮")

        # 接口验证登录请求是否成功
        # with self.page.expect_response("**/api/login") as response_info:
        #     self.page.get_by_role("button", name="登录").click()
        # response = response_info.value
        # print(f"登录API状态码: {response.status}")
        # print(f"登录API响应: {response.json()}")
        # if response.status != 200:
        #     raise Exception(f"登录失败: {response.json().get('message', '未知错误')}")

        # # 等待会话验证完成
        # self.page.wait_for_function(
        #     """
        #     () => {
        #         // 检查 localStorage/sessionStorage 中的 token
        #         const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
        #         // 检查页面是否存在登录成功后的元素
        #         const dashboard = document.querySelector('.main-container');
        #         return token && dashboard;
        #     }
        #     """,
        #     timeout=15000
        # )


    # def wait_for_login_complete(self):
    #     """等待登录完成，验证登录成功的标志"""
    #     try:
    #         # 等待登录成功后才会出现的元素
    #         self.page.wait_for_selector(AuthLocators.LOGIN_SUCCESS_INDICATOR, timeout=10000)
    #         print("登录成功")
    #     except TimeoutError:
    #         # 登录失败处理
    #         if self.page.query_selector(AuthLocators.LOGIN_ERROR_MESSAGE):
    #             error_msg = self.page.query_selector(AuthLocators.LOGIN_ERROR_MESSAGE).text_content()
    #             raise Exception(f"登录失败: {error_msg}")
    #         else:
    #             raise Exception("登录超时，未检测到登录成功标志")
    #
    def is_logged_in(self):
        """检查是否已登录"""
        return self.page.is_visible(AuthLocators.LOGIN_SUCCESS_INDICATOR)
    #
    # def logout(self):
    #     """退出登录"""
    #     self.page.click(AuthLocators.LOGOUT_BUTTON)
    #     self.page.wait_for_selector(AuthLocators.LOGIN_PAGE_INDICATOR)
    #     print("已退出登录")