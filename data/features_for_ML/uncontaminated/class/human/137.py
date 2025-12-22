from datetime import datetime
from src.chat.utils.prompt_builder import Prompt, global_prompt_manager
from src.chat.utils.chat_message_builder import (
    get_raw_msg_by_timestamp_with_chat,
    build_readable_messages,
)
import time
from src.config.config import global_config, model_config
from src.llm_models.utils_model import LLMRequest
from src.plugin_system.apis import frequency_api

class FrequencyControl:
    """简化的频率控制类，仅管理不同chat_id的频率值"""

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        # 发言频率调整值
        self.talk_frequency_adjust: float = 1.0
        
        self.last_frequency_adjust_time: float = 0.0
        self.frequency_model = LLMRequest(
            model_set=model_config.model_task_config.utils_small, request_type="frequency.adjust"
        )

    def get_talk_frequency_adjust(self) -> float:
        """获取发言频率调整值"""
        return self.talk_frequency_adjust

    def set_talk_frequency_adjust(self, value: float) -> None:
        """设置发言频率调整值"""
        self.talk_frequency_adjust = max(0.1, min(5.0, value))
        
        
    async def trigger_frequency_adjust(self) -> None:
        msg_list = get_raw_msg_by_timestamp_with_chat(
            chat_id=self.chat_id,
            timestamp_start=self.last_frequency_adjust_time,
            timestamp_end=time.time(),
        )
        
        
        if time.time() - self.last_frequency_adjust_time < 120 or len(msg_list) <= 5:
            return
        else:
            new_msg_list = get_raw_msg_by_timestamp_with_chat(
                chat_id=self.chat_id,
                timestamp_start=self.last_frequency_adjust_time,
                timestamp_end=time.time(),
                limit=5,
                limit_mode="latest",
            )
            
            message_str = build_readable_messages(
                new_msg_list,
                replace_bot_name=True,
                timestamp_mode="relative",
                read_mark=0.0,
                show_actions=False,
            )
            time_block = f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            bot_name = global_config.bot.nickname
            bot_nickname = (
                f",也有人叫你{','.join(global_config.bot.alias_names)}" if global_config.bot.alias_names else ""
            )
            name_block = f"你的名字是{bot_name}{bot_nickname}，请注意哪些是你自己的发言。"

            prompt = await global_prompt_manager.format_prompt(
                "frequency_adjust_prompt",
                name_block=name_block,
                time_block=time_block,
                message_str=message_str,
            )
            response, (reasoning_content, _, _) = await self.frequency_model.generate_response_async(
                prompt,
            )
            
            # logger.info(f"频率调整 prompt: {prompt}")
            # logger.info(f"频率调整 response: {response}")
            
            if global_config.debug.show_prompt:
                logger.info(f"频率调整 prompt: {prompt}")
                logger.info(f"频率调整 response: {response}")
                logger.info(f"频率调整 reasoning_content: {reasoning_content}")
            
            final_value_by_api = frequency_api.get_current_talk_value(self.chat_id)

            # LLM依然输出过多内容时取消本次调整。合法最多4个字，但有的模型可能会输出一些markdown换行符等，需要长度宽限
            if len(response) < 20:
                if "过于频繁" in response:
                    logger.info(f"频率调整: 过于频繁，调整值到{final_value_by_api}")
                    self.talk_frequency_adjust = max(0.1, min(3.0, self.talk_frequency_adjust * 0.8))
                elif "过少" in response:
                    logger.info(f"频率调整: 过少，调整值到{final_value_by_api}")
                    self.talk_frequency_adjust = max(0.1, min(3.0, self.talk_frequency_adjust * 1.2))
                self.last_frequency_adjust_time = time.time()
            else:
                logger.info(f"频率调整：response不符合要求，取消本次调整")