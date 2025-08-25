#批量创建页面[旧版]
#包含页面具体操作方法、验证元素存在方法、页面加载状态。。。
import re
from itertools import product
from click.decorators import CmdType
from conftest import campaign_page
from src.core.base_page import BasePage
from src.core.locators import CampaignLocators
from src.pages.preview_page import PreviewPage


class OldCampaignPage(BasePage):
    """旧版巨量引擎-批量创建页面操作类"""
    def __init__(self, page):
        super().__init__(page)

    def is_loaded(self):
        """验证页面是否加载完成"""
        # return self.page.is_visible(CampaignLocators.PAGE_TITLE)
        return self.page.title()==CampaignLocators.PAGE_TITLE_OLD

    def get_current_page_url(self):
        """获取当前页面 URL，用于判断跳转"""
        return self.page.url

    def create_campaign(self, test_data):
        """旧版页面执行批量创建流程"""

        #调换1、2两个部分字段的操作顺序，解决切换【推广目的】【营销场景】字段值导致账户清空的问题，避免导致后续数据为空
        #顺序为：先【关联游戏】、再【营销目标与场景】、最后【投放账户】


        # 1.1关联游戏
        self.set_game(test_data["game"])

        # 2. 营销目标与场景【推广目标、投放类型、营销场景、广告类型、投放模式、】
        self.set_purpose_and_scene(
            test_data["purpose"],
            test_data.get("sub_purpose"),
            test_data["scene"],
            test_data["ad_type"],
            test_data["delivery_mode"],
            test_data["game"]
        )

        # 1.2 投放账户
        self.set_account(test_data["account"])

        # 3. 投放内容与目标【星广联投任务、应用类型、推广应用、转化目标】
        if "star_task" in test_data:
            self.set_content_and_target(
                test_data["app_type"],
                test_data["star_task"]
            )
        else:
            self.set_content_and_target(test_data["app_type"])

        # 4. 投放版位【投放位置、媒体选择】
        if test_data["ad_type"] == "通投广告"  and test_data["delivery_mode"] == "手动投放":
            self.set_placement(
                test_data["placement"],
                test_data.get("media_options")
            )

        # 5.用户定向【定向盒子、过滤已转化、过滤时间、】
        if test_data["filter_type"] == "公司账户" or test_data["filter_type"] == "APP":
            self.set_targeting(
                filter_type=test_data["filter_type"],
                filter_days=test_data["filter_days"]
            )
        else:
            self.set_targeting(
                filter_type=test_data["filter_type"],
            )

        # 6. 广告创意【原生广告投放、创意盒子/素材组、产品名称、产品主图、产品卖点、行动号召】
        if "native_ad" in test_data:
            native_ad=test_data["native_ad"]
        else:
            native_ad = None
        if "material_type" in test_data:
            material_type = test_data["material_type"]
        else:
            material_type = None
        if test_data["app_type"] == "安卓应用":
            land_page = test_data["app_type"]
        else:
            land_page = None

        #搜索-极速智投、搜索-常规投放，需要文本摘要
        if test_data["ad_type"]== "搜索广告":
            text_summary = "文本摘要"
        else:
            text_summary = None
        self.set_creative(native_ad=native_ad, game=test_data['game'], land_page = land_page, material_type=material_type,text_summary=text_summary)


        # 7. 排期与预算【投放时间、投放时段、竞价策略、项目预算、付费方式 / 竞价策略、广告预算、广告出价】
        if test_data["ad_type"] == "通投广告" and test_data["delivery_mode"] == "自动投放":  #没有项目预算选项
            budget_type = None
            daily_budget = None
        else:
            budget_type = test_data["budget_type"]
            if test_data["budget_type"] == "不限":  # 没有日预算
                daily_budget = None
            else:
                daily_budget = test_data["daily_budget"]
        self.set_budget(
            time=test_data["time"],
            time_period=test_data["time_period"],
            bidding_strategy=test_data["bidding_strategy"],
            daily_budget=daily_budget,
            ad_budget=test_data["ad_budget"],
            ad_bid=test_data["ad_bid"],
            budget_type=budget_type
        )



        # 8.设置搜索快投/搜索广告：【只考虑通投广告-手动投放即可】
        # 搜索快投：仅通投广告-手动投放需要：【(出价系数、定向拓展)】
        # 搜索广告-常规投放：智能拓流、动态创意【只有开启选项，无需设置】
        if test_data["ad_type"] == "通投广告" and test_data["delivery_mode"] == "手动投放":
            self.set_search_express(
                test_data["bid_factor"],
                test_data["expansion"]
            )

        # 9. 项目生成方式与标签【项目生成方式、投放类型、/+（项目启停设置、广告启停设置）】
        # 直播-直播素材，项目生成方式 只有“按受众”选项可以选择【存在默认选择，就可以不进行操作】
        self.set_generation(
            test_data["generation_type"],
            test_data["campaign_type"],
            test_data["campaign_status"],
            test_data["ad_status"]
        )

        # 10. 广告预览与创建【另存为新草稿、预览按钮】
        # self.page.get_by_role("button", name="提交").click()
        # 提交创建
        # self.click_element(CampaignLocators.SUBMIT_BUTTON)

        # 验证创建成功
        return self._verify_creation_success()

    # 跳转页面-预览页
    def click_preview_button(self):
        """点击「预览广告」按钮，返回预览页面对象"""
        self.click_element(CampaignLocators.PREVIEW_BUTTON)
        self.page.wait_for_load_state("networkidle") # 等待预览页加载完成
        return PreviewPage(self.page)



    def set_game(self, game):
        """1.1选择关联游戏"""
        self.page.locator(CampaignLocators.GAME_ACCOUNT_SELECTOR).get_by_role("textbox", name="请选择").click()
        self.page.locator("div").filter(has_text=game).nth(3).click()   #下拉列表选择

    def set_account(self, account):
        """1.2 选择投放账户"""
        # 投放账户
        self.click_element(CampaignLocators.ACCOUNT_ADD) #点击按钮
        self.fill_input(CampaignLocators.ACCOUNT_FILL, account) #输入账户
        self.page.get_by_role("dialog", name="选择账户").locator("i").nth(1).click() #点击搜索
        self.page.wait_for_load_state("networkidle") # 等待页面加载完成
        self.page.get_by_role("row", name=account).locator("span").nth(1).click() #勾选出现的第一个
        self.page.mouse.wheel(0, 100)  # 向下滑动鼠标,向下滑动 100 像素
        self.page.get_by_role("button", name="确认").click() # 点击确认

    def set_purpose_and_scene(self, purpose, sub_purpose, scene, ad_type, delivery_mode,game):
        """2.选择营销目标与场景【(推广目的、投放类型)、营销场景、广告类型、投放模式】"""
        self.click_element(CampaignLocators.LIST_PURPOSE_SCENE)
        # 推广目的
        self.page.locator(CampaignLocators.PURPOSE_SCENE_SELECTOR).filter(has_text=purpose).click()
        # 投放类型/子目标
        if sub_purpose:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=sub_purpose).click()
        #营销场景
        if scene == "直播":  #否则会匹配到两个元素
            self.page.locator(CampaignLocators.PURPOSE_SCENE_LABEL).filter(has_text=scene).click()
        else:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=scene).click()
        #广告类型
        self.page.locator(CampaignLocators.PURPOSE_SCENE_LABEL).filter(has_text=ad_type).click()  # 修改了定位器，按照原来的，搜索-常规 会定位2个元素
        #投放模式
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=delivery_mode).click()

        #搜索广告-极速智投，新增蓝海关键词选项（非必选）

        #如果是搜索广告-常规投放，需要选择蓝海流量包（必选）
        lanhai_button = self.page.locator(CampaignLocators.LANHAI_BUTTON)
        if lanhai_button.is_visible():
            lanhai_button.click()
            self.page.locator(f'role=row[name*="{game}"]').get_by_role("radio").click()
            self.page.get_by_role("button", name="确认").click()


    def set_content_and_target(self, app_type,star_task=None):
        """3.投放内容与目标【应用类型、推广应用、转化目标】"""
        self.click_element(CampaignLocators.LIST_CONTENT_TARGET)
        # 非必须字段：关联星广联投任务＜（＾－＾）＞[营销场景十一 选择该字段，会影响后续广告/创意设置]
        if star_task:
            self.click_element(CampaignLocators.TASK_SELECTOR_BUTTON) # 选择关联星广联投任务
            self.page.get_by_text("战火勋章25年6月星广联投素材-常规剪辑赛道-芦鸣").click()  # 设置固定选一个任务
            self.page.get_by_role("button", name="确认").click()  # 确认按钮
        #选择应用类型
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=app_type).click()
        # 推广应用是否固定选择？？？ 暂时按照文字匹配选择第一个 ＜（＾－＾）＞
        self.page.locator(CampaignLocators.APP_SELECTOR).locator(CampaignLocators.APP_SELECTOR_BOX).click()
        if app_type == "安卓应用":
            self.page.get_by_text("中国-安卓",exact=False).first.click()
        else:
            self.page.locator("text=/.*中国-(ios|苹果|iOS).*/i").click()
        # 选择具体的转化目标 【可以自己新建test转化目标{test_zst}，也可以选择带有公测的】
        if self.page.locator(CampaignLocators.CONVERSION_BUTTON).is_visible():
            self.click_element(CampaignLocators.CONVERSION_BUTTON)
            #如果在搜索前可见“test_zst”，则直接点击；否则再进行搜索选择
            if self.page.get_by_text("test_zst").is_visible():
                self.page.get_by_text("test_zst").click()
            else:
                self.fill_input(CampaignLocators.CONVERSION_SEARCH_INPUT,"test_zst")
                self.page.locator(
                    ".search-wrap > .el-input > .el-input__suffix > .el-input__suffix-inner > .el-input__icon").click()
                self.page.get_by_role("dialog").locator("tbody").get_by_role("cell").filter(has_text=re.compile(r"^$")).locator(
                    "span").click()
            self.page.get_by_role("button", name="确认").click()

    def set_placement(self, position, media_options):
        """4. 投放版位【投放位置、媒体选择】"""
        self.click_element(CampaignLocators.LIST_PLACEMENT)
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=position).click()# 选择投放位置
        # 如果是首选媒体，选择具体媒体【默认全选,不需要操作】
        # if position == "首选媒体" and media_options:
        #     for media in media_options:
        #         self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=media).locator("span").nth(1).click()

    def set_targeting(self, filter_type, filter_days=None):  #targeting_num参数
        """5.用户定向【定向盒子、过滤已转化、过滤时间】"""
        self.click_element(CampaignLocators.LIST_USER_TARGETING)
        #TODO 定向盒子[定向盒子的数量、选择] ？？？
        # 【搜索test选择】＜（＾－＾）＞
        # if targeting_num == 1:
        #     # 若只有一个定向盒子，则直接点击选择定向包
        #     self.click_element(CampaignLocators.TARGETING_PACK_SELECTOR) #点击选择定向包
        # self.page.get_by_role("button",name="取消").click()
        self.click_element(CampaignLocators.TARGETING_PACK_SELECTOR)  # 点击选择定向包
        # 如果在搜索前可见“test_zst”，则直接选择；否则再进行搜索选择
        if self.page.get_by_title("dap内部自动化测试").is_visible():
            self.page.get_by_title("dap内部自动化测试").click()
        else:
            self.fill_input(CampaignLocators.TARGETING_SEARCH_INPUT,"test_zst") #输入“test_zst”
            # self.page.locator(CampaignLocators.TARGETING_SEARCH_BUTTON).nth(2).click() #点击搜索按钮
            self.page.locator(CampaignLocators.TARGETING_SEARCH_INPUT).press("Enter") #回车搜索
            self.page.get_by_role("row", name=re.compile("test")).first.locator("use").click()  # 选择匹配到的第一个
        self.page.get_by_role("button", name="确认").click() #确认按钮

        self.page.mouse.wheel(0,200)

        # 过滤已转化
        if filter_type == "不限" or filter_days == "广告":
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=re.compile(rf"^{filter_type}$")).click()
        else:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=filter_type).click()
        # 过滤时间[与过滤已转化的取值有关]
        if filter_days:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=filter_days).click()


    def set_creative(self, native_ad=None,game=None, material_type=None,land_page=None,text_summary=None):
        """6.广告创意/广告设置（根据场景选择原生广告或素材类型）【原生广告投放、创意盒子/素材组、产品名称、产品主图、产品卖点、行动号召】"""
        self.click_element(CampaignLocators.LIST_AD_SET)
        # 短视频+图文场景有原生广告开关；直播场景有素材类型选择
        # 选择原生广告投放
        if native_ad:
            self.page.locator(CampaignLocators.ADMATERIAL_LABEL_SELECTOR).filter(has_text=native_ad).click()
        # 选择抖音号
        douyin_selector = self.page.locator(CampaignLocators.DOUYIN_SELECT_BUTTON)
        if douyin_selector.is_visible():
            douyin_selector.click()  # 点击选择抖音号按钮
            self.page.wait_for_load_state("networkidle")
            # 如果当前页面包含game名称的抖音号是可见的,则直接选择；否则再通过搜索选择
            if material_type:
                name = f"{game}-天下 68553950326 抖音号授权"
            else:
                name = f"{game}"
            game_douyin_account = self.page.get_by_role("row", name=name).locator("use").first
            if game_douyin_account.is_visible():
                game_douyin_account.click()  # 选择匹配到的第一个
                self.page.get_by_role("button", name="确认").click()  # 确认按钮
            else:
                self.fill_input(CampaignLocators.DOUYIN_SEARCH_INPUT, name)  # 在搜索框输入游戏名 #指定name
                self.page.locator(CampaignLocators.DOUYIN_SEARCH_INPUT).press("Enter")  # 回车搜索
                self.page.get_by_role("row", name=re.compile(game)).first.locator("use").click()  # 选择匹配到的第一个
                self.page.get_by_role("button", name="确认").click()  # 确认按钮

        #选择素材类型
        if material_type:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=material_type).click()


        #TODO
        # 创意盒子/素材组【现有页面和需求文档上的不一致，暂无法按照需求文档上的编写】 ＜（＾－＾）＞
        # 创意盒子一般在选择的时候可以输入"测试"进行选择；没有的话其他的也可以选；也可以在创意中心中自己创建
        # todo: 可以更改dap创意与抖音素材选择的逻辑：
        #  先判断抖音创意是否可见，可见则选抖音素材，且不需要再选择dap素材，不可见则进一步判断dap创意是否可见；
        #  dap创意可见则选择dap素材，不可见则不需要选择。
        #选择dap创意[直播-素材形式为直播素材时不需要选择dap创意][营销场景十一：选择关联星广联投任务后，也不需要选择dap创意]
        #【直接选择第一个素材】
        # if material_type == None and material_type != "直播素材":
        if self.page.locator(CampaignLocators.ADMATERIAL_BOX).is_visible(): #若dap创意可见，则进行选择
            self.click_element(CampaignLocators.ADMATERIAL_BOX) #点击dap创意按钮
            dap_dialog = self.page.locator(CampaignLocators.DAP_DIALOG_SELECTOR)  # 定位DAP创意弹窗容器
            dap_dialog.wait_for(state="visible", timeout=5000)
            first_creative = dap_dialog.locator(CampaignLocators.FIRST_CREATIVE_SELECTOR).first # 定位dap弹窗内的第一个素材卡片
            first_creative.wait_for(state="visible", timeout=30000)
            self.page.wait_for_load_state("networkidle")
            # 直接选择dap弹窗中的第一个素材
            if first_creative.count() != 0:
                first_creative.click()
            else:
                print("dap创意中暂无数据")
            # self.fill_input(CampaignLocators.ADMATERIAL_BOX_SEARCH_INPUT, "测试") #输入测试选择素材
            # self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_INPUT).press("Enter") #回车搜索
            # self.page.wait_for_load_state("networkidle")
            # admaterial_search_first = self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_RESULT_FIRST).first
            # if admaterial_search_first.is_visible():
            #     self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_RESULT_FIRST).click()  # 点击搜索后指定固定素材
            # else:
            #     self.fill_input(CampaignLocators.ADMATERIAL_BOX_SEARCH_INPUT, "公测")
            #     self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_INPUT).press("Enter")  # 回车搜索
            #     self.page.wait_for_load_state("networkidle")
            #     admaterial_search_first = self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_RESULT_FIRST).first
            #     if admaterial_search_first.is_visible(): #搜索{公测}
            #         self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_RESULT_FOURTH).click()  # 点击搜索后指定固定素材
            #     else: #搜索{测试/公测}后没有结果，则在主页任选一个
            #         self.fill_input(CampaignLocators.ADMATERIAL_BOX_SEARCH_INPUT, "")
            #         self.page.locator(CampaignLocators.ADMATERIAL_BOX_SEARCH_INPUT).press("Enter")  # 回车搜索
            #         self.page.wait_for_load_state("networkidle")
            #         self.page.get_by_text("公测-测新").first.click()  #固定选择
            self.page.get_by_role("button", name="确认").click()
        #选择抖音号创意/抖音创意[注：目前页面有两种形式ui]
        douyin_a = self.page.locator(CampaignLocators.DOUYIN_BOX_A)
        douyin_button = self.page.locator(CampaignLocators.DOUYIN_BOX_BUTTON)
        if douyin_a.is_visible(): #若抖音创意可见，则进行选择
            douyin_a.click() #点击抖音创意
            self.page.get_by_title("媒体素材ID:").first.click() #任意选择一个[固定]
            self.page.get_by_role("button", name="确认").click()
        if douyin_button.is_visible(): #若抖音号创意可见，则进行选择[选择关联星广联投任务]
            douyin_button.click() #点击抖音号创意
            self.page.get_by_title("媒体素材ID: ").first.click() #任意选择一个[固定]
            self.page.get_by_role("button", name="确认").click()

        #如果是搜索广告-常规投放，则需要选择蓝海关键词
        if self.page.locator(CampaignLocators.LANHAI_KEY_SELECTOR).is_visible():
            self.click_element(CampaignLocators.LANHAI_KEY_SELECTOR)
            self.page.get_by_text("优选 游戏下载 预估消耗（元）").click() #任意选一个

        # TODO 如果应用类型为安卓应用，则需要选择落地页【test】  ＜（＾－＾）＞
        if land_page:
            self.click_element(CampaignLocators.LAND_PAGE_SELECT_BUTTON) #点击选择落地页按钮
            self.fill_input(CampaignLocators.LAND_PAGE_SEARCH_INPUT,"test")
            self.page.locator(CampaignLocators.LAND_PAGE_SEARCH_INPUT).press("Enter")
            self.page.get_by_role("row", name=re.compile("test")).first.locator("span").nth(1).click() #选择匹配到的第一个
            self.page.get_by_role("button", name="确定").click()

        if text_summary:
            # 如果营销场景是搜索-极速智投、搜索-常规投放 需要选择【文本摘要】
            self.click_element(CampaignLocators.TEXT_SUMMARY)  # 点击摘要库
            self.page.get_by_role("row").nth(1).locator("span").nth(1).click() #勾选第一行
            self.page.get_by_role("button", name="确 定").click()

        #添加鼠标滚动
        self.page.mouse.wheel(0, 100)

        # TODO产品名称、产品主图  检验是否与game相符合【当素材形式为直播素材时，没有这两个字段】
        if material_type == None or material_type != "直播素材":
            # product_name = self.page.locator("#adMaterial").get_by_role("textbox").first.text_content()
            # assert product_name == game,"产品名称与关联游戏名称不符"
            product_img = self.page.locator(CampaignLocators.ADMATERIAL_IMG).get_by_role("img")
            game_img = self.page.locator(CampaignLocators.GAME_IMG)
            assert product_img.get_attribute("src") == game_img.get_attribute("src"),"产品主图与关联游戏图片不符"
            # 产品卖点、行动号召  默认即可 不需要操作


    def set_budget(self, time, time_period, bidding_strategy, ad_budget, ad_bid, daily_budget=None,budget_type=None):
        """7.设置排期与预算"""
        self.click_element(CampaignLocators.LIST_SCHEDULE_BUDGET)
        #投放时间
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=time).click()
        #投放时段
        if time_period == "不限":
            self.page.locator(CampaignLocators.SCHEDULE_AND_BUDGET).get_by_role("radio",name=time_period).first.click()
        else:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=time_period).click()
        #竞价策略
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=bidding_strategy).click()
        #项目预算
        if budget_type == "不限":
            self.page.locator(CampaignLocators.SCHEDULE_AND_BUDGET).get_by_role("radio",name=budget_type).nth(2).click() #点击不限
        elif budget_type == "日预算":
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=budget_type).click() #点击日预算
            self.fill_input(CampaignLocators.DAILY_BUDGET_INPUT, str(daily_budget)) #输入项目预算
        #付费方式 默认只有一个选项，不需要操作
        self.page.mouse.wheel(0,50)
        #广告预算
        if budget_type is None: #通投-自动，项目日预算
            self.fill_input(CampaignLocators.AD_DAILY_BUDGET_INPUT, str(ad_budget))
        else: #其他场景，广告预算
            self.fill_input(CampaignLocators.AD_BUDGET_INPUT, str(ad_budget))
        #广告出价
        self.fill_input(CampaignLocators.AD_BID_INPUT, str(ad_bid))


    def set_search_express(self, bid_factor, expansion):
        """8.设置搜索快投"""
        self.click_element(CampaignLocators.LIST_SEARCH)
        #TODO 关键词 非必需字段需要吗？怎么选？【搜索关键字 test】【可选可不选】
        # self.click_element(CampaignLocators.KEY_BAG_BUTTON) #点击选择关键词包按钮
        # key_bag_name = "test"
        # self.fill_input(CampaignLocators.KEY_BAG_SEARCH, key_bag_name) #输出关键词包名搜索
        # self.page.get_by_role("row", name=key_bag_name).locator("span").nth(1).click() #勾选
        # self.page.get_by_role("button", name="确认").click()  # 确认按钮
        # self.page.get_by_role("button", name="取消").click()  # 取消按钮
        #出价系数
        self.fill_input(CampaignLocators.BID_FACTOR_INPUT,str(bid_factor))
        #定向拓展
        self.page.locator(CampaignLocators.SEARCH_QUICK_LABEL).filter(has_text=expansion).click()


    def set_generation(self, generation_type, campaign_type, campaign_status, ad_status):
        """9.设置项目生成方式与标签"""
        self.click_element(CampaignLocators.LIST_GENERATION)
        #项目生成方式   直播-直播素材，只能选择“按受众”选项[此时，他们对应的“按受众”是disabled状态]
        if generation_type == "按受众":
            radio = self.page.get_by_role("radio", name=generation_type).first
            if radio and 'is-disabled' not in radio.get_attribute('class'):
                radio.click() #活动状态才点击
            else:
                print("按受众radio为disabled状态，不需要点击，跳过")
        else:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=generation_type).click()
        #投放类型
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=campaign_type).click()

        # 项目标签【非必需字段，可以将其默认设为NONE，在创建广告时中先判断test_data中是否包含该字段，有则进行操作】
        # self.click_element(CampaignLocators.CAMPAIGN_TAG) #点击项目标签＋号
        # self.page.get_by_text("项目生成方式 按受众 按受众、创意 投放类型 拉新 回流 混投 项目标签").click() #点击空白处

        #TODO 目前页面没有这两个字段
        # 项目启停设置
        # self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=campaign_status).click()
        # 广告启停设置
        # self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=ad_status).click()



    def _verify_creation_success(self):
        """点击按钮后直接返回成功（不检查成功消息）"""
        try:
            self.page.get_by_text("另存为新草稿 预览广告").click()
            return True  # 如果没有报错，直接返回成功
        except Exception as e:
            print(f"点击失败: {e}")
            return False


    def is_form_empty(self):
        """验证表单是否为空（所有字段未填写）"""
        # 根据实际表单结构调整验证逻辑
        required_fields = [
            CampaignLocators.AD_BUDGET_INPUT,
            CampaignLocators.AD_BID_INPUT
        ]

        for field in required_fields:
            input_value = self.page.locator(field).input_value()
            if input_value:
                return False
        return True


    def refresh_page(self):
        """刷新页面"""
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        return self
