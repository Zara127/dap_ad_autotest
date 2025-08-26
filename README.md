# 项目结构
dap-ad-autotest/
├── configs/                     # 配置文件
│   └── test.yaml                # 测试环境配置
│
├── src/                         # 核心代码
│   ├── common/                  # 公共组件
│   │   ├── logger.py            # 日志模块
│   │   ├── exceptions.py        # 自定义异常
│   │   └── utils.py             # 工具函数
│   │
│   ├── core/                    # 核心框架
│   │   ├── base_page.py         # 页面基类(POM)
│   │   ├── auth_page.py         # 登录页面
│   │   └── locators.py          # 统一元素定位器
│   │
│   ├── pages/                   # 页面对象(UI)
│   │   ├── home_page.py         # 主页
│   │   ├── campaign_page.py     # 新版批量创建页*
│   │   ├── old_campaign_page.py # 旧版批量创建页*
│   │   ├── preview_page.py      # 预览页
│   └── └── adlist_page.py       # 广告列表页
│
├── tests/                       # 测试数据&测试用例
│   ├── test_data/                      
│   │   ├── base_data.yaml       # 基础字段数据
│   └── └── scenarios.yaml       # 场景字段数据
│   │
│   ├── test_cases/                      
│   │   ├── test_login.py        
│   │   ├── test_home.py         
│   │   ├── test_campaign.py     # 新版
│   │   ├── test_campaign_old.py # 旧版
│   │   ├── test_preview.py      
│   └── └── test_adlist.py       
│ 
├── reports/                     # 测试报告
│   ├── allure-report/           # Allure报告
│   ├── allure-results/          
│   ├── html/                    # HTML报告
│   ├── screenshots/             # 失败截图
│   └── videos/                  # 执行录像(可选)
│
├── requirements.txt             # Python依赖
├── pytest.ini                   # Pytest配置
├── conftest.py                  # pytest.ini 配套文件
└── README.md                    

# 执行测试用例
pytest tests/test_cases/test_campaign.py -s -v --alluredir=reports/allure-results
pytest tests/test_cases/test_campaign_old.py -s -v --alluredir=reports/allure-results

# 生成allure报告到指定目录下（不自动打开）
allure generate allure-results -o reports/allure-report --clean 

# 生成allure报告到指定目录下（默认打开浏览器）
allure serve reports/allure-results

# 生成html报告
pytest tests/test_cases/test_campaign.py -s -v --html=reports/html/report.html
pytest tests/test_cases/test_campaign_old.py -s -v --html=reports/html/report.html

