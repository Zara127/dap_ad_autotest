import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
from itertools import product
from typing import Dict, Any, Optional, Iterator, Tuple, List


def load_config(env: str = 'test', config_dir: Optional[Path] = None, env_file: Optional[Path] = None) -> Dict[
    str, Any]:
    """
    加载指定环境的配置，自动替换环境变量

    Args:
        env: 环境名称，对应yaml文件名（如'test'会加载'test.yaml'）
        config_dir: 可选，指定configs目录路径，默认是项目根目录下的configs
        env_file: 可选，指定.env文件路径，默认是项目根目录下的.env

    Returns:
        解析后的配置字典

    Raises:
        FileNotFoundError: 配置文件不存在
        ValueError: 配置格式错误或环境变量未设置
    """
    # 确定文件路径
    base_dir = Path(__file__).parent.parent.parent
    env_file = env_file or base_dir / ".env"
    config_dir = config_dir or base_dir / "configs"
    config_path = config_dir / f"{env}.yaml"
    # 验证文件存在
    if not env_file.exists():
        raise FileNotFoundError(f"未找到.env文件: {env_file}")
    if not config_path.exists():
        raise FileNotFoundError(f"未找到配置文件: {config_path}")
    # 加载环境变量
    load_dotenv(env_file, override=True)
    # 加载并解析YAML
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"配置文件解析失败: {str(e)}")
    # 递归替换环境变量
    def replace_env_vars(data):
        if isinstance(data, dict):
            return {k: replace_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [replace_env_vars(item) for item in data]
        elif isinstance(data, str) and data.startswith('${') and data.endswith('}'):
            var_name = data[2:-1]
            var_value = os.getenv(var_name)
            if var_value is None:
                raise ValueError(f"环境变量未设置: {var_name}")
            return var_value
        return data
    config = replace_env_vars(config)
    # # 验证必要配置项
    # if not config['test'].get('auth', {}).get('token'): #!!!!!注意不要忘记test层级 不是config而是config['test']
    #     raise ValueError("配置中缺少有效的auth.token")
    return config




def load_yaml(file_path: str) -> Dict:
    """
    加载 YAML 文件内容（通用方法，测试/业务代码均可复用）
    :param file_path: YAML 文件路径
    :return: 解析后的 YAML 数据（字典格式）
    :raises FileNotFoundError: 文件不存在时抛出异常
    :raises yaml.YAMLError: YAML 解析失败时抛出异常
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML 文件未找到: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML 解析失败: {str(e)}") from e


def match_resources(base_data: Dict[str, Any], scene: str,
                    purpose: str, app_type: str) -> Tuple[str, str]:
    """
    精确匹配游戏和账户资源，返回单个值
    :return: (game, account)
    :raises ValueError: 如果找不到匹配资源
    """
    matched_games = []
    matched_accounts = []

    for mapping in base_data.get("resource_mapping", []):
        scene_match = mapping["scene"] == scene
        purpose_match = (mapping["purpose"] == "*" or
                         mapping["purpose"] == purpose)
        app_type_match = (mapping["app_type"] == "*" or
                          mapping["app_type"] == app_type)

        if scene_match and purpose_match and app_type_match:
            if mapping["games_key"] in base_data["games"]:
                matched_games.extend(base_data["games"][mapping["games_key"]])
            if mapping["accounts_key"] in base_data["accounts"]:
                matched_accounts.extend(base_data["accounts"][mapping["accounts_key"]])

    if not matched_games or not matched_accounts:
        raise ValueError(f"未找到匹配的资源: scene={scene}, purpose={purpose}, app_type={app_type}")

    # 返回第一个匹配项
    return matched_games[0], matched_accounts[0]


def generate_test_combinations(scenario: Dict[str, Any],
                               base_data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """生成测试数据组合"""
    # 1. 提取场景字段
    scene_fields = {
        "scene": scenario["scene"],
        "ad_type": scenario["ad_type"],
        "delivery_mode": scenario["delivery_mode"]
    }
    if "extra_fields" in scenario:
        scene_fields.update(scenario["extra_fields"])

    # 2. 准备基础字段
    base_fields = {
        "app_type": base_data["contents"]["app_types"],
        "placement": base_data["placements"]["positions"],
        "filter_type": base_data["targetings"]["filter_types"],
        "filter_days": base_data["targetings"]["filter_days"],
        "time": base_data["budget"]["time"],
        "time_period": base_data["budget"]["time_periods"],
        "bidding_strategy": base_data["budget"]["bidding_strategies"],
        "budget_type": base_data["budget"]["budget_types"],
        "daily_budget": base_data["budget"]["daily_budgets"],
        "ad_budget": base_data["budget"]["ad_budgets"],
        "ad_bid": base_data["budget"]["ad_bids"],
        "generation_type": base_data["generation"]["generation_types"],
        "campaign_type": base_data["generation"]["campaign_types"],
        "campaign_status": base_data["generation"]["campaign_status"],
        "ad_status": base_data["generation"]["ad_status"]
    }

    # 3. 处理特殊字段
    if scenario["ad_type"] == "通投广告" and scenario["delivery_mode"] == "手动投放":
        base_fields["bid_factor"] = base_data["search_express"]["bid_factors"]
        base_fields["expansion"] = base_data["search_express"]["expansion_options"]

    if scene_fields["scene"] == "直播" and scene_fields.get("material_type") == "直播素材":
        base_fields["generation_type"] = ["按受众"]

    # 4. 生成组合
    purpose_sub_combos = [
        combo for purpose in base_data["purposes"]
        for combo in purpose["purpose_sub_combos"]
    ]
    other_field_names = list(base_fields.keys())
    other_field_values = list(base_fields.values())

    for other_values, (purpose, sub_purpose) in product(
            product(*other_field_values), purpose_sub_combos):

        test_data = dict(zip(other_field_names, other_values))
        test_data.update({
            "purpose": purpose,
            "sub_purpose": sub_purpose,
            **scene_fields,
            "scenario_name": scenario["name"]
        })

        # 获取单个game和account值
        try:
            game, account = match_resources(
                base_data,
                test_data["scene"],
                purpose,
                test_data.get("app_type")
            )
            test_data["game"] = game
            test_data["account"] = account
            yield test_data
        except ValueError as e:
            print(f"跳过无效组合: {str(e)}")
            continue





# def generate_test_combinations(scenario: Dict[str, Any], base_data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
#     """将场景字段作为整体与基础数据字段进行笛卡尔积组合"""
#     # 1. 提取场景字段
#     scene_fields = {
#         "scene": scenario["scene"],
#         "ad_type": scenario["ad_type"],
#         "delivery_mode": scenario["delivery_mode"]
#     }
#     # # 添加原生广告或素材类型或星广联投任务\指定使用抖音素材
#     # if "native_ad" in scenario:
#     #     scene_fields["native_ad"] = scenario["native_ad"]
#     # if "material_type" in scenario:
#     #     scene_fields["material_type"] = scenario["material_type"]
#     # # 处理新增营销场景十一的星广联投任务字段，它是一个非必须字段，故只给特殊场景进行添加
#     # if "star_task" in scenario:
#     #     scene_fields["star_task"] = scenario["star_task"]
#     # #当某个场景可以选择dap素材+抖音素材时，将该场景数据进行重复设置，用dy_material指定使用抖音素材，未标注的则使用dap素材
#     # if "dy_material" in scenario:
#     #     scene_fields["dy_material"] = scenario["dy_material"]
#
#     # 合并场景数据中的特殊字段（无需if-elif）
#     if "extra_fields" in scenario:
#         scene_fields.update(scenario["extra_fields"])
#     scene_name = scene_fields["scene"]  # 缓存场景名称用于后续判断
#     # 2. 提取基础数据字段（转为列表形式）
#     base_fields = {
#         # 推广目标与子目标的预绑定组合（从基础数据的purpose_sub_combos提取）
#         "purpose_sub": [
#             combo for purpose in base_data["purposes"]
#             for combo in purpose["purpose_sub_combos"]
#         ],
#         # 基础投放字段
#         "app_type": base_data["contents"]["app_types"],
#         "placement": base_data["placements"]["positions"],
#         "filter_type": base_data["targetings"]["filter_types"],
#         "filter_days": base_data["targetings"]["filter_days"],
#         "time": base_data["budget"]["time"],
#         "time_period": base_data["budget"]["time_periods"],
#         "bidding_strategy": base_data["budget"]["bidding_strategies"],
#         "budget_type": base_data["budget"]["budget_types"],
#         "daily_budget": base_data["budget"]["daily_budgets"],
#         "ad_budget": base_data["budget"]["ad_budgets"],
#         "ad_bid": base_data["budget"]["ad_bids"],
#         "generation_type": base_data["generation"]["generation_types"],
#         "campaign_type": base_data["generation"]["campaign_types"],
#         "campaign_status": base_data["generation"]["campaign_status"],
#         "ad_status": base_data["generation"]["ad_status"]
#
#     }
#
#     # # 3. 按场景匹配游戏和账户
#     # if base_data["purposes"]["name"] == "小程序":  # 推广目标为小程序
#     #     base_fields["game"] = base_data["games"]["applet_games"]
#     #     base_fields["account"] = base_data["accounts"]["applet_accounts"]
#     # else: #应用推广
#     #     if scenario["scene"] == "直播":
#     #         base_fields["game"] = base_data["games"]["live_games"]
#     #         base_fields["account"] = base_data["accounts"]["live_accounts"]
#     #     else: #短视频+图文
#     #         if base_data["contents"]["app_types"] == "苹果应用":
#     #             base_fields["game"] = base_data["games"]["sv_games_ios"]
#     #             base_fields["account"] = base_data["accounts"]["sv_accounts_ios"]
#     #         elif base_data["contents"]["app_types"] == "安卓应用":
#     #             base_fields["game"] = base_data["games"]["sv_games_android"]
#     #             base_fields["account"] = base_data["accounts"]["sv_accounts_android"]
#
#     # 3. 按资源映射表匹配游戏和账户
#     matched_games = []
#     matched_accounts = []
#     for mapping in base_data.get("resource_mapping", []):  # 容错：映射表不存在时不报错
#         # 判断映射规则是否匹配当前场景、推广目标范围、应用类型范围
#         scene_match = mapping["scene"] == scene_name
#         # 推广目标匹配：映射表为"*"或包含在基础数据的推广目标中
#         purpose_match = mapping["purpose"] == "*" or any(
#             mapping["purpose"] == p["name"] for p in base_data["purposes"]
#         )
#         # 应用类型匹配：映射表为"*"或包含在基础数据的应用类型中
#         app_type_match = mapping["app_type"] == "*" or mapping["app_type"] in base_data["contents"]["app_types"]
#
#         if scene_match and purpose_match and app_type_match:
#             # 安全获取游戏和账户（避免键不存在报错）
#             if mapping["games_key"] in base_data["games"]:
#                 matched_games.extend(base_data["games"][mapping["games_key"]])
#             if mapping["accounts_key"] in base_data["accounts"]:
#                 matched_accounts.extend(base_data["accounts"][mapping["accounts_key"]])
#
#     # 去重后添加到基础字段（确保游戏和账户不为空）
#     base_fields["game"] = list(set(matched_games)) if matched_games else []
#     base_fields["account"] = list(set(matched_accounts)) if matched_accounts else []
#
#     # 处理通投广告-手动投放特有的字段
#     if scenario["ad_type"] == "通投广告"  and scenario["delivery_mode"] == "手动投放":
#         base_fields["bid_factor"] = base_data["search_express"]["bid_factors"]
#         base_fields["expansion"] = base_data["search_express"]["expansion_options"]
#
#     # 处理通投广告-自动投放特殊的字段【只有它没有项目预算字段的选项】
#     # if scenario["ad_type"] != "通投广告" and scenario["delivery_mode"] != "自动投放":
#     #     base_fields["budget_type"] = base_data["budget"]["budget_types"]
#
#     # # 处理直播-直播素材特殊的字段【项目生成方式，只有“按受众”可以选择】
#     # if scenario["scene"] == "直播" and  scenario["material_type"] == "直播素材":
#     #     base_fields["generation_type"] = ["按受众"]
#
#     # 5. 处理直播-直播素材特有字段（从合并后的scene_fields获取material_type）
#     if scene_name == "直播" and scene_fields.get("material_type") == "直播素材":
#         base_fields["generation_type"] = ["按受众"]  # 强制固定值
#
#
#     # # 4. 处理媒体选项（首选媒体时生成组合）
#     # media_options = []
#     # if base_fields["placement"][0] == "首选媒体":
#     #     from itertools import combinations
#     #     # 生成1到5个媒体的所有组合
#     #     for r in range(1, 6):
#     #         for combo in combinations(base_data["placements"]["media_options"], r):
#     #             media_options.append(list(combo))
#     #     base_fields["media_options"] = media_options
#
# #注：确定不需要设置特殊媒体时，这里可以直接不进行处理，
#     # 4. 处理媒体选项（首选媒体时直接选择全部媒体）
#     # if base_fields["placement"][0] == "首选媒体":
#     #     # 直接选择所有媒体选项，而不是生成组合
#     #     base_fields["media_options"] = base_data["placements"]["media_options"]
#
#     # # 5. 生成基础字段的笛卡尔积
#     # field_names = list(base_fields.keys())
#     # field_values = list(base_fields.values())
#     #
#     # # 6. 将场景字段整体与基础字段组合
#     # for base_values in product(*field_values):
#     #     # 创建基础数据组合
#     #     test_data = dict(zip(field_names, base_values))
#     #     # 合并场景字段（作为整体）
#     #     test_data.update(scene_fields)
#     #     # # 7. 补充推广目标（从基础数据获取） #推广目标不是设置成默认值，而是和其他字段一样，可以通过笛卡尔组合，不同取值构成不同测试用例
#     #     # if "purpose" not in test_data:
#     #     #     default_purpose = base_data["purposes"][0]
#     #     #     test_data["purpose"] = default_purpose["name"]
#     #     #     test_data["sub_purpose"] = default_purpose["sub_types"][0]
#     #
#     #     # 8. 补充场景名称（用于测试用例ID）
#     #     test_data["scenario_name"] = scenario["name"]
#     #     yield test_data
#
#         # 6. 生成最终笛卡尔积组合（拆分purpose_sub确保绑定关系）
#         # 分离purpose_sub字段与其他基础字段
#     purpose_sub_combos = base_fields.pop("purpose_sub")  # 取出预绑定的(目标,子目标)组合
#     other_field_names = list(base_fields.keys())
#     other_field_values = list(base_fields.values())
#
#     # 组合所有维度：其他基础字段 + 绑定的(目标,子目标) + 场景字段
#     for other_values, (purpose, sub_purpose) in product(product(*other_field_values), purpose_sub_combos):
#         # 构建测试用例数据
#         test_data = dict(zip(other_field_names, other_values))
#         test_data.update({
#             "purpose": purpose,  # 推广目标（来自预绑定组合）
#             "sub_purpose": sub_purpose,  # 子目标（来自预绑定组合，确保匹配）
#             **scene_fields,
#             "scenario_name": scenario["name"]
#         })
#
#         yield test_data
