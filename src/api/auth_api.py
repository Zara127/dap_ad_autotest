import requests
from src.common.logger import get_logger
from src.common.utils import load_config

logger = get_logger(__name__)


class AuthAPI:
    def __init__(self):
        self.config = load_config()['test']
        self.base_url = self.config['api_url']

    def get_token(self, username=None, password=None):
        """获取认证token"""
        creds = {
            "username": username or self.config['credentials']['admin']['username'],
            "password": password or self.config['credentials']['admin']['password']
        }
        response = requests.post(
            f"{self.base_url}/auth/login",
            json=creds,
            timeout=10
        )
        response.raise_for_status()
        token = response.json()['data']['token']
        logger.info("成功获取认证token")
        return token