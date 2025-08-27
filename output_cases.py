import allure
from datetime import datetime
from src.common.utils import load_yaml, generate_test_combinations

# 加载数据
base_data = load_yaml("tests/test_data/base_data.yaml")
scenarios = load_yaml("tests/test_data/scenarios.yaml")

def output_test_data():
    """
    加载场景数据，生成测试组合并输出测试数据
    """
    combined_scenarios = scenarios["short_video_scenarios"] + scenarios["live_scenarios"]
    for scenario in combined_scenarios:
        test_data = list(generate_test_combinations(scenario, base_data))
        print(f"场景名称: {scenario['name']}")
        print(f"测试数据组合数量: {len(test_data)}")
        print("测试数据详情:")
        # for index, data in enumerate(test_data, start=1):
        #     print(f"  组合 {index}: {data}")
        # print("-" * 50)

if __name__ == "__main__":
    output_test_data()


