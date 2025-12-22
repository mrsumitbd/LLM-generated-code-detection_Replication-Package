import anthropic
import json
import re


class DictDataService:
    """
    字典数据管理模块服务层
    """

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.dict_data = {}

    def add_dict_type(self, dict_type: str, description: str = "") -> dict:
        """
        添加字典类型
        
        Args:
            dict_type: 字典类型名称
            description: 字典类型描述
            
        Returns:
            操作结果
        """
        if dict_type in self.dict_data:
            return {"success": False, "message": f"字典类型 {dict_type} 已存在"}
        
        self.dict_data[dict_type] = {
            "description": description,
            "items": {}
        }
        return {"success": True, "message": f"字典类型 {dict_type} 添加成功"}

    def add_dict_item(self, dict_type: str, item_key: str, item_value: str, item_label: str = "") -> dict:
        """
        添加字典项
        
        Args:
            dict_type: 字典类型
            item_key: 项键
            item_value: 项值
            item_label: 项标签
            
        Returns:
            操作结果
        """
        if dict_type not in self.dict_data:
            return {"success": False, "message": f"字典类型 {dict_type} 不存在"}
        
        if item_key in self.dict_data[dict_type]["items"]:
            return {"success": False, "message": f"项 {item_key} 已存在"}
        
        self.dict_data[dict_type]["items"][item_key] = {
            "value": item_value,
            "label": item_label
        }
        return {"success": True, "message": f"项 {item_key} 添加成功"}

    def get_dict_items(self, dict_type: str) -> dict:
        """
        获取字典项列表
        
        Args:
            dict_type: 字典类型
            
        Returns:
            字典项列表
        """
        if dict_type not in self.dict_data:
            return {"success": False, "message": f"字典类型 {dict_type} 不存在", "items": []}
        
        items = []
        for key, value in self.dict_data[dict_type]["items"].items():
            items.append({
                "key": key,
                "value": value["value"],
                "label": value["label"]
            })
        return {"success": True, "items": items}

    def delete_dict_item(self, dict_type: str, item_key: str) -> dict:
        """
        删除字典项
        
        Args:
            dict_type: 字典类型
            item_key: 项键
            
        Returns:
            操作结果
        """
        if dict_type not in self.dict_data:
            return {"success": False, "message": f"字典类型 {dict_type} 不存在"}
        
        if item_key not in self.dict_data[dict_type]["items"]:
            return {"success": False, "message": f"项 {item_key} 不存在"}
        
        del self.dict_data[dict_type]["items"][item_key]
        return {"success": True, "message": f"项 {item_key} 删除成功"}

    def query_with_ai(self, query: str) -> str:
        """
        使用AI查询字典数据
        
        Args:
            query: 查询问题
            
        Returns:
            AI回复
        """
        dict_context = json.dumps(self.dict_data, ensure_ascii=False, indent=2)
        
        prompt = f"""你是一个字典数据管理助手。当前系统中的字典数据如下：

{dict_context}

用户的查询是：{query}

请根据字典数据回答用户的问题。如果用户要求添加、删除或修改字典数据，请告诉用户需要使用相应的API方法。"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text

    def process_command(self, command: str) -> dict:
        """
        处理自然语言命令
        
        Args:
            command: 自然语言命令
            
        Returns:
            处理结果
        """
        prompt = f"""你是一个命令解析助手。用户输入了以下命令：
"{command}"

请分析这个命令，并返回一个JSON格式的结果，包含以下字段：
- action: 操作类型 (add_type, add_item, get_items, delete_item, query)
- dict_type: 字典类型名称
- item_key: 项键（如果适用）
- item_value: 项值（如果适用）
- item_label: 项标签（如果适用）
- description: 字典类型描述（如果适用）
- query: 查询内容（如果是query操作）

只返回JSON，不要有其他文本。"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                parsed_command = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"success": False, "message": "无法解析命令"}
        else:
            return {"success": False, "message": "无法解析命令"}
        
        action = parsed_command.get("action")
        
        if action == "add_type":
            return self.add_dict_type(
                parsed_command.get("dict_type", ""),
                parsed_command.get("description", "")
            )
        elif action == "add_item":
            return self.add_dict_item(
                parsed_command.get("dict_type", ""),
                parsed_command.get("item_key", ""),
                parsed_command.get("item_value", ""),
                parsed_command.get("item_label", "")
            )
        elif action == "get_items":
            return self.get_dict_items(parsed_command.get("dict_type", ""))
        elif action == "delete_item":
            return self.delete_dict_item(
                parsed_command.get("dict_type", ""),
                parsed_command.get("item_key", "")
            )
        elif action == "query":
            result = self.query_with_ai(parsed_command.get("query", ""))
            return {"success": True, "result": result}
        else:
            return {"success": False, "message": f"未知的操作类型: {action}"}


if __name__ == "__main__":
    service = DictDataService()
    
    print("=== 测试字典数据管理服务 ===\n")
    
    print("1. 添加字典类型")
    result = service.add_dict_type("gender", "性别字典")
    print(f"结果: {result}\n")
    
    print("2. 添加字典项")
    result = service.add_dict_item("gender", "1", "male", "男性")
    print(f"结果: {result}")
    result = service.add_dict_item("gender", "2", "female", "女性")
    print(f"结果: {result}\n")
    
    print("3. 获取字典项")
    result = service.get_dict_items("gender")
    print(f"结果: {result}\n")
    
    print("4. 使用AI查询")
    result = service.query_with_ai("性别字典中有哪些项？")
    print(f"AI回复: {result}\n")
    
    print("5. 处理自然语言命令")
    result = service.process_command("添加一个名为status的字典类型，用于表示状态")
    print(f"结果: {result}\n")
    
    print("6. 删除字典项")
    result = service.delete_dict_item("gender", "1")
    print(f"结果: {result}\n")