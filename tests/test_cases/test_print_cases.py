import pytest
import allure
from datetime import datetime
from src.common.utils import load_yaml, generate_test_combinations

# 加载数据
base_data = load_yaml("tests/test_data/base_data.yaml")
scenarios = load_yaml("tests/test_data/scenarios.yaml")

class TestCases:

    @allure.story("输出测试用例")
    @pytest.mark.parametrize(
        "scenario",
        scenarios["short_video_scenarios"]+
        scenarios["live_scenarios"],
        ids=[s["name"] for s in
             scenarios["short_video_scenarios"] +
             scenarios["live_scenarios"]]
    )
    def test_cases(self, scenario):
        """创建广告,生成所有组合"""
        test_data = list(generate_test_combinations(scenario, base_data))
        print(test_data.__len__())



