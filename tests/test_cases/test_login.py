# 测试login文件
from src.core.auth_page import AuthPage


def test_login(page):
    auth = AuthPage(page)
    auth.navigate("/login")  # 导航到登录页
    # 执行登录
    auth.login()

    # 验证登录成功
    assert auth.is_logged_in()
