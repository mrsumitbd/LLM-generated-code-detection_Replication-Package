import time
from typing import Dict, List, Optional, Union, AsyncGenerator, Any
from app.models.schemas import OpenAIRequest

class ProviderRouter:
    """提供商路由器"""
    
    def __init__(self):
        self.factory = ProviderFactory()
    
    async def route_request(
        self, 
        request: OpenAIRequest,
        **kwargs
    ) -> Union[Dict[str, Any], AsyncGenerator[str, None]]:
        """路由请求到合适的提供商"""
        logger.info(f"🚦 路由请求: 模型={request.model}, 流式={request.stream}")
        
        # 获取提供商
        provider = self.factory.get_provider_for_model(request.model)
        if not provider:
            error_msg = f"不支持的模型: {request.model}"
            logger.error(f"❌ {error_msg}")
            return {
                "error": {
                    "message": error_msg,
                    "type": "invalid_request_error",
                    "code": "model_not_found"
                }
            }
        
        logger.info(f"✅ 使用提供商: {provider.name}")
        
        try:
            # 调用提供商处理请求
            result = await provider.chat_completion(request, **kwargs)
            logger.info(f"🎉 请求处理完成: {provider.name}")
            return result
            
        except Exception as e:
            error_msg = f"提供商 {provider.name} 处理请求失败: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return provider.handle_error(e, "路由处理")
    
    def get_provider_for_model(self, model: str) -> Optional[Dict[str, str]]:
        """
        获取模型对应的提供商信息

        Returns:
            包含提供商名称的字典，例如 {"provider": "zai"}
        """
        provider = self.factory.get_provider_for_model(model)
        if provider:
            return {"provider": provider.name}
        return None

    def get_models_list(self) -> Dict[str, Any]:
        """获取模型列表（OpenAI格式）"""
        models = []
        current_time = int(time.time())

        # 按提供商分组获取模型
        for provider_name in self.factory.list_providers():
            provider_models = self.factory.get_models_for_provider(provider_name)
            for model in provider_models:
                models.append({
                    "id": model,
                    "object": "model",
                    "created": current_time,
                    "owned_by": provider_name
                })

        return {
            "object": "list",
            "data": models
        }