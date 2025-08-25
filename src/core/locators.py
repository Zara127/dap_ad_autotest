# 统一元素定位器
from dataclasses import dataclass

@dataclass
class AuthLocators:
    #选择登录方式
    ACCOUNT_PWD_LOGIN = "//p[contains(text(),'账户密码登录')]"
    # 登录页面元素
    USERNAME_INPUT = "input[placeholder='用户名']"
    PASSWORD_INPUT = "input[placeholder='密码']"
    LOGIN_BUTTON = "#app-viewport > div > div:nth-child(2) > div > div > div.login-password > button"
    # # 登录成功后的元素
    LOGIN_SUCCESS_INDICATOR = "div#main-viewport"  # 根据实际页面调整
    # # 登出相关元素
    # LOGOUT_BUTTON = "button:has-text('退出')"
    # LOGIN_PAGE_INDICATOR = "div.login-container"  # 登录页面的标志性元素


@dataclass
class HomeLocators:
    MAIN_CONTENT = "div#main-viewport"
    NAV_ITEMS = "#main-container > div.top-menu.flex-between-center > div:nth-child(1) > ul > div[data-class ='router-link-custom-class'] > a > li"
    # NAV_ITEMS = "div.top-menu ul > div > a > li"
    # div[data-class ='router-link-custom-class']

