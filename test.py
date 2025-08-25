import os
print(os.getenv("TEST_AUTH_TOKEN"))

# 临时运行检查
from dotenv import load_dotenv
load_dotenv()  # 现在应该能正确加载
print("TOKEN:", os.getenv("TEST_AUTH_TOKEN"))

# 检查Token有效性
import requests
headers = {"Authorization": os.getenv("TEST_AUTH_TOKEN")}
response = requests.get("http://dap-staging-ad2.micro-stage.lilith.sh/ping", headers=headers)
print(response.status_code)  # 应该返回200


import yaml
from pathlib import Path
config_path = "C:\\Users\\zhousitian\\PycharmProjects\\dap_ad_autotest\\configs\\test.yaml"
with open(config_path) as f:
    content = f.read()
    print("文件内容：\n", content)
    config = yaml.safe_load(content)
    print("解析结果：", config)

# 手动测试Token（在Python控制台）
import requests
response = requests.get(
    "http://dap-staging-ad2.micro-stage.lilith.sh/advertise-2/home",
    headers={"Authorization": os.getenv("TEST_AUTH_TOKEN")}
)
print(response.status_code)  # 应为200，不是401/403