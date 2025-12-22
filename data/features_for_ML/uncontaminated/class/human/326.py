import asyncio
from maim_message import Seg
from src.chat.message_receive.message import MessageSending
from src.chat.message_receive.storage import MessageStorage
from src.chat.utils.utils import calculate_typing_time
from src.plugin_system.base.component_types import EventType
from src.plugin_system.core.events_manager import events_manager

class UniversalMessageSender:
    """管理消息的注册、即时处理、发送和存储，并跟踪思考状态。"""

    def __init__(self):
        self.storage = MessageStorage()

    async def send_message(
        self, message: MessageSending, typing=False, set_reply=False, storage_message=True, show_log=True
    ):
        """
        处理、发送并存储一条消息。

        参数：
            message: MessageSending 对象，待发送的消息。
            typing: 是否模拟打字等待。

        用法：
            - typing=True 时，发送前会有打字等待。
        """
        if not message.chat_stream:
            logger.error("消息缺少 chat_stream，无法发送")
            raise ValueError("消息缺少 chat_stream，无法发送")
        if not message.message_info or not message.message_info.message_id:
            logger.error("消息缺少 message_info 或 message_id，无法发送")
            raise ValueError("消息缺少 message_info 或 message_id，无法发送")

        chat_id = message.chat_stream.stream_id
        message_id = message.message_info.message_id

        try:
            if set_reply:
                message.build_reply()
                logger.debug(f"[{chat_id}] 选择回复引用消息: {message.processed_plain_text[:20]}...")

            from src.plugin_system.core.events_manager import events_manager
            from src.plugin_system.base.component_types import EventType

            continue_flag, modified_message = await events_manager.handle_mai_events(
                EventType.POST_SEND_PRE_PROCESS, message=message, stream_id=chat_id
            )
            if not continue_flag:
                logger.info(f"[{chat_id}] 消息发送被插件取消: {str(message.message_segment)[:100]}...")
                return False
            if modified_message:
                if modified_message._modify_flags.modify_message_segments:
                    message.message_segment = Seg(type="seglist", data=modified_message.message_segments)
                if modified_message._modify_flags.modify_plain_text:
                    logger.warning(f"[{chat_id}] 插件修改了消息的纯文本内容，可能导致此内容被覆盖。")
                    message.processed_plain_text = modified_message.plain_text

            await message.process()

            continue_flag, modified_message = await events_manager.handle_mai_events(
                EventType.POST_SEND, message=message, stream_id=chat_id
            )
            if not continue_flag:
                logger.info(f"[{chat_id}] 消息发送被插件取消: {str(message.message_segment)[:100]}...")
                return False
            if modified_message:
                if modified_message._modify_flags.modify_message_segments:
                    message.message_segment = Seg(type="seglist", data=modified_message.message_segments)
                if modified_message._modify_flags.modify_plain_text:
                    message.processed_plain_text = modified_message.plain_text

            if typing:
                typing_time = calculate_typing_time(
                    input_string=message.processed_plain_text,
                    thinking_start_time=message.thinking_start_time,
                    is_emoji=message.is_emoji,
                )
                await asyncio.sleep(typing_time)

            sent_msg = await _send_message(message, show_log=show_log)
            if not sent_msg:
                return False

            continue_flag, modified_message = await events_manager.handle_mai_events(
                EventType.AFTER_SEND, message=message, stream_id=chat_id
            )
            if not continue_flag:
                logger.info(f"[{chat_id}] 消息发送后续处理被插件取消: {str(message.message_segment)[:100]}...")
                return True
            if modified_message:
                if modified_message._modify_flags.modify_message_segments:
                    message.message_segment = Seg(type="seglist", data=modified_message.message_segments)
                if modified_message._modify_flags.modify_plain_text:
                    message.processed_plain_text = modified_message.plain_text

            if storage_message:
                await self.storage.store_message(message, message.chat_stream)

            return sent_msg

        except Exception as e:
            logger.error(f"[{chat_id}] 处理或存储消息 {message_id} 时出错: {e}")
            raise e