@dataclass
class CampaignLocators:
    """广告创建页面元素定位器"""
    # 页面标题与导航
    # PAGE_TITLE = "头条批量创建 - 表单-DAP"  #新版title
    # PAGE_TITLE_OLD = "批量创建-巨量引擎-DAP" #旧版title
    PAGE_TITLE = "text=批量创建"
    PAGE_TITLE_OLD = "text=巨量引擎/批量"

    BACK_OLD_BUTTON = "button:has-text('返回旧版')"

    # 1. 投放游戏与账户
    LIST_GAME_ACCOUNT = "li:has-text('投放游戏与账户')"
    GAME_ACCOUNT_SELECTOR = "#gameAndAccount"  #旧版
    GAME_ACCOUNT_SELECTOR_NEW = "#gameAccount" #新版
    GAME_SELECTOR_NEW = "#gameAccount div.ep-select__selection > div.ep-select__selected-item.ep-select__placeholder" #todo 新版，不能固定游戏名字
    GAME_IMG = "#gameAndAccount img"
    ACCOUNT_ADD = "button:has-text('添加账户')"
    ACCOUNT_FILL_NEW = "input[placeholder='请输入']" #新版
    ACCOUNT_FILL = "input[placeholder='请输入名称、ID或备注搜索']"
    # AACCOUNT_SEARCH_CONFIRM = "button:has-text('确认')"

    # 2. 营销目标与场景
    LIST_PURPOSE_SCENE = "li:has-text('营销目标与场景')"
    PURPOSE_SCENE_SELECTOR = "div#purposeAndScene"
    PURPOSE_SCENE_SELECTOR_NEW = "div#marketingScene"#新版
    PURPOSE_SCENE_LABEL = "#purposeAndScene label"
    PURPOSE_SCENE_LABEL_NEW = "#marketingScene label" #新版
    LABEL_LOCATOR = "label"
    # LANHAI_KEY = "role=textbox[name='添加蓝海关键词']"
    LANHAI_KEY = "button:has-text('添加蓝海关键词')"
    AUTO_KEY = "div:has-text('自定义关键词')"
    AUTO_KEY_INPUT = "input[placeholder='最多可输入10个关键词进行搜索']"
    LANHAI_BUTTON = "button:has-text('选择蓝海流量包')" #旧版
    LANHAI_BAG = "#marketingScene div:has-text('未选择蓝海流量包')"  # 新版，关联蓝海流量包区域
    LANHAI_BAG_SELECTOR = ".c-blue.hand:has-text('选择')" #新版,蓝海流量包 选择按钮

    # 3. 投放内容与目标
    LIST_CONTENT_TARGET = "li:has-text('投放内容与目标')"
    TASK_SELECTOR_BUTTON = "button:has-text('选择任务')" #旧版，关联星广联投任务
    STAR_TASK = "text=未选择星广联投任务" #新版，关联星广联投任务区域
    STAR_TASK_SELECTOR = ".c-blue.hand:has-text('选择')" #选择按钮
    APP_SELECTOR = "#targetBlock"
    APP_SELECTOR_NEW = "#deliveryGoal"  #新版
    APP_SELECTOR_BOX = "role=textbox[name='请选择']"
    APP_SELECTOR_BOX_NEW = "#deliveryGoal div.ep-select__selection > div.ep-select__selected-item.ep-select__placeholder"   #新版
    CONVERSION_BUTTON = "button:has-text('选择转化目标')" #旧版，转化目标按钮
    CONVERSION_AIM = "#deliveryGoal div:has-text('未选择转化目标')" #新版，转化目标区域
    CONVERSION_AIM_SELECTOR = ".c-blue.hand:has-text('选择')" #选择按钮
    CONVERSION_SEARCH_INPUT = "input[placeholder='请输入转化名称关键字']"
    CONVERSION_SEARCH_INPUT_NEW = "input[placeholder='请输入关键词']" #新版
    DEEP_CONVERSION_LABEL = "label:has-text('深度转化方式')"
    DEEP_CONVERSION_WAY = "span:has-text('每次付费+7日ROI')"

    # 4. 投放版位
    LIST_PLACEMENT = "li:has-text('投放版位')"
    PLACEMENT_SELECTOR = "#PlacementSpace"

    # 5. 用户定向
    LIST_USER_TARGETING = "li:has-text('用户定向')"
    USER_TARGETING_SELECTOR = "#placementAndTarget"
    TARGETING_PACK_SELECTOR = "a:has-text('选择定向包')" #旧版
    TARGETING_PACK_BUTTON = "button:has-text('添加定向包')" #新版
    TARGETING_SEARCH_INPUT = "input[placeholder='请输入']"  #新版
    TARGETING_SEARCH_BUTTON = "dialog[role='dialog'][name='用户定向'] i"

    # 6. 广告创意（旧版）/广告设置
    LIST_AD_SET_NEW = "li:has-text('广告设置')" #新版
    LIST_AD_SET = "li:has-text('广告创意')"
    ADMATERIAL_LABEL_SELECTOR = "#adMaterial label"
    ADMATERIAL_LABEL_SELECTOR_NEW = "#promotionSetting label"
    DOUYIN_SELECT_BUTTON = "button:has-text('选择抖音号')"
    # DOUYIN_DIV_PARENT = "div:has-text('投放抖音号')" #新版，投放抖音号父级模块div
    DOUYIN_SELECTOR_NEW = "span[placeholder='未选择抖音号']" #新版
    DOUYIN_SELECTOR_BUTTON_NEW = "../following-sibling::button" #新版xpath 兄弟层级定位
    # DOUYIN_SEARCH_INPUT = "input[placeholder='请输入名称、ID或备注搜索']"
    DOUYIN_SEARCH_INPUT = "role=textbox[name='请输入名称、ID或备注搜索']"
    DOUYIN_SEARCH_INPUT_NEW = "input[placeholder='请输入抖音号']" #新版
    DOUYIN_SEARCH_BUTTON = "dialog[role='dialog'][name='选择抖音号'] i"
    PRODUCT_NAME = "#adMaterial"
    PRODUCT_NAME_LABEL = "label:has-text('产品名称')"
    PRODUCT_NAME_CONTENT = ".. >> div.el-form-item__content"
    ADMATERIAL_IMG = "#adMaterial"
    TEXT_SUMMARY_INPUT = "input[placeholder='至少49个字符']"
    TEXT_SUMMARY = "button:has-text('摘要库')"
    TEXT_TEST = "testtesttesttesttesttesttesttesttesttesttesttesttest"


