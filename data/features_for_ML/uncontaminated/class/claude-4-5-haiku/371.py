import anthropic
import json
import re


class SeedEXState:
    """席德强化E释放的**当前**状态"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.state_data = {}

    def get_state(self) -> dict:
        """获取当前状态"""
        return self.state_data

    def set_state(self, state: dict) -> None:
        """设置状态"""
        self.state_data = state

    def update_state(self, key: str, value) -> None:
        """更新状态中的特定键"""
        self.state_data[key] = value

    def analyze_with_claude(self, prompt: str) -> str:
        """使用Claude分析状态"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def get_state_description(self) -> str:
        """获取状态的文字描述"""
        if not self.state_data:
            return "状态未初始化"

        state_str = json.dumps(self.state_data, ensure_ascii=False, indent=2)
        prompt = f"请用简洁的中文描述以下游戏状态：\n{state_str}"

        return self.analyze_with_claude(prompt)

    def validate_state(self) -> bool:
        """验证状态是否有效"""
        if not self.state_data:
            return False

        required_keys = ["energy", "cooldown", "active"]
        return all(key in self.state_data for key in required_keys)

    def reset_state(self) -> None:
        """重置状态"""
        self.state_data = {"energy": 0, "cooldown": 0, "active": False}

    def get_recommendation(self) -> str:
        """获取Claude的建议"""
        if not self.state_data:
            return "请先初始化状态"

        state_str = json.dumps(self.state_data, ensure_ascii=False, indent=2)
        prompt = f"基于以下席德强化E释放状态，请给出优化建议：\n{state_str}"

        return self.analyze_with_claude(prompt)

    def parse_state_from_text(self, text: str) -> dict:
        """从文本中解析状态信息"""
        prompt = f"""请从以下文本中提取游戏状态信息，并返回JSON格式：
文本内容：{text}

请返回包含以下字段的JSON（如果文本中没有相关信息，使用null）：
- energy: 能量值（数字）
- cooldown: 冷却时间（数字）
- active: 是否激活（布尔值）
- level: 技能等级（数字）
- description: 状态描述（字符串）

只返回JSON，不要其他内容。"""

        response = self.analyze_with_claude(prompt)

        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                self.state_data.update(parsed)
                return parsed
        except (json.JSONDecodeError, AttributeError):
            pass

        return {}

    def compare_states(self, other_state: dict) -> str:
        """比较两个状态"""
        current_str = json.dumps(self.state_data, ensure_ascii=False, indent=2)
        other_str = json.dumps(other_state, ensure_ascii=False, indent=2)

        prompt = f"""请比较以下两个席德强化E释放状态，并说明差异：
当前状态：
{current_str}

对比状态：
{other_str}"""

        return self.analyze_with_claude(prompt)


if __name__ == "__main__":
    state = SeedEXState()

    state.reset_state()
    print("初始状态:", state.get_state())

    state.update_state("energy", 100)
    state.update_state("cooldown", 5)
    state.update_state("active", True)
    state.update_state("level", 3)

    print("\n更新后的状态:", state.get_state())
    print("状态有效性:", state.validate_state())

    print("\n状态描述:")
    print(state.get_state_description())

    print("\n优化建议:")
    print(state.get_recommendation())

    text = "席德的E技能已激活，当前能量为85，冷却时间还剩3秒，技能等级为2级"
    print("\n从文本解析状态:")
    parsed = state.parse_state_from_text(text)
    print("解析结果:", parsed)

    other_state = {"energy": 50, "cooldown": 10, "active": False, "level": 1}
    print("\n状态对比:")
    print(state.compare_states(other_state))