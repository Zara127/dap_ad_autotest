# 在原有代码基础上添加以下函数
from typing import Dict, Any, Optional

from src.common.utils import generate_test_combinations, load_yaml


def print_test_cases(scenarios: Dict[str, Any], base_data: Dict[str, Any], limit: Optional[int] = None) -> None:
    """
    生成并打印测试用例列表

    Args:
        scenarios: 场景数据（包含多个测试场景）
        base_data: 基础数据配置
        limit: 可选，限制输出的测试用例数量（避免数量过多）
    """
    all_test_cases = []

    # 遍历所有场景生成测试用例
    for scenario in scenarios:
        # 调用生成器获取当前场景的所有测试用例
        scenario_cases = list(generate_test_combinations(scenario, base_data))
        all_test_cases.extend(scenario_cases)
        print(f"场景 [{scenario['name']}] 生成 {len(scenario_cases)} 条测试用例")

    # 输出总览
    print(f"\n===== 测试用例总览 =====")
    print(f"共生成 {len(all_test_cases)} 条测试用例")

    # 打印测试用例（可限制数量）
    print("\n===== 测试用例列表 =====")
    for i, case in enumerate(all_test_cases[:limit], 1):
        print(f"\n测试用例 {i}:")
        # 格式化输出，按字段分类显示
        for key, value in case.items():
            print(f"  {key}: {value}")


# 示例调用（可放在文件末尾）
if __name__ == "__main__":
    # 加载场景数据和基础数据
    base_data = load_yaml("tests/test_data/base_data.yaml")
    scenarios = load_yaml("tests/test_data/scenarios.yaml")
    # 打印测试用例（限制前5条，避免输出过多）
    print_test_cases(scenarios, base_data, limit=5)
