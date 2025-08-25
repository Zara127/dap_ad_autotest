ad-platform-autotest/
├── configs/                     # 配置文件
│   ├── dev.yaml                 # 开发环境配置
│   ├── test.yaml                # 测试环境配置
│   └── prod.yaml                # 生产环境配置
│
├── test_data/                   # 测试数据
│   ├── ui/                      
│   │   ├── ad_campaigns/        # 广告活动测试数据
│   │   ├── creatives/           # 创意素材测试数据
│   │   └── targeting/           # 定向条件测试数据
│   │
│   └── api/
│       ├── positive_cases/      # 正向测试用例数据
│       ├── negative_cases/      # 异常测试用例数据
│       └── performance/         # 性能测试数据
│
├── src/                         # 核心代码
│   ├── common/                  # 公共组件
│   │   ├── logger.py            # 日志模块
│   │   ├── exceptions.py        # 自定义异常
│   │   └── utils.py             # 工具函数
│   │
│   ├── core/                    # 核心框架
│   │   ├── base_page.py         # 页面基类(POM)
│   │   ├── base_api.py          # API请求基类
│   │   └── locators.py          # 统一元素定位器
│   │
│   ├── pages/                   # 页面对象(UI)
│   │   ├── login_page.py        
│   │   ├── dashboard_page.py    
│   │   ├── campaign_page.py     
│   │   └── reporting_page.py    
│   │
│   ├── api/                     # API接口封装
│   │   ├── auth_api.py          # 认证接口
│   │   ├── campaign_api.py      # 广告活动接口
│   │   └── reporting_api.py     # 报表接口
│   │
│   └── services/                # 业务服务层
│       ├── campaign_service.py  # 广告活动服务
│       └── user_service.py      # 用户服务
│
├── tests/                       # 测试用例
│   ├── ui/                      
│   │   ├── login/               
│   │   ├── campaign_management/ 
│   │   └── reporting/           
│   │
│   ├── api/                     
│   │   ├── test_auth.py         
│   │   ├── test_campaigns.py    
│   │   └── test_reports.py      
│   │
│   └── integration/             # 集成测试
│       ├── test_flow_create_campaign.py
│       └── test_flow_report_generation.py
│
├── reports/                     # 测试报告
│   ├── html/                    # HTML报告
│   ├── screenshots/             # 失败截图
│   └── videos/                  # 执行录像(可选)
│
├── requirements.txt             # Python依赖
├── pytest.ini                  # Pytest配置
├── README.md                   # 项目文档
└── .gitignore                  # Git忽略规则