#素材组
    #新版
    MATERIAL_SELECT_BUTTON = "button:has-text('批量选择素材')"
    LANHAI_KEY_SELECTOR_SET = ".ep-select__selected-item:has-text('请选择蓝海关键词')"
    #【素材组设置】

    VIDEO= "div.drawer-content-inner div.ep-input__wrapper span:has-text('视频')"
    IMG =  "div.drawer-content-inner div.ep-input__wrapper span:has-text('图片')"
    GROUPIMG =  "div.drawer-content-inner div.ep-input__wrapper span:has-text('图文')"
    TEXT =  "div.drawer-content-inner div.ep-input__wrapper span:has-text('文案')"
    DOUYIN_VIDEO =  "div.drawer-content-inner div.ep-input__wrapper span:has-text('抖音视频')"
    DOUYIN_IMG =  "div.drawer-content-inner div.ep-input__wrapper span:has-text('抖音图文')"

    #【素材类别按钮】
    VIDEOBUTTON = "span.ep-tooltip__trigger:has-text('视频（'):has-text('）')"
    IMGBUTTON = "span.ep-tooltip__trigger:has-text('图片（'):has-text('）')"
    GROUPIMGBUTTON = "span.ep-tooltip__trigger:has-text('组图（'):has-text('）')"
    MUSICBUTTON = "span.ep-tooltip__trigger:has-text('音乐库（'):has-text('）')"
    TEXTBUTTON = "span.ep-tooltip__trigger:has-text('文案库（'):has-text('）')"
    DOUYIN_VIDEO_BUTTON = "span.ep-tooltip__trigger:has-text('抖音视频（'):has-text('）')"
    DOUYIN_IMG_BUTTON = "span.ep-tooltip__trigger:has-text('抖音图文（'):has-text('）')"



    #旧版[创意盒子]
    ADMATERIAL_BOX = "a:has-text('DAP创意')"
    DAP_DIALOG_SELECTOR = 'div.el-dialog__wrapper:has-text("DAP创意")'
    FIRST_CREATIVE_SELECTOR = '.image-list-wrap.el-row .image-item.hand.p-b-5.m-b-15.el-col.el-col-24' # DAP创意第一个素材
    DOUYIN_BOX_A = "a:has-text('抖音创意')"
    DOUYIN_BOX_BUTTON = "button:has-text('抖音号创意')"
    ADMATERIAL_BOX_SEARCH_INPUT = "input[placeholder='请输入素材、创意名称、文案或创建人搜索']"
    ADMATERIAL_BOX_SEARCH_BUTTON = "button.el-button el-button--default el-button--small is-plain"
    ADMATERIAL_BOX_SEARCH_RESULT_FIRST = ".creative-wp"
    ADMATERIAL_BOX_SEARCH_RESULT_FOURTH = "div:nth-child(4) > .creative-wp > .content"
    LAND_PAGE_SELECT_BUTTON = "a:has-text('添加落地页')" #旧版，添加落地页（a）
    LAND_PAGE_SELECT_BUTTON_NEW = "button:has-text('添加落地页')" #新版，添加落地页（button）
    LAND_PAGE_SEARCH_INPUT = "input[placeholder='请输入名称关键词']"
    LAND_PAGE_SEARCH_BUTTON = "dialog[role='dialog'] i"

    # 7. 搜索快投
    LIST_SEARCH = "li:has-text('搜索快投')"
    KEY_BAG_BUTTON = "button:has-text('选择关键词包')"
    KEY_BAG_SEARCH = "input[placeholder='请输入关键词包名称进行搜索']"
    BID_FACTOR_INPUT = "input[placeholder='请输入出价系数，不少于1.00，不超过2.00']"
    SEARCH_QUICK_LABEL = "#searchQuickPut label"

    # 8. 排期与预算
    LIST_SCHEDULE_BUDGET = "li:has-text('排期与预算')"
    SCHEDULE_AND_BUDGET = "#scheduleAndBudget"
    SCHEDULE_AND_BUDGET_NEW = "#scheduleBudget" #新版
    PRICE_STRATEGY = "label:has-text('竞价策略')"  #竞价策略
    DAILY_BUDGET_INPUT = "input[placeholder='请输入项目预算']"
    AD_DAILY_BUDGET_INPUT = "input[placeholder='请输入项目日预算']"
    AD_BUDGET_INPUT = "input[placeholder='请输入广告预算']"
    AD_BID_INPUT = "input[placeholder='请输入出价']"
    DEEP_ROI= "input[placeholder='请输入深度转化ROI系数']"

    # 9. 项目生成方式与标签
    LIST_GENERATION = "li:has-text('项目生成方式与标签')"
    GENERATION_TYPE = "select[name='generationType']"
    CAMPAIGN_TYPE = "select[name='campaignType']"
    CAMPAIGN_STATUS = "div[class*='campaign-status'] label:has-text('{0}')"
    AD_STATUS = "div[class*='ad-status'] label:has-text('{0}')"

    # 10. 提交按钮与结果
    LIST_SUBMIT = "li:has-text('广告预览与创建')"
    CAMPAIGN_TAG = "#generateWayAndTag svg"
    CAMPAIGN_TAG_NEW = "#projectGenTypeTag svg"
    PREVIEW_BUTTON = "button:has-text('预览广告')"

    # 11. 返回旧版按钮
    RETURN_OLD_VERSION_BUTTON = "button:has-text('返回旧版')"
    OLD_VERSION_PAGE_TITLE = "" #todo
    OLD_VERSION_CREATE_BUTTON = "" #todo


