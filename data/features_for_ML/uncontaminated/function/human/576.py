from src.chat.utils.prompt_builder import Prompt, global_prompt_manager

def init_prompt():
    Prompt(
        """
{time_block}
{name_block}
你的兴趣是：{interest}
{chat_context_description}，以下是具体的聊天内容
**聊天内容**
{chat_content_block}

**动作记录**
{actions_before_now_block}

**可用的action**
reply
动作描述：
进行回复，你可以自然的顺着正在进行的聊天内容进行回复或自然的提出一个问题
{{
    "action": "reply",
    "target_message_id":"想要回复的消息id",
    "reason":"回复的原因"
}}

no_reply
动作描述：
等待，保持沉默，等待对方发言
{{
    "action": "no_reply",
}}

{action_options_text}

请选择合适的action，并说明触发action的消息id和选择该action的原因。消息id格式:m+数字
先输出你的选择思考理由，再输出你选择的action，理由是一段平文本，不要分点，精简。
**动作选择要求**
请你根据聊天内容,用户的最新消息和以下标准选择合适的动作:
{plan_style}
{moderation_prompt}

请选择所有符合使用要求的action，动作用json格式输出，如果输出多个json，每个json都要单独用```json包裹，你可以重复使用同一个动作或不同动作:
**示例**
// 理由文本
```json
{{
    "action":"动作名",
    "target_message_id":"触发动作的消息id",
    //对应参数
}}
```
```json
{{
    "action":"动作名",
    "target_message_id":"触发动作的消息id",
    //对应参数
}}
```

""",
        "brain_planner_prompt",
    )

    Prompt(
        """
{action_name}
动作描述：{action_description}
使用条件：
{action_require}
{{
    "action": "{action_name}",{action_parameters},
    "target_message_id":"触发action的消息id",
    "reason":"触发action的原因"
}}
""",
        "brain_action_prompt",
    )