#批量创建页面[新版]
#包含页面具体操作方法、验证元素存在方法、页面加载状态。。。
import re
from itertools import product
from click.decorators import CmdType
# from conftest import campaign_page
from src.core.base_page import BasePage
from src.core.locators import CampaignLocators
from src.pages.old_campaign_page import OldCampaignPage
from src.pages.preview_page import PreviewPage


class CampaignPage(BasePage):
    """新版巨量引擎-批量创建页面操作类"""
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def is_loaded(self):
        """验证页面是否加载完成"""
        # return self.page.is_visible(CampaignLocators.PAGE_TITLE)
        return self.page.is_visible(CampaignLocators.PAGE_TITLE)

    def get_current_page_url(self):
        """获取当前页面 URL，用于判断跳转"""
        return self.page.url

    def create_campaign(self, test_data):
        """根据测试数据创建广告"""

        # #调换1、2两个部分字段的操作顺序，解决切换【推广目的】【营销场景】字段值导致账户清空的问题，避免导致后续数据为空
        # #顺序为：先【关联游戏】、再【营销目标与场景】、最后【投放账户】
        # 1.1关联游戏
        self.set_game(test_data["game"])
        # 1.2 投放账户
        self.set_account(test_data["account"])

        # 2. 营销目标与场景【推广目标、投放类型、营销场景、广告类型、投放模式、】
        self.set_purpose_and_scene(
            test_data["purpose"],
            test_data.get("sub_purpose"),
            test_data["scene"],
            test_data["ad_type"],
            test_data["delivery_mode"],
            test_data["game"]
        )

        # 3. 投放内容与目标【星广联投任务、应用类型、推广应用、转化目标】
        if "star_task" in test_data:
            star_task = test_data["star_task"]
        else:
            star_task = None
        self.set_content_and_target(test_data["app_type"],test_data["ad_type"],test_data["delivery_mode"],star_task)

        # 4. 投放版位【投放位置、媒体选择】
        # 只有通投-手动时，需要手动选择投放版位，其他情景下只有一个选项，默认选择。
        if test_data["ad_type"] == "通投广告"  and test_data["delivery_mode"] == "手动投放":
            self.set_placement(
                test_data["placement"],
                test_data.get("media_options")
            )

        # 5.用户定向【定向盒子、过滤已转化、过滤时间、】
        #todo 若固定过滤转化和过滤时间的话，这里可以直接不进行区分
        if test_data["filter_type"] == "公司账户" or test_data["filter_type"] == "APP":
            self.set_targeting(
                filter_type=test_data["filter_type"],
                filter_days=test_data["filter_days"]
            )
        else:
            self.set_targeting(
                filter_type=test_data["filter_type"],
            )

        # 6. 广告设置【原生广告投放、创意盒子/素材组、产品名称、产品主图、产品卖点、行动号召】
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
        if "star_task" in test_data:
            star_task = test_data["star_task"]
        else:
            star_task = None
        if "dy_material" in test_data:
            dy_material = test_data["dy_material"]
        else:
            dy_material = None

        #搜索-极速智投、搜索-常规投放，需要文本摘要
        if test_data["ad_type"]== "搜索广告":
            text_summary = "文本摘要"
        else:
            text_summary = None
        self.set_creative(native_ad=native_ad, game=test_data['game'], land_page = land_page, material_type=material_type,text_summary=text_summary,star_task=star_task,dy_material=dy_material)


        # 7. 排期与预算【投放时间、投放时段、竞价策略、项目预算、付费方式 / 竞价策略、广告预算、广告出价】
        if test_data["ad_type"] == "通投广告" and test_data["delivery_mode"] == "自动投放":  #没有项目预算选项、竞价策略新增最大转化
            #竞价策略【选择原则：通投-自动，传入“最大转化”值进行选择；其他默认不操作】
            budget_type = None
            daily_budget = None
            bidding_strategy = test_data["bidding_strategy"]
        else:
            bidding_strategy = None
            budget_type = test_data["budget_type"]
            if test_data["budget_type"] == "不限":  # 没有日预算
                daily_budget = None
            else:
                daily_budget = test_data["daily_budget"]
        self.set_budget(
            time=test_data["time"],
            time_period=test_data["time_period"],
            bidding_strategy=bidding_strategy, #竞价策略【选择原则：通投-自动，传入“最大转化”值进行选择；其他默认不操作】
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

    # 跳转页面-返回旧版
    def click_return_old_version(self):
        """点击「返回旧版」按钮"""
        with self.page.expect_popup() as page2_info:
            self.click_element(CampaignLocators.RETURN_OLD_VERSION_BUTTON)
            self.page.wait_for_load_state("networkidle")  # 等待页面加载
        page2 = page2_info.value
        page2.wait_for_load_state("networkidle")
        # 返回广告创建页面实例
        return OldCampaignPage(page2)

    def is_old_version_loaded(self):
        """验证是否跳转到旧版页面"""
        # 根据旧版页面特征元素判断（如旧版页面标题、特有元素等）
        return self.page.is_visible(CampaignLocators.OLD_VERSION_PAGE_TITLE)



    def set_game(self, game):
        """1.1选择关联游戏"""
        self.page.locator(CampaignLocators.GAME_SELECTOR_NEW).click()# #新版
        self.page.get_by_role("option", name=game).locator("div").first.click()#下拉列表选择

    def set_account(self, account):
        """1.2 选择投放账户"""
        # 投放账户
        self.click_element(CampaignLocators.ACCOUNT_ADD) #点击按钮
        self.fill_input(CampaignLocators.ACCOUNT_FILL_NEW, account) #输入账户
        self.page.get_by_role("textbox", name="请输入", exact=True).press("Enter")
        self.page.wait_for_load_state("networkidle") # 等待页面加载完成
        self.page.get_by_role("row", name=account).locator("use").first.click() #勾选搜索后出现的第一个
        self.page.get_by_role("button", name="确定").click() # 点击确认->确定

    def set_purpose_and_scene(self, purpose, sub_purpose, scene, ad_type, delivery_mode,game):
        """2.选择营销目标与场景【(推广目标、投放类型/投放内容)、营销场景、广告类型、投放模式】"""
        self.click_element(CampaignLocators.LIST_PURPOSE_SCENE)
        # 推广目标：应用推广/小程序
        self.page.locator(CampaignLocators.PURPOSE_SCENE_SELECTOR_NEW).filter(has_text=purpose).click() #新版
        # 子目标：投放类型/投放内容
        if sub_purpose:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=sub_purpose).click()
        #营销场景
        if scene == "直播":  #否则会匹配到两个元素
            self.page.locator(CampaignLocators.PURPOSE_SCENE_LABEL_NEW).filter(has_text=scene).click() #新版
        else:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=scene).click()
        #广告类型
        self.page.locator(CampaignLocators.PURPOSE_SCENE_LABEL_NEW).filter(has_text=ad_type).click()  # 新版
        #投放模式
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=delivery_mode).click()

        # 搜索广告-极速智投，新增蓝海关键词选项、自定义关键词（非必选）
        #选择蓝海关键词 【选择原则：根据关联游戏名称选择对应分组下的第一个关键词】
        lanhai_key = self.page.locator(CampaignLocators.LANHAI_KEY)
        if lanhai_key.is_visible():
            lanhai_key.click() #点击 添加蓝海关键词 按钮
            # 定位游戏分组（通过 <h3 class="group-title"> 匹配游戏名称）
            game_group_selector = f"h3.group-title:has-text('{game}')"
            game_group = self.page.locator(game_group_selector).locator("..") #父级div
            if not game_group or not game_group.is_visible():
                raise ValueError(f"未找到游戏分组: {game}，请检查游戏名称或页面加载！")
            # 定位分组内的第一个关键词选项: 游戏分组内的第一个 .keyword-option 下的复选框
            first_keyword_checkbox = game_group.locator(".keyword-option:nth-child(1) label.ep-checkbox").first
            if first_keyword_checkbox.count() == 0:
                raise ValueError(f"游戏 {game} 分组内未找到关键词复选框！")
            first_keyword_checkbox.check()  #勾选复选框
            self.page.get_by_role("button", name="确定").click() #点击确定按钮，关闭抽屉
        #选择自定义关键词
        # auto_key = self.page.locator(CampaignLocators.AUTO_KEY).locator("div").filter(has_text="自定义关键词")
        auto_key = self.page.get_by_role("group",name="自定义关键词")
        if auto_key.is_visible():
            auto_key.get_by_role("button",name="选择").click()
            self.fill_input(CampaignLocators.AUTO_KEY_INPUT,"测试")  #随便输入..
            self.page.get_by_role("button", name="查询").click()
            self.page.locator(".item-action:has-text('添加')").first.click()
            self.page.get_by_role("button",name="确定").click()

        #如果是搜索广告-常规投放，需要选择蓝海流量包(必选)
        #选择蓝海流量包【选择原则：根据游戏名称选择】
        lanhai_bag_button = self.page. get_by_label("蓝海流量包").locator("div").filter(has_text="未选择蓝海流量包 选择").first #新版选择按钮
        if lanhai_bag_button.is_visible():
            self.page.locator(CampaignLocators.LANHAI_BAG).get_by_label("蓝海流量包").get_by_text("选择", exact=True).click()
            self.page.get_by_role("row",name=f"{game}").locator("span").nth(1).click()
            self.page.get_by_role("button", name="确定").click() #确认->确定
        # else:
        #     print("蓝海流量包选择不可见")


    def set_content_and_target(self, app_type,ad_type,delivery_mode,star_task=None):
        """3.投放内容与目标【应用类型、推广应用、转化目标】"""
        self.click_element(CampaignLocators.LIST_CONTENT_TARGET)
        #选择关联星广联投任务 【选择原则：固定选择一个任务】
        # [营销场景十一 选择该字段，会影响后续广告/创意设置]
        if star_task:
            star_task_select_button = self.page.locator(CampaignLocators.STAR_TASK).locator("../..").locator(CampaignLocators.STAR_TASK_SELECTOR)
            star_task_select_button.click() # 点击 关联星广联投任务 选择按钮
            (self.page.get_by_text("战火勋章25年6月星广联投素材-常规发布赛道-芦鸣", exact=True).locator("../../..")
             .locator("td:first-child .ep-radio__inner").click())  # 设置固定选一个任务
            self.page.get_by_role("button", name="确定").click()  # 确认->确定

        #选择应用类型
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=app_type).click()
        #选择推广应用【todo优化：这里会有默认值，也可以不进行操作】
        self.page.locator(CampaignLocators.APP_SELECTOR_BOX_NEW).click() #新版
        if app_type == "安卓应用": #【选择原则：优先选择中国-安卓（不含同名包）的第一个；若无，则选择带有“中国-安卓”的第一个】
            # 先定位所有包含 "中国-安卓" 文本的元素，然后过滤掉包含 "同名包" 文本的元素，取第一个进行点击
            target_elements = self.page.get_by_text("中国-安卓", exact=False).filter(has_not_text="同名包")
            if target_elements.count() > 0:
                target_elements.first.click()
            else:
                # 如果过滤后没有符合条件的元素，就选第一个包含 "中国-安卓" 文本的元素（即便包含同名包，保证有选项可点）
                self.page.get_by_text("中国-安卓", exact=False).first.click()
        elif app_type == "苹果应用":
            # self.page.locator("text=/.*中国-(ios|苹果|iOS|IOS).*/i").click()
            self.page.get_by_role("option",name=re.compile(r".*中国-(ios|苹果|iOS|IOS).*")).first.click()

        #选择转化目标 【选择原则：在创建广告的几个账号的不同场景下都新建test转化目标，激活：test_zst(sdk)/test_i(api)；付费-7日roi：test_zst_roi】
        conversion_aim =  self.page.get_by_label("转化目标").locator("div").filter(has_text="未选择转化目标 选择").nth(1)
        if conversion_aim.is_visible(): #转化目标区域
            conversion_aim_selector = self.page.get_by_label("转化目标").get_by_text("选择", exact=True)
            conversion_aim_selector.click() #点击 选择 按钮
            if ad_type == "通投广告" and delivery_mode == "自动投放": #特定营销场景，需要先更改选择弹窗中的筛选器再选择转化目标
                #更改筛选器内容为：转化目标：付费、深度转化目标：付费ROI-7日
                self.page.get_by_text("转化目标:", exact=True).click()
                self.page.get_by_role("option", name="付费").click()
                self.page.get_by_text("深度转化目标:").click()
                self.page.get_by_role("option", name="付费ROI-7日").click()
                #选择转化目标：包含test_zst_roi
                self.page.get_by_role("row", name=re.compile(r".*test_zst_roi.*", re.IGNORECASE)).locator("label").click()
                self.page.get_by_role("button", name="确定").click()  # 确认->确定
                #选择新出现的字段：深度转化方式：每次付费+7日roi【选择该值，后续竞价策略选择新增值：最大转化】
                #判断深度转化方式字段是否存在
                if self.page.locator(CampaignLocators.DEEP_CONVERSION_LABEL).is_visible():
                    self.page.locator(CampaignLocators.DEEP_CONVERSION_WAY).click() #选择深度转化方式：每次付费+7日roi
            else:
                #如果在搜索前可见“test_zst”，则直接点击；否则再进行搜索选择
                if self.page.get_by_text("test_zst").is_visible():
                    self.page.get_by_text("test_zst").click()
                    self.page.get_by_role("row", name=re.compile(r"^test_zst.*")).locator("label").click()
                else:
                    self.fill_input(CampaignLocators.CONVERSION_SEARCH_INPUT_NEW,"test_zst")
                    self.page.locator(
                        ".search-wrap > .el-input > .el-input__suffix > .el-input__suffix-inner > .el-input__icon").click()
                    self.page.get_by_role("dialog").locator("tbody").get_by_role("cell").filter(has_text=re.compile(r"^$")).locator(
                        "span").click()
                self.page.get_by_role("button", name="确定").click()  # 确认->确定


    def set_placement(self, position, media_options):
        """4. 投放版位【投放位置、媒体选择】"""
        self.click_element(CampaignLocators.LIST_PLACEMENT)
        self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=position).click()# 选择投放位置
        #【注】首选媒体，默认全选，不需要操作；若需要指定版位，在操作时需要先去掉默认勾选，再勾选指定版位

    def set_targeting(self, filter_type, filter_days=None):  #targeting_num参数
        """5.用户定向【定向盒子、过滤已转化、过滤时间】"""
        self.click_element(CampaignLocators.LIST_USER_TARGETING)
        self.click_element(CampaignLocators.TARGETING_PACK_BUTTON)  # 点击添加定向包【新版】
        #选择用户定向包【选择原则：在关联游戏下创建定向包，命名为test_zst】
        # 如果在搜索前可见“test_zst”，则直接选择；否则再进行搜索选择
        user_target_selector = self.page.get_by_role("cell", name=re.compile(r".*test_zst.*", re.IGNORECASE))
        if user_target_selector.is_visible():
            user_target_selector.first.click()
        else:
            # self.fill_input(CampaignLocators.TARGETING_SEARCH_INPUT,"test_zst") #输入“test_zst”
            self.page.get_by_role("textbox", name="请输入", exact=True).click()
            self.page.get_by_role("textbox", name="请输入", exact=True).fill("test_zst")
            self.page.get_by_role("textbox", name="请输入", exact=True).press("Enter")
            self.page.get_by_role("row", name=re.compile("test")).locator("div").first.click()  # 选择匹配到的第一个
        self.page.get_by_role("button", name="确定").click() #确认->确定

        self.page.mouse.wheel(0,200)

        #【注】过滤已转化、过滤时间可以设置为默认值、固定、不进行操作【不影响主流程】
        self.page.get_by_label("过滤已转化").get_by_text("不限").click() #固定选择过滤已转化：不限
        # # 过滤已转化
        # if filter_type == "不限" or filter_days == "广告": #[ui定位器有点区别]
        #     self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=re.compile(rf"^{filter_type}$")).click()
        # else:
        #     self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=filter_type).click()
        # # 过滤时间[与过滤已转化的取值有关]
        # if filter_days:
        #     self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=filter_days).click()


    def select_douyin_account(self, game,material_type=None):
        # 选择抖音号
        # douyin_selector = self.page.locator(CampaignLocators.DOUYIN_SELECTOR_NEW)
        # douyin_selector_button = douyin_selector.locator(CampaignLocators.DOUYIN_SELECTOR_BUTTON_NEW)
        #先找到投放抖音号父级
        douyin_placeholder = self.page.get_by_text("未选择抖音号", exact=True)
        douyin_parent_module =  douyin_placeholder.locator("../../..")  # 向上找 3 层父级
        #再根据父级定位选择按钮，避免定位到同一页面的多个元素
        douyin_selector_button = douyin_parent_module.get_by_role("button", name="选择", exact=True)
        if douyin_selector_button.is_visible():
            douyin_selector_button.click()  # 点击抖音号 选择按钮
            self.page.wait_for_load_state("networkidle")
            # 如果当前页面包含game名称的抖音号是可见的,则直接选择；否则再通过搜索选择
            if game=="剑与远征：启程":
                name = "剑与远征"
            else:
                name = game
            game_douyin_account = self.page.get_by_role("cell",name=name).first
            if game_douyin_account.is_visible():
                game_douyin_account.click()  # 选择匹配到的第一个
                if material_type == "直播素材":
                    print("直播素材")
                    self.page.get_by_role("button",name="确定").click()
                else:
                    self.page.get_by_role("button", name="确定").nth(1).click()
                    # self.page.locator("button[aria-disabled='false']:has-text('确定')").click()  # 确认按钮--->确定
            else:
                self.fill_input(CampaignLocators.DOUYIN_SEARCH_INPUT_NEW, name)  # 在搜索框输入游戏名 #指定name
                self.page.locator(CampaignLocators.DOUYIN_SEARCH_INPUT_NEW).press("Enter")  # 回车搜索
                self.page.get_by_role("cell",name=re.compile(r".*"+name+".*")).first.click()  # 选择匹配到的第一个(包含)
                if material_type == "直播素材":
                    print("直播素材")
                    self.page.get_by_role("button", name="确定").click()  #todo
                else:
                    self.page.get_by_role("button", name="确定").nth(1).click()  # 确认按钮--->确定
        else:
            print("未找到抖音号选择按钮")



    def fill_search(self,text: str):
        if text != "":
            search_box = self.page.get_by_role("textbox", name=re.compile(r"请输入搜索内容|请输入音乐名称进行搜索|请输入文案进行搜索|请输入标题关键词搜索"))  # 获取搜索框
            search_box.click()  # 点击搜索框
            search_box.fill(text)  # 填写搜索内容
            search_box.press("Enter")  # 按下 Enter 键

    def select_material(self,count: int):
        # 定位所有包含素材复选框的容器/视觉元素
        if self.page.locator("div.grid > div.cursor-pointer:has(label.ep-checkbox)").first.is_visible():
            checkboxes = self.page.locator("div.grid > div.cursor-pointer:has(label.ep-checkbox)")
        else:
            checkboxes = self.page.locator("table.ep-table__body > tbody > tr.ep-table__row:has(label.ep-checkbox)")
        # 验证数量并选择
        print(checkboxes.count())
        if checkboxes.count() < count:
            print(f"素材不足，需{count}个，实际{checkboxes.count()}个")
            count = checkboxes.count()
            print(f"实际选择{count}个素材")
        if checkboxes.count() > 1: #页面有一个选择全部的固定checkbox
            for i in range(count):
                # 定位第i个复选框的label/span,触发勾选
                checkbox_label = checkboxes.nth(i + 1).locator("span.ep-checkbox__input")
                checkbox_label.click()
                print(f"已选择第{i + 1}个素材")
        else:
            pass #直接跳过

    def set_material_count(self,materials):
        for material in materials:
            locator, count = material
            span_locator = self.page.locator(locator).nth(1)
            span_locator.click()  # 点击素材类型按钮
            input_locator = span_locator.locator("../following-sibling::input")
            input_locator.fill(str(count))  # 填写数量

    def select_materials(self,materials):
        for material in materials:
            button, search_keyword, count = material
            self.page.locator(button).nth(0).click()  # 点击素材类型按钮
            self.fill_search(search_keyword)
            self.select_material(count)


    def set_creative(self, native_ad=None,game=None, material_type=None,land_page=None,text_summary=None,star_task=None,dy_material=None):
        """6.广告创意/广告设置（根据场景选择原生广告或素材类型）【原生广告投放、创意盒子/素材组、产品名称、产品主图、产品卖点、行动号召】"""
        self.click_element(CampaignLocators.LIST_AD_SET_NEW)
        # 【注】：短视频+图文场景有原生广告开关；直播场景有素材类型选择
        # 直播-直播素材：在外面选择抖音号；直播-广告素材/其他：在素材组中选择抖音号

        # 选择原生广告投放
        if native_ad:
            self.page.locator(CampaignLocators.ADMATERIAL_LABEL_SELECTOR_NEW).filter(has_text=native_ad).click()
        #选择素材类型
        if material_type:
            self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=material_type).click()
            if material_type == "直播素材": #场景七&九：直播-直播素材  不需要选择素材组,在外部选择抖音号
                self.select_douyin_account(game,material_type)

            #素材组外选择蓝海关键词【直播-搜索-常规 可见】
            # 【注】如果是搜索广告-常规投放，则需要选择蓝海关键词【直播的蓝海关键词在外面,短视频+图文的在素材组内】
            lanhai_key_selector_set = self.page.locator(CampaignLocators.LANHAI_KEY_SELECTOR_SET)
            if lanhai_key_selector_set.is_visible():
                lanhai_key_selector_set.click()
                #选择原则：选择第一个
                self.page.get_by_text("预估消耗（元）").nth(0).click()


        material_button = self.page.locator(CampaignLocators.MATERIAL_SELECT_BUTTON)
        if material_button.is_visible(): #场景七&九：直播-直播素材时，该按钮不可见，不需要选择素材组
            material_button.click()  #点击 批量选择素材 按钮
            # 1.如果开启原生广告或选择广告素材，则可以选dap+抖音素材（copy场景数据，如果设置了ad_material的值就选择抖音素材，未设置则选择dap素材）；
            # 2.如果选择了星广联投，则只能选择抖音素材（抖音视频）；
            # 3.否则，只能选择dap素材
            if star_task: # 只可选择抖音素材(抖音视频)
                #1.素材组设置
                materials_to_set = [
                    (CampaignLocators.DOUYIN_VIDEO, 5),  # 抖音视频
                ]
                self.set_material_count(materials_to_set)
                #2.选择投放抖音号[可以不选择指定抖音号，默认选择全部抖音号]
                # self.select_douyin_account(game,material_type)
                #3.选择素材
                materials_to_select = [
                    (CampaignLocators.DOUYIN_VIDEO_BUTTON, "", 1),  # 抖音视频
                ]
                self.select_materials(materials_to_select)
                self.page.get_by_role("button", name="确定").click()  # 点击 确定 按钮
                #注：星广联投：先选择素材、再选择文案
                # 4.选择文案
                self.page.locator("button:has-text('文案库')").click()  #点击文案库 按钮
                self.page.get_by_role("row", name=re.compile("^测试")).first.locator("span").nth(1).click()
                # self.page.locator("table.ep-table__body tbody tr.ep-table__row:has-text('测试数据勿用821')")  #固定选择一条文案内容
                self.page.get_by_role("button", name="确定").click()


            # if native_ad=="开启" or material_type=="广告素材": # 可以选择dap/抖音素材
            elif dy_material: # 选择抖音素材（抖音视频+抖音图文）
                #1.素材组设置
                materials_to_set = [
                    (CampaignLocators.TEXT, 2),  # 文案
                    (CampaignLocators.DOUYIN_VIDEO, 5),  # 抖音视频
                    (CampaignLocators.DOUYIN_IMG, 5),    #抖音图文
                ]
                self.set_material_count(materials_to_set)
                #2.选择投放抖音号
                self.select_douyin_account(game,material_type)
                #3.选择素材
                materials_to_select = [
                    (CampaignLocators.TEXTBUTTON, "", 2),  # 文案库
                    (CampaignLocators.DOUYIN_VIDEO_BUTTON, "", 1),  # 抖音视频
                    (CampaignLocators.DOUYIN_IMG_BUTTON, "", 1),  # 抖音图文[提供账号下没有抖音图文的素材]

                ]
                self.select_materials(materials_to_select)
                self.page.get_by_role("button", name="确定").click()  # 点击 确定 按钮

            else: #选择dap素材/只可选择dap素材
                #1.素材组设置【视频：5，图片：5，图文：2，文案：2】
                materials_to_set = [
                    (CampaignLocators.VIDEO, 5),  # 视频
                    (CampaignLocators.IMG, 5),  # 图片
                    (CampaignLocators.GROUPIMG, 2),  # 图文
                    (CampaignLocators.TEXT, 2)  # 文案
                ]
                self.set_material_count(materials_to_set)

                #补充：如果选择投放抖音号可见，则选择抖音号
                self.select_douyin_account(game, material_type)

                #2.选择素材【视频：1，图片：3，组图：4，音乐库：2，文案库：2】
                materials_to_select = [
                    (CampaignLocators.VIDEOBUTTON, "测试", 2),  # 视频
                    (CampaignLocators.IMGBUTTON, "测试", 2),  # 图片
                    (CampaignLocators.GROUPIMGBUTTON, "测试", 2),  # 组图
                    (CampaignLocators.MUSICBUTTON, "", 1),  # 音乐库
                    (CampaignLocators.TEXTBUTTON, "", 1)  # 文案库
                ]
                self.select_materials(materials_to_select)
                self.page.get_by_role("button", name="确定").click() # 点击 确定 按钮

            # 素材组内选择蓝海关键词【任意选择一个】
            if self.page.locator(CampaignLocators.LANHAI_KEY_SELECTOR_SET).is_visible():
                self.click_element(CampaignLocators.LANHAI_KEY_SELECTOR_SET)
                self.page.get_by_text("预估消耗（元）").nth(0).click()

        # 营销场景：搜索-极速智投、搜索-常规投放 需要填写文本摘要【选择原则：在摘要库中选择第一条】
        if text_summary:
            self.click_element(CampaignLocators.TEXT_SUMMARY)  # 点击摘要库
            self.page.get_by_role("row").nth(1).locator("span").nth(1).click() #勾选第一行
            self.page.get_by_role("button", name="确定").click()
            self.page.get_by_role("group", name="文本摘要*").get_by_role("img").nth(1).click() #[注：点击摘要库添加会自动新增一个框，点击删除按钮]


        # 应用类型：安卓应用，选择落地页【选择原则：根据游戏名称game固定选择落地页】
        # 例如：
        # 战火勋章，选择：官包-Wgame-真实战场灰-长版 ；
        # 万龙觉醒，选择：万龙觉醒，国风新版本！
        if land_page:
            land_name = ""
            if game == "战火勋章":
                land_name = "官包-Wgame-真实战场灰-长版"
            elif game =="万龙觉醒":
                land_name = "万龙觉醒，国风新版本！"
            self.click_element(CampaignLocators.LAND_PAGE_SELECT_BUTTON_NEW) #点击 添加落地页 按钮【新版】
            # 先找包含目标文本的单元格，再定位该行的复选框
            checkbox_locator = ((self.page.get_by_text(land_name)
                        .locator('..')
                       .locator('preceding-sibling::td'))
                       .locator('input.ep-checkbox__original')) #定位到指定落地页名称所在行的复选框
            checkbox_locator.click() #勾选复选框
            self.page.get_by_role("button", name="确定").click()


        # 添加鼠标滚动
        self.page.mouse.wheel(0, 100)

    def set_budget(self, time, time_period, ad_budget, ad_bid,bidding_strategy=None, daily_budget=None, budget_type=None):
        """7.设置排期与预算"""
        self.click_element(CampaignLocators.LIST_SCHEDULE_BUDGET)
        #【注】投放时间、投放时段可以默认值，不进行操作
        # #投放时间
        # self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=time).click()
        # #投放时段
        # if time_period == "不限":
        #     self.page.locator(CampaignLocators.SCHEDULE_AND_BUDGET).get_by_role("radio",name=time_period).first.click()
        # else:
        #     self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=time_period).click()

        #竞价策略【选择原则：通投-自动--选择“最大转化”；其他选择默认值，即不操作】
        # 在base_data中设置，bidding_strategy只有“最大转化”，其他场景不操作
        if bidding_strategy:
            self.page.locator(CampaignLocators.SCHEDULE_AND_BUDGET_NEW).get_by_text(f"{bidding_strategy}").click()
        #项目预算
        if budget_type == "不限":
            self.page.get_by_label("项目预算").get_by_text(f"{budget_type}").click() #点击不限
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
        #广告/项目出价【竞价策略选择最大转化时，不展示出价】
        ad_bid_selector = self.page.locator(CampaignLocators.AD_BID_INPUT)
        if ad_bid_selector.is_visible():
            self.fill_input(CampaignLocators.AD_BID_INPUT, str(ad_bid))


    def set_search_express(self, bid_factor, expansion):
        """8.设置搜索快投"""
        self.click_element(CampaignLocators.LIST_SEARCH)
        #关键词 非必需字段【搜索关键字 test】【可选可不选】
        # self.click_element(CampaignLocators.KEY_BAG_BUTTON) #点击选择关键词包按钮
        # key_bag_name = "test"
        # self.fill_input(CampaignLocators.KEY_BAG_SEARCH, key_bag_name) #输出关键词包名搜索
        # self.page.get_by_role("row", name=key_bag_name).locator("span").nth(1).click() #勾选
        # self.page.get_by_role("button", name="确认").click()  # 确认按钮
        # self.page.get_by_role("button", name="取消").click()  # 取消按钮
        #出价系数
        self.fill_input(CampaignLocators.BID_FACTOR_INPUT,str(bid_factor))
        #定向拓展【默认值，可不操作】
        # self.page.locator(CampaignLocators.SEARCH_QUICK_LABEL).filter(has_text=expansion).click()


    def set_generation(self, generation_type, campaign_type, campaign_status, ad_status):
        """9.设置项目生成方式与标签"""
        #可以取默认值，不操作
        self.click_element(CampaignLocators.LIST_GENERATION)
        #项目生成方式   直播-直播素材，只能选择“按受众”选项[此时，他们对应的“按受众”是disabled状态]
        # if generation_type == "按受众":
        #     radio = self.page.get_by_role("radio", name=generation_type).first
        #     if radio and 'is-disabled' not in radio.get_attribute('class'):
        #         radio.click() #活动状态才点击
        #     else:
        #         print("按受众radio为disabled状态，不需要点击，跳过")
        # else:
        #     self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=generation_type).click()
        # #投放类型
        # self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=campaign_type).click()

        # 项目标签【非必需字段，可以将其默认设为NONE，在创建广告时中先判断test_data中是否包含该字段，有则进行操作】
        # self.click_element(CampaignLocators.CAMPAIGN_TAG) #点击项目标签＋号
        # self.page.get_by_text("项目生成方式 按受众 按受众、创意 投放类型 拉新 回流 混投 项目标签").click() #点击空白处

        #项目启停、广告启停【默认值即可，不需要操作】
        # 项目启停设置
        # self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=campaign_status).click()
        # 广告启停设置
        # self.page.locator(CampaignLocators.LABEL_LOCATOR).filter(has_text=ad_status).click()



    def _verify_creation_success(self):
        """点击按钮后直接返回成功（不检查成功消息）"""
        try:
            self.page.get_by_text("预览广告").click()
            #todo 暂时添加一个 点击浏览器返回按钮，方便检查【后面再去掉】
            self.page.wait_for_load_state("networkidle")
            self.page.go_back()
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
        return self.page