class PreviewLocators:
    LOADING_INDICATOR_OLD = "text=暂无数据"  #当前页面
    LOADING_INDICATOR = "text=数据加载中" #需求页面
    PREVIEW_TITLE = "text=广告结构预览"
    CREATE_BUTTON = "button:has-text('创建广告')"
    BACK_BUTTON = "button:has-text('返回上一页')"
    PLAY_BUTTON = "button:has-text('播放')"
    PAUSE_BUTTON = "button:has-text('暂停')"

    AD_PREVIEW_GRID = "#dataGrid"
    AD_PREVIEW_TITLE_OLD= "role=cell[name='创意预览']"  # 修改前
    AD_PREVIEW_TITLE_NOW = "role=cell[name='广告预览']"  # 修改后
    AD_SETTINGS_TITLE_OLD = "role=cell[name='创意设置']" # 修改前
    AD_SETTINGS_TITLE_NOW = "role=cell[name='广告设置']" # 修改后

    ACCOUNT_NAME = "div.account-name.m-b-10 span.text-ellipsis"
    PROJECT_NAME = ".el-table__fixed-body-wrapper > .el-table__body > tbody > tr > .el-table_6_column_30 > .cell > div:nth-child(2)"
    AD_NAME = ".el-table__fixed-body-wrapper > .el-table__body > tbody > tr:nth-child(2) > .el-table_6_column_30 > .cell > div"


class AdListLocators:
    LIST_TITLE = "text=新建项目"    # 示例，需替换为实际列表页标题
    CREATE_BUTTON = "button:has-text('批量创建')"

    GAME_SELECTOR = ".el-input__inner"
    FILTER_BAR = "#filter-bar"
    FILTER_SEARCH_INPUT = "input[placeholder='请输入名称、ID或备注搜索']"

    # AD_LIST_TABLE = "#app > div.el-table__fixed-body-wrapper > table.el-table__body > tr.el-table__row"
    AD_LIST_TABLE = ".dap-table-content > div:nth-child(2)"
    AD_NAME = ".el-table__fixed-body-wrapper > .el-table__body > tbody > tr:nth-child(2) > .el-table_12_column_117 > .cell"
    PROJECT_NAME = ".el-table__fixed-body-wrapper > .el-table__body > tbody > tr:nth-child(2) > .el-table_23_column_432 > .cell > .budget > .name"

    # 新增：筛选条件定位器
    CURRENT_USER_FILTER = "css=.filter-item:has-text('当前用户')"
    ACCOUNT_FILTER = "css=.filter-account"
    ACCOUNT_OPTION = lambda account: f"css=.filter-option:has-text('{account}')"
    ACCOUNT_FILTERED = lambda account: f"css=.active-filter:has-text('{account}')"
    PROJECT_FILTER = "css=.filter-project"
    PROJECT_OPTION = lambda project: f"css=.filter-option:has-text('{project}')"
    PROJECT_FILTERED = lambda project: f"css=.active-filter:has-text('{project}')"

    # 新增：广告列表定位器
    AD_ROWS = "css=.ad-row"
    AD_NAME_FIRST = "css=.ad-row:first-child .ad-